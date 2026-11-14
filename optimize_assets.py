"""Generate high-quality page previews and text-based webfont subsets."""

import hashlib
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageOps
from fontTools import subset
from fontTools.ttLib import TTFont


MAX_IMAGE_WIDTH = 2400
IMAGE_QUALITY = 94
FONT_FILES = {
    "title": "zihun-jingsisong.woff2",
    "label": "hy-yakuhei-75.woff2",
}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
IMAGE_TAG = re.compile(r"<img\b[^>]*>", re.I)
SOURCE_ATTRIBUTE = re.compile(r"\ssrc=([\"'])(.*?)\1", re.I)


class FontTextParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.characters = {name: set() for name in FONT_FILES}

    def handle_starttag(self, tag, attributes):
        classes = set(dict(attributes).get("class", "").split())
        ancestor_classes = set().union(*(entry[1] for entry in self.stack))
        font = self.stack[-1][2] if self.stack else None
        if tag == "h1" or "next-project" in classes:
            font = "title"
        if tag == "h2" and ancestor_classes & {"section-intro", "about-heading", "e3-contact"}:
            font = "title"
        if "project-wordmark" in classes or (tag == "h3" and "project-caption" in ancestor_classes):
            font = "label"
        if tag not in VOID_TAGS:
            self.stack.append((tag, classes, font))

    def handle_startendtag(self, tag, attributes):
        self.handle_starttag(tag, attributes)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, text):
        font = self.stack[-1][2] if self.stack else None
        if font:
            self.characters[font].update(text)


def build_font_subsets(output, pages):
    characters = {name: set() for name in FONT_FILES}
    for page in pages:
        parser = FontTextParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for name in characters:
            characters[name].update(parser.characters[name])
    urls = {}
    savings = 0
    for name, filename in FONT_FILES.items():
        source = output / "assets/fonts" / filename
        # Include Latin text and numbers, which may appear alongside Chinese titles.
        text = "".join(sorted(characters[name] | {chr(code) for code in range(32, 127)}))
        digest = hashlib.sha256(source.read_bytes() + text.encode()).hexdigest()[:12]
        target = source.with_name(f"{source.stem}-subset-{digest}.woff2")
        font = TTFont(source, recalcTimestamp=False)
        original_codepoints = set(font.getBestCmap())
        options = subset.Options()
        options.flavor = "woff2"
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        font.flavor = "woff2"
        font.save(target)
        font.close()
        with TTFont(target) as result:
            required = {ord(character) for character in text} & original_codepoints
            if not required <= set(result.getBestCmap()):
                raise RuntimeError(f"字体子集缺少页面文字：{filename}")
        url = "/" + target.relative_to(output).as_posix()
        css = output / "edition3.css"
        content = css.read_text().replace("/assets/fonts/" + filename, url)
        css.write_text(content)
        urls[name] = url
        savings += source.stat().st_size - target.stat().st_size
        print(f"字体 {filename}：{source.stat().st_size // 1024} KB → {target.stat().st_size // 1024} KB", flush=True)
    return urls, savings


def build_image_preview(output, source_url, cache):
    location = urlsplit(source_url)
    if location.scheme or location.netloc:
        return None
    path = (output / unquote(location.path).lstrip("/")).resolve()
    if not path.is_relative_to(output.resolve()) or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        return None
    if not path.is_file():
        raise RuntimeError(f"页面图片缺失：{source_url}")
    with Image.open(path) as original:
        if getattr(original, "n_frames", 1) > 1:
            return None
        width, height = original.size
        if path.stat().st_size < 150_000 and width <= MAX_IMAGE_WIDTH:
            return None
        if path.suffix.lower() == ".webp" and width <= MAX_IMAGE_WIDTH:
            return None
        digest = hashlib.sha256(path.read_bytes() + f"preview-v1-{MAX_IMAGE_WIDTH}-{IMAGE_QUALITY}".encode()).hexdigest()[:16]
        filename = f"{path.stem}-{digest}.webp"
        cached = cache / filename
        if not cached.is_file():
            image = ImageOps.exif_transpose(original).convert("RGBA" if "A" in original.getbands() or "transparency" in original.info else "RGB")
            if image.width > MAX_IMAGE_WIDTH:
                target_height = round(image.height * MAX_IMAGE_WIDTH / image.width)
                image = image.resize((MAX_IMAGE_WIDTH, target_height), Image.Resampling.LANCZOS)
            with tempfile.NamedTemporaryFile(dir=cache, suffix=".webp", delete=False) as temporary:
                temporary_path = Path(temporary.name)
            try:
                image.save(temporary_path, format="WEBP", quality=IMAGE_QUALITY, alpha_quality=100, method=6)
                temporary_path.replace(cached)
            finally:
                temporary_path.unlink(missing_ok=True)
        if cached.stat().st_size >= path.stat().st_size:
            return None
        target = output / "assets/optimized" / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, target)
        return "/" + target.relative_to(output).as_posix(), width, height, path.stat().st_size - target.stat().st_size


def optimize_assets(output):
    output = Path(output)
    cache = Path.home() / ".cache/yuki52-publish/previews"
    cache.mkdir(parents=True, exist_ok=True)
    pages = sorted(output.rglob("*.html"))
    font_urls, font_savings = build_font_subsets(output, pages)
    previews = {}
    for page in pages:
        content = page.read_text(encoding="utf-8")

        def replace_image(match):
            tag = match.group()
            attribute = SOURCE_ATTRIBUTE.search(tag)
            if not attribute:
                return tag
            source_url = attribute.group(2)
            if source_url not in previews:
                previews[source_url] = build_image_preview(output, source_url, cache)
            preview = previews[source_url]
            if not preview:
                return tag
            url, width, height, _ = preview
            tag = tag[:attribute.start(2)] + escape(url, quote=True) + tag[attribute.end(2):]
            dimensions = ""
            if not re.search(r"\swidth=", tag):
                dimensions += f' width="{width}"'
            if not re.search(r"\sheight=", tag):
                dimensions += f' height="{height}"'
            return tag[:-1] + dimensions + ">"

        content = IMAGE_TAG.sub(replace_image, content)
        if "edition3.css" in content:
            preloads = [font_urls["title"]]
            if page == output / "index.html":
                preloads.append(font_urls["label"])
            links = "".join(f'<link rel="preload" href="{url}" as="font" type="font/woff2" crossorigin>' for url in preloads)
            content = content.replace("</head>", links + "</head>")
        page.write_text(content, encoding="utf-8")
    changed = [preview for preview in previews.values() if preview]
    image_savings = sum(preview[3] for preview in changed)
    # Content versions make new styles, scripts and font URLs take effect on the next visit.
    for page in pages:
        content = page.read_text(encoding="utf-8")

        def version_file(match):
            url = match.group(2)
            location = urlsplit(url)
            asset = output / location.path.lstrip("/")
            if location.scheme or location.netloc or asset.suffix not in {".css", ".js"} or not asset.is_file():
                return match.group()
            digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
            return f'{match.group(1)}"{location.path}?v={digest}"'

        content = re.sub(r'(\b(?:src|href)=)"([^"]+)"', version_file, content)
        page.write_text(content, encoding="utf-8")
    print(f"已生成 {len(changed)} 个高质量预览，图片下载量合计减少 {image_savings / 1024 / 1024:.1f} MB，字体减少 {font_savings / 1024 / 1024:.2f} MB", flush=True)
