"""Build the portfolio and publish it to yuki52.com with one command."""

import argparse
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
import urllib.error
import urllib.request


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


def build(directory):
    print("正在构建网站", flush=True)
    snapshot = directory / "source"
    shutil.copytree(
        SOURCE,
        snapshot,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".DS_Store"),
    )
    run([sys.executable, "build.py"], snapshot)
    output = snapshot / "dist"
    for path in output.rglob("*"):
        if path.suffix.lower() in {".html", ".css", ".js", ".json", ".xml", ".txt", ".svg"}:
            content = path.read_text(encoding="utf-8")
            for origin in OLD_ORIGINS:
                content = content.replace(origin, SITE_URL)
            content = re.sub(r"([\"'`(])/yuki-edition-3/", r"\1/", content)
            path.write_text(content, encoding="utf-8")
    (output / "CNAME").write_text("yuki52.com\n", encoding="utf-8")
    (output / ".nojekyll").touch()
    if not (output / "index.html").is_file():
        raise RuntimeError("构建结果缺少 index.html")
    card_script = (output / "demos/card-effects/card-preview.js").read_text()
    assets = set(re.findall(r"[\"'](/demos/[^\"'\s]+\.webp)[\"']", card_script))
    missing = sorted(asset for asset in assets if not (output / asset.lstrip("/")).is_file())
    if missing:
        raise RuntimeError("卡牌素材缺失\n" + "\n".join(missing))
    from optimize_assets import optimize_assets
    optimize_assets(output)
    print(f"构建完成，已检查 {len(assets)} 个卡牌素材，域名已配置", flush=True)
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
