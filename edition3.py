"""Build the third portfolio edition using the existing case content."""
from html import escape
import json
from pathlib import Path
import re
from scrapbook import render_footer, render_navigation, render_scrapbook
from edition3_gallery import PROJECT_ORDER, selected_projects, project_gallery, image_preview


ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VISIBLE_PROJECT_ORDER = tuple(slug for slug in PROJECT_ORDER if slug != "game-link")


FLOWER_PATHS = {
    "blue": 'M272 197 C250 165 238 119 244 81 C240 48 279 28 313 33 C346 27 363 64 361 105 C364 137 353 173 343 194 C363 158 414 119 452 130 C480 133 496 166 488 196 C487 222 442 255 403 270 C451 261 509 267 541 288 C576 313 556 352 521 364 C480 385 442 383 400 377 C430 408 458 459 445 494 C434 528 397 542 366 529 C335 518 324 470 310 428 C309 470 285 532 248 550 C216 567 177 542 170 511 C161 477 191 430 218 394 C183 412 128 429 98 415 C63 403 50 374 63 344 C76 315 127 297 170 293 C126 281 80 252 75 221 C68 188 96 164 126 171 C168 176 206 199 236 217 C231 199 245 192 272 197 Z',
    "red": 'M252.1 61.1 C255.6 42.5 286.9 34.4 302.0 35.0 C317.1 35.6 335.6 45.3 342.8 64.7 C349.9 84.0 336.1 146.2 344.9 151.2 C353.7 156.3 378.7 103.0 395.7 95.1 C412.7 87.1 436.2 94.7 447.0 103.5 C457.9 112.4 462.8 130.5 460.6 148.1 C458.4 165.6 421.1 199.9 433.8 208.8 C446.4 217.7 513.4 194.6 536.6 201.2 C559.8 207.8 570.7 232.5 572.8 248.2 C575.0 264.0 567.3 284.7 549.5 296.0 C531.7 307.3 472.2 306.1 465.8 316.1 C459.3 326.1 503.3 340.7 510.7 355.8 C518.1 371.0 517.3 395.0 510.4 406.8 C503.5 418.6 486.5 427.3 469.4 426.8 C452.3 426.3 413.0 393.1 407.8 403.7 C402.6 414.3 439.0 468.8 438.1 490.4 C437.3 512.1 416.8 528.2 402.8 533.5 C388.8 538.8 369.0 535.6 354.2 522.2 C339.5 508.9 327.6 448.4 314.4 453.5 C301.2 458.7 291.5 534.8 275.0 553.1 C258.4 571.4 230.5 568.9 215.2 563.2 C199.9 557.6 184.6 541.3 183.3 519.3 C182.0 497.3 211.6 443.4 207.4 431.2 C203.1 418.9 173.0 447.0 157.6 445.6 C142.1 444.1 121.5 433.5 114.6 422.4 C107.7 411.2 109.0 392.4 116.2 378.7 C123.3 365.0 167.0 348.3 157.6 340.1 C148.2 332.0 79.8 340.5 59.7 330.1 C39.5 319.6 35.0 292.8 36.6 277.4 C38.3 262.1 49.9 244.9 69.7 238.1 C89.5 231.3 147.2 246.2 155.5 236.8 C163.8 227.5 123.1 199.1 119.4 181.9 C115.8 164.7 123.9 142.8 133.7 133.4 C143.5 124.1 164.3 122.1 178.2 125.6 C192.1 129.1 212.2 161.8 217.0 154.6 C221.8 147.4 201.6 100.4 207.0 82.5 C212.3 64.7 234.7 50.0 249.2 47.6 C263.7 45.1 288.7 51.1 294.0 67.5 C299.3 84.0 288.0 147.5 281.0 146.5 C274.0 145.4 248.6 79.7 252.1 61.1 Z',
}


def flower_shape(kind="blue", color="#84def9", center="#0636ce"):
    return (
        '<svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
        f'<path d="{FLOWER_PATHS[kind]}" fill="{color}" />'
        f'<path d="M279 239 C309 221 350 245 358 274 C375 306 357 344 327 357 '
        f'C296 374 255 351 247 323 C232 294 250 254 279 239 Z" fill="{center}" /></svg>'
    )


def apply_scrapbook_shell(page, slug, is_project):
    resume = slug == "resume"
    dark = slug == "ai-game"
    nav = render_navigation("about" if resume else "work" if is_project else "")
    footer = render_footer()

    if re.search(r'<header class="(?:site-header|e3-header)">', page):
        page = re.sub(r'<header class="(?:site-header|e3-header)">.*?</header>', nav, page, count=1, flags=re.S)
    else:
        page = re.sub(r'(<main\b)', lambda m: nav + m[0], page, count=1)

    if re.search(r'<footer class="(?:footer|e3-footer e3-wrap|site-footer)">', page):
        page = re.sub(r'<footer class="(?:footer|e3-footer e3-wrap|site-footer)">.*?</footer>', footer, page, count=1, flags=re.S)
        page = page.replace(f'<div class="wrap">{footer}</div>', footer)
    else:
        page = page.replace('</main>', '</main>' + footer, 1)

    if 'class="page-mast"' not in page:
        if resume:
            pattern = r'(<h1>.*?</h1><p class="resume-subtitle">.*?</p><p class="resume-summary">.*?</p>)'
            page = re.sub(
                pattern,
                r'<div class="page-mast"><p class="page-kicker">RESUME</p>\1</div>',
                page,
                count=1,
                flags=re.S,
            )
        elif is_project and 'class="wrap detail"' in page:
            pattern = (
                r'(?P<context><div class="detail-top">.*?</div>)?(?P<title><h1>.*?</h1>)'
                r'(?:<p class="detail-meta">(?P<tags>.*?)</p>)?(?P<lead><p class="case-lead">.*?</p>)?'
            )
            page = re.sub(pattern, render_case_mast, page, count=1, flags=re.S)

    page = re.sub(r'(class="edition-three e3-case)(?! scrapbook-inner)', r'\1 scrapbook-inner', page, count=1)
    page = re.sub(
        r'(<meta name="theme-color" content=")[^"]*',
        lambda m: m[1] + ("#24212b" if dark else "#f8f7f3"),
        page,
        count=1,
    )
    styles = '<link rel="stylesheet" href="/scrapbook.css"><link rel="stylesheet" href="/scrapbook-pages.css">'
    return page.replace(styles, "").replace('</head>', styles + '</head>', 1)


def render_case_mast(match):
    context = match["context"] or ""
    lead = match["lead"] or ""
    tags = ""
    if match["tags"]:
        items = "".join(f"<li>{item.strip()}</li>" for item in match["tags"].split(" · "))
        tags = f'<ul class="case-tags" aria-label="项目关键词">{items}</ul>'
    return (
        '<div class="page-mast"><div class="case-heading">'
        f'<p class="page-kicker">CASE STUDY</p>{match["title"]}{lead}{context}</div>{tags}</div>'
    )


def build_edition3():
    content = json.loads((ROOT / "content.json").read_text())
    origin = json.loads((ROOT / ".openai/hosting.json").read_text()).get("site_url", "https://yuki-edition-3.yuki3316950442.chatgpt.site")
    projects = selected_projects(content)
    assets = json.loads((ROOT / "edition3-assets.json").read_text())
    figma_boards = json.loads((ROOT / "edition3-figma.json").read_text())
    (DIST / "index.html").write_text(render_scrapbook(origin))
    # Case demos keep their original scripts and receive the third-edition shell.
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text().replace('content="#101210"', 'content="#f7f5ef"')
        page = page.replace('href="/favicon.svg" type="image/svg+xml"', 'href="/favicon-cat.webp" type="image/webp"')
        page = re.sub(r'<link rel="stylesheet" href="/edition3\.css(?:\?[^"]*)?">', "", page)
        page = re.sub(r'<script src="/edition3\.js(?:\?[^"]*)?" defer></script>', "", page)
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css?v=figma-20261114"><script src="/edition3.js?v=flower-stop" defer></script></head>')
        page = page.replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        (path).write_text(page)
    from site_base import head
    for slug in ("spring-gala", "game-link", "game-events"):
        project = projects[slug]
        page = head(project["title"] + ' · Yuki Design', project["summary"], '/work/' + slug + '.html').replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css?v=figma-20261114"><script src="/edition3.js?v=flower-stop" defer></script></head>')
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page += f'<main class="wrap detail" id="main"><a class="back-link" href="/#project-{slug}">返回作品</a><h1>{escape(project["title"])}</h1><p class="case-lead">{escape(project["summary"])}</p>{project_gallery(project, assets, figma_boards)}</main>' + image_preview() + '</body></html>'
        (DIST / 'work' / f'{slug}.html').write_text(page)

    for slug in PROJECT_ORDER:
        path = DIST / 'work' / f'{slug}.html'
        page = path.read_text()
        if slug == "ai-game":
            page = page.replace('class="edition-three e3-case"', 'class="edition-three e3-case e3-card-dark"')
            page = page.replace('</head>', '<link rel="stylesheet" href="/card-dark.css?v=taro-radial"></head>')
            page = page.replace('</head>', '<link rel="stylesheet" href="/card-story.css?v=20261121-latest"><script src="/card-story.js?v=20261119" defer></script></head>')
            page = page.replace('name="theme-color" content="#f7f5ef"', 'name="theme-color" content="#302a3b"')
            start = page.index('<div class="case-reading card-case-reading">')
            end = page.index('</main>', start)
            story = (ROOT / "card-story.html").read_text()
            page = page[:start] + story + page[end:]
        elif slug == "ai-review":
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
            page = page.replace('class="edition-three e3-case"', 'class="edition-three e3-case e3-review"')
        elif slug == "dual-screen":
            start = page.index('<section class="project-guide"')
            end = page.index('</main>', start)
            page = page[:start] + (ROOT / "dual-screen-case.html").read_text() + page[end:]
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
            page = page.replace('<body id="top" class="edition-three e3-case">', '<body id="top" class="edition-three e3-case dual-screen-case">')
            page = re.sub(r'<h1>.*?</h1>', '<h1>提升游戏直播开看播体验</h1>', page, count=1, flags=re.S)
            page = re.sub(r'<div class="detail-top">.*?</div>', '', page, flags=re.S)
            page = re.sub(r'<p class="detail-meta">.*?</p>', '', page, flags=re.S)
            page = page.replace('直播双屏项目 · Yuki Design', '提升游戏直播开看播体验 · Yuki Design')
            page = page.replace('</head>', '<link rel="stylesheet" href="/dual-screen-case.css"></head>')
        page = re.sub(r'<section class="case-assets">.*?</section>', '', page, flags=re.S)
        if 'id="art-lightbox"' not in page:
            page = page.replace('</body>', image_preview() + '</body>')
        path.write_text(page)
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = re.sub(r'<a class="next-project".*?</a>', '', path.read_text(), flags=re.S)
        path.write_text(apply_scrapbook_shell(page, path.stem, path.parent.name == "work"))
    sitemap = DIST / "sitemap.xml"
    routes = ['/', '/resume.html'] + [f'/work/{slug}.html' for slug in VISIBLE_PROJECT_ORDER]
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{origin}{route}</loc></url>' for route in routes) + '</urlset>')
    (DIST / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    print('Built Edition 3 homepage, case navigation and site metadata.')


if __name__ == "__main__":
    build_edition3()
