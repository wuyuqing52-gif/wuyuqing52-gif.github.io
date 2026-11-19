"""Build the portfolio and publish it to yuki52.com with one command."""

import argparse
import hashlib
import json
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import venv
import xml.etree.ElementTree as ET
import urllib.error
import urllib.request
from urllib.parse import urlsplit


SOURCE = Path(__file__).resolve().parent
SITE_URL = "https://yuki52.com"
REPOSITORY = "https://github.com/wuyuqing52-gif/yuki-edition-3.git"
API_URL = "https://api.github.com/repos/wuyuqing52-gif/yuki-edition-3/actions/runs"
OLD_ORIGINS = (
    "https://wuyuqing52-gif.github.io/yuki-edition-3",
    "https://yuki-edition-3.yuki3316950442.chatgpt.site",
    "https://yuki-design.yuki3316950442.chatgpt.site",
)


def run(arguments, directory, environment=None):
    result = subprocess.run(
        arguments,
        cwd=directory,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.strip()


def ensure_build_dependencies():
    modules = ("PIL", "fontTools", "brotli")
    if all(importlib.util.find_spec(module) for module in modules):
        return
    environment = Path.home() / ".cache/yuki52-publish/python"
    interpreter = environment / "bin/python"
    if not interpreter.is_file():
        venv.EnvBuilder(with_pip=True).create(environment)
    ready = subprocess.run(
        [str(interpreter), "-c", "import PIL, fontTools, brotli"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0
    if not ready:
        print("首次发布正在准备图片与字体处理依赖", flush=True)
        subprocess.run(
            [str(interpreter), "-m", "pip", "install", "Pillow>=10", "fonttools>=4", "brotli>=1"],
            check=True,
        )
    result = subprocess.run([str(interpreter), str(SOURCE / "publish.py"), *sys.argv[1:]])
    raise SystemExit(result.returncode)


def branch_revision(branch):
    try:
        return run(["git", "rev-parse", "--verify", "refs/heads/" + branch], SOURCE)
    except subprocess.CalledProcessError:
        return run(["git", "rev-parse", "--verify", "refs/remotes/origin/" + branch], SOURCE)


def snapshot_version(directory, branch):
    snapshot = directory / (branch + "-source")
    checkout = None
    checkouts = []
    worktrees = run(["git", "worktree", "list", "--porcelain", "-z"], SOURCE)
    for field in worktrees.split("\0"):
        if field.startswith("worktree "):
            checkout = Path(field.removeprefix("worktree "))
        elif field == "branch refs/heads/" + branch:
            checkouts.append(checkout)
    if checkouts:
        checkout = SOURCE if SOURCE in checkouts else checkouts[0]
        shutil.copytree(
            checkout,
            snapshot,
            ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
        )
        return snapshot
    archive = directory / (branch + ".tar")
    revision = branch_revision(branch)
    run(["git", "archive", "--format=tar", "--output=" + str(archive), revision], SOURCE)
    snapshot.mkdir()
    run(["tar", "-xf", str(archive), "-C", str(snapshot)], SOURCE)
    return snapshot


def add_version_prefix(output, prefix):
    # Match real top-level routes, including runtime JS strings and CSS URLs.
    roots = {path.name for path in output.iterdir()}
    url_pattern = re.compile(r"([\"'`(])(/(?![/>])[^\"'`<>\s)]*)")

    def replace_url(match):
        url = match.group(2)
        path = urlsplit(url).path
        if path == "/" or path.lstrip("/").split("/", 1)[0] in roots:
            return match.group(1) + prefix + url
        return match.group()

    for path in output.rglob("*"):
        if path.suffix.lower() not in {".html", ".css", ".js", ".json", ".xml", ".txt", ".svg"}:
            continue
        content = path.read_text(encoding="utf-8")
        # Full URLs cover canonical metadata, sitemap entries and robots.txt.
        content = content.replace(SITE_URL + "/", SITE_URL + prefix + "/")
        def replace_srcset(match):
            value = re.sub(r"(^|,\s*)(/[^,\s]+)", replace_url, match.group(3))
            return match.group(1) + match.group(2) + value + match.group(2)

        content = re.sub(r"((?:data-[\w-]+-)?srcset=)([\"'])(.*?)\2", replace_srcset, content, flags=re.I)
        content = url_pattern.sub(replace_url, content)
        path.write_text(content, encoding="utf-8")


def build_version(directory, branch):
    print("正在构建 " + branch, flush=True)
    snapshot = snapshot_version(directory, branch)
    run([sys.executable, "build.py"], snapshot)
    output = snapshot / "dist"
    for path in output.rglob("*"):
        if path.suffix.lower() in {".html", ".css", ".js", ".json", ".xml", ".txt", ".svg"}:
            content = path.read_text(encoding="utf-8")
            for origin in OLD_ORIGINS:
                content = content.replace(origin, SITE_URL)
            content = re.sub(r"([\"'`(])/yuki-edition-3/", r"\1/", content)
            path.write_text(content, encoding="utf-8")
    if not (output / "index.html").is_file():
        raise RuntimeError("构建结果缺少 index.html：" + branch)
    card_script = (output / "demos/card-effects/card-preview.js").read_text()
    assets = set(re.findall(r"[\"'](/demos/[^\"'\s]+\.webp)[\"']", card_script))
    missing = sorted(asset for asset in assets if not (output / asset.lstrip("/")).is_file())
    if missing:
        raise RuntimeError("卡牌素材缺失\n" + "\n".join(missing))
    from optimize_assets import optimize_assets
    optimize_assets(output)
    print(f"{branch} 构建完成，已检查 {len(assets)} 个卡牌素材", flush=True)
    return output


def build(directory):
    output = build_version(directory, "redbook")
    website = build_version(directory, "website")
    favicon = website / "favicon-cat.webp"
    shutil.copyfile(favicon, output / favicon.name)
    add_version_prefix(website, "/website")
    destination = output / "website"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(website, destination)
    legacy = output / "edition-3"
    if legacy.exists():
        shutil.rmtree(legacy)
    routes = run(["git", "ls-tree", "-r", "--name-only", branch_revision("edition-3"), "dist"], SOURCE)
    for route in routes.splitlines():
        relative = Path(route).relative_to("dist")
        if relative.suffix != ".html":
            continue
        target = "/website/" if relative == Path("index.html") or not (website / relative).is_file() else "/website/" + relative.as_posix()
        page = legacy / relative
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Yuki · 页面已更新</title><link rel="canonical" href="' + SITE_URL + target + '">'
            '<meta http-equiv="refresh" content="0;url=' + target + '"></head>'
            '<body><a href="' + target + '">查看更新后的作品集</a><script>'
            'location.replace(' + json.dumps(target) + '+location.search+location.hash);'
            '</script></body></html>', encoding="utf-8",
        )
    digest = hashlib.sha256((output / favicon.name).read_bytes()).hexdigest()[:12]
    icon = '<link rel="icon" href="/' + favicon.name + '?v=' + digest + '" type="image/webp">'
    for page in output.rglob("*.html"):
        content = page.read_text(encoding="utf-8")
        content = re.sub(r'<link\b(?=[^>]*\brel=["\'](?:shortcut )?icon["\'])[^>]*>', "", content)
        page.write_text(content.replace("</head>", icon + "</head>"), encoding="utf-8")
    (output / "CNAME").write_text("yuki52.com\n", encoding="utf-8")
    (output / ".nojekyll").touch()
    robots = output / "robots.txt"
    content = robots.read_text(encoding="utf-8") if robots.exists() else "User-agent: *\nAllow: /\n"
    robots.write_text(content.rstrip() + "\nSitemap: " + SITE_URL + "/website/sitemap.xml\n", encoding="utf-8")
    from optimize_assets import version_page_assets
    version_page_assets(output)
    for asset in output.rglob("*.svg"):
        try:
            ET.parse(asset)
        except ET.ParseError as error:
            raise RuntimeError("SVG 文件损坏：" + str(asset.relative_to(output))) from error
    print("双版本构建完成，redbook 为主站，website 发布在 /website/，旧版入口已添加跳转", flush=True)
    return output


def publish(directory, output):
    print("正在同步发布仓库", flush=True)
    repository = directory / "release"
    git = ["git", "-c", "credential.helper=store"]
    run(git + ["clone", "--depth", "1", "--filter=blob:none", "--no-checkout", REPOSITORY, str(repository)], SOURCE)
    parent = run(git + ["rev-parse", "HEAD"], repository)
    environment = os.environ.copy()
    environment["GIT_INDEX_FILE"] = str(directory / "release-index")
    author_name = run(["git", "config", "user.name"], SOURCE)
    author_email = run(["git", "config", "user.email"], SOURCE)
    environment.update(
        GIT_AUTHOR_NAME=author_name,
        GIT_AUTHOR_EMAIL=author_email,
        GIT_COMMITTER_NAME=author_name,
        GIT_COMMITTER_EMAIL=author_email,
    )
    run(git + ["read-tree", parent], repository, environment)
    run(git + ["--work-tree=" + str(output), "add", "--all"], repository, environment)
    tree = run(git + ["write-tree"], repository, environment)
    previous_tree = run(git + ["rev-parse", parent + "^{tree}"], repository)
    if tree == previous_tree:
        print("线上文件已与本次构建一致", flush=True)
        return parent
    commit = run(git + ["commit-tree", tree, "-p", parent, "-m", "Publish portfolio to yuki52.com"], repository, environment)
    print("正在上传网站文件", flush=True)
    run(git + ["push", "origin", commit + ":refs/heads/main"], repository, environment)
    return commit


def wait_for_deployment(commit):
    print("正在等待 GitHub Pages 部署", flush=True)
    headers = {"User-Agent": "yuki52-publisher", "Accept": "application/vnd.github+json"}
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        ["git", "-c", "credential.helper=store", "credential", "fill"],
        cwd=SOURCE,
        input="url=" + REPOSITORY + "\n\n",
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    credential = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if result.returncode == 0 and credential.get("password"):
        headers["Authorization"] = "Bearer " + credential["password"]
    deadline = time.monotonic() + 1200
    while time.monotonic() < deadline:
        request = urllib.request.Request(
            API_URL + "?head_sha=" + commit + "&per_page=10",
            headers=headers,
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                runs = json.load(response)["workflow_runs"]
            pages_runs = [item for item in runs if item["name"] == "pages build and deployment"]
            if pages_runs and pages_runs[0]["status"] == "completed":
                deployment = pages_runs[0]
                if deployment["conclusion"] != "success":
                    raise RuntimeError("GitHub Pages 部署失败，请查看仓库 Actions 中的运行记录")
                with urllib.request.urlopen(SITE_URL, timeout=30) as response:
                    if response.status != 200:
                        raise RuntimeError("部署已完成，网站访问检查尚未通过")
                print("发布完成，网站地址为 " + SITE_URL, flush=True)
                return
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(15)
    raise RuntimeError("代码已上传，部署检查超时，请查看仓库 Actions 中的运行记录")


def main():
    parser = argparse.ArgumentParser(description="一键发布个人网站到 yuki52.com")
    parser.add_argument("--check", action="store_true", help="构建并检查发布文件")
    arguments = parser.parse_args()
    ensure_build_dependencies()
    with tempfile.TemporaryDirectory(prefix="yuki52-publish-") as temporary:
        directory = Path(temporary)
        output = build(directory)
        if arguments.check:
            return
        commit = publish(directory, output)
        wait_for_deployment(commit)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as error:
        print((error.stderr or "").strip() or str(error), file=sys.stderr)
        sys.exit(1)
    except (RuntimeError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
