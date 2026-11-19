"""Build the third portfolio edition using the existing case content."""
from html import escape
import json
from pathlib import Path
import re
from edition3_gallery import PROJECT_ORDER, selected_projects, project_gallery, image_preview


ROOT = Path(__file__).parent
DIST = ROOT / "dist"
VISIBLE_PROJECT_ORDER = tuple(slug for slug in PROJECT_ORDER if slug != "game-link")


def build_edition3():
    content = json.loads((ROOT / "content.json").read_text())
    origin = json.loads((ROOT / ".openai/hosting.json").read_text()).get("site_url", "https://yuki-edition-3.yuki3316950442.chatgpt.site")
    projects = selected_projects(content)
    assets = json.loads((ROOT / "edition3-assets.json").read_text())
    figma_boards = json.loads((ROOT / "edition3-figma.json").read_text())
    email = "435456341@qq.com"
    brand = '<a class="shelf-brand" href="/" aria-label="Yuki 首页">iamyuki</a>'
    nav_links = '<a class="shelf-marker" href="/#work">作品</a><a class="shelf-marker" href="/#about">关于我</a><a class="shelf-marker" href="/#contact">联系</a>'
    navigation = f'''<header class="shelf-header shelf-wrap">
      {brand}
      <nav class="shelf-nav" aria-label="主导航">{nav_links}</nav>
      <details class="shelf-mobile-menu"><summary>菜单 <span aria-hidden="true">⌄</span></summary><nav class="shelf-nav" aria-label="主导航">{nav_links}</nav></details>
    </header>'''
    footer = '''<footer class="shelf-footer shelf-wrap">
      <div class="shelf-footer-cats" aria-hidden="true">
        <img src="/assets/folder-portfolio/cat.webp" alt="" width="42" height="44" loading="lazy">
        <img src="/assets/folder-portfolio/cat-companion.webp" alt="" width="46" height="40" loading="lazy">
      </div>
      <div class="shelf-footer-row"><p>© 2026 吴雨晴</p><a class="shelf-marker" href="#top">回到顶部 <span aria-hidden="true">↑</span></a></div>
    </footer>'''
    stylesheet = '<link rel="stylesheet" href="/folder-portfolio.css?v=title-marker">'
    cards = []
    for slug in VISIBLE_PROJECT_ORDER:
        project = projects[slug]
        title = escape(project["title"]).replace("AI ", '<span class="shelf-latin">AI</span> ')
        sheets = ''.join(
            f'<img class="folder-sheet" src="/assets/folder-portfolio/{slug}-{number}.webp" alt="" width="240" height="300" loading="lazy" decoding="async" draggable="false">'
            for number in (1, 2, 3)
        )
        cards.append(f'''<li id="project-{slug}">
          <a class="project-folder folder-{slug}" href="/work/{slug}.html" aria-description="{escape(project['summary'])}">
            <span class="folder-art" aria-hidden="true"><span class="folder-back"></span>{sheets}<span class="folder-front"></span><span class="folder-front folder-front-right"></span></span>
            <span class="folder-label shelf-marker">{title}</span>
          </a>
        </li>''')
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#eae8e3"><title>Yuki · 吴雨晴｜体验与 AI 设计师</title>
<meta name="description" content="吴雨晴的抖音 IP、游戏直播、AI 产品与设计工作流作品集。">
<meta property="og:title" content="Yuki · 吴雨晴｜体验与 AI 设计师"><meta property="og:type" content="website"><meta property="og:url" content="{origin}/"><meta property="og:image" content="{origin}/assets/ai-card-cover.png">
<link rel="canonical" href="{origin}/"><link rel="icon" href="/favicon-cat.webp" type="image/webp">
<link rel="stylesheet" href="/edition3.css?v=plain-buttons">{stylesheet}<script src="/edition3.js?v=cat-expressions" defer></script></head>
<body class="edition-three shelf-home" id="top"><a class="e3-skip" href="#main">跳到主要内容</a>{navigation}
<main id="main">
  <section class="shelf-intro shelf-wrap" aria-labelledby="hero-title">
    <button class="shelf-cat" type="button" aria-label="让小猫微笑" aria-pressed="false">
      <img src="/assets/folder-portfolio/cat.webp" alt="" width="72" height="72" fetchpriority="high">
      <img class="shelf-cat-smile" src="/assets/folder-portfolio/cat-smile.webp" alt="" width="72" height="72">
    </button>
    <h1 id="hero-title">你好，我是吴雨晴<br>一名<a class="shelf-title-marker" href="#about">体验设计师</a><br>喜欢打磨更好的用户体验方式<br>也喜欢用AI 探索编程的世界</h1>
    <p class="shelf-bio" lang="en">I’m a designer who starts with design and follows ideas wherever they lead. I refine complex workflows, system frameworks, and collaborative experiences while exploring visual design, code, and motion. My work spans live streaming, tool platforms, games, and financial products. I’m proficient with AI tools and have developed my own AI workflow.</p>
  </section>
  <section class="shelf-work shelf-wrap" id="work" aria-labelledby="work-title">
    <h2 id="work-title">精选作品</h2>
    <ul class="folder-grid">{''.join(cards)}</ul>
  </section>
  <section class="shelf-about shelf-wrap" id="about" aria-labelledby="about-title">
    <div><h2 id="about-title">关于我</h2><a class="shelf-link" href="/resume.html"><span class="shelf-marker">查看完整简历</span><img class="shelf-resume-arrow" src="/assets/folder-portfolio/resume-arrow.svg" width="6" height="6" alt=""></a></div>
    <div class="shelf-about-copy">
      <ul class="shelf-career">
        <li><strong>字节跳动</strong><span>抖音 <span class="shelf-latin">IP</span> 与游戏 · 体验 / <span class="shelf-latin">AI</span> 设计</span><time>2021.04 — 至今</time></li>
        <li><strong>拼多多</strong><span>用户增长 · 交互设计</span><time>2020.12 — 2021.04</time></li>
        <li><strong>腾讯</strong><span>理财通 · 交互设计</span><time>2019.11 — 2020.12</time></li>
      </ul>
    </div>
  </section>
  <section class="shelf-contact shelf-wrap" id="contact" aria-labelledby="contact-title">
    <h2 id="contact-title">联系</h2>
    <div class="shelf-contact-actions">
      <a class="shelf-contact-card" href="mailto:{email}"><strong class="shelf-marker">发邮件</strong><small>{email} <span class="shelf-arrow" aria-hidden="true">↗</span></small></a>
      <button class="shelf-contact-card" type="button" data-copy-email aria-label="复制邮箱地址"><strong class="shelf-marker">复制邮箱</strong><small>{email}</small></button>
    </div>
    <p class="shelf-copy-status" data-copy-status role="status" aria-live="polite"></p>
  </section>
</main>{footer}</body></html>'''
    (DIST / "index.html").write_text(html)
    # Case demos keep their original scripts and receive the third-edition shell.
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text().replace('content="#101210"', 'content="#f7f5ef"')
        page = re.sub(r'<link rel="stylesheet" href="/edition3\.css(?:\?[^"]*)?">', "", page)
        page = re.sub(r'<script src="/edition3\.js(?:\?[^"]*)?" defer></script>', "", page)
        page = re.sub(r'<header class="(?:site-header|e3-header shelf-header|e3-header|shelf-header shelf-wrap)">.*?</header>', navigation, page, flags=re.S)
        page = re.sub(r'<footer class="(?:footer|e3-footer e3-wrap|e3-footer shelf-footer shelf-wrap|shelf-footer shelf-wrap)">.*?</footer>', footer, page, flags=re.S)
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css?v=plain-buttons"><script src="/edition3.js?v=cat-expressions" defer></script></head>')
        page = page.replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        (path).write_text(page)
    from site_base import head
    for slug in ("spring-gala", "game-link", "game-events"):
        project = projects[slug]
        page = head(project["title"] + ' · Yuki Design', project["summary"], '/work/' + slug + '.html').replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css?v=plain-buttons"><script src="/edition3.js?v=cat-expressions" defer></script></head>')
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page += navigation + f'<main class="wrap detail" id="main"><a class="back-link" href="/#project-{slug}">返回作品</a><h1>{escape(project["title"])}</h1><p class="case-lead">{escape(project["summary"])}</p>{project_gallery(project, assets, figma_boards)}</main>' + footer + image_preview() + '</body></html>'
        (DIST / 'work' / f'{slug}.html').write_text(page)

    for index, slug in enumerate(PROJECT_ORDER):
        path = DIST / 'work' / f'{slug}.html'
        page = path.read_text()
        if slug == "ai-game":
            page = page.replace('class="edition-three e3-case"', 'class="edition-three e3-case e3-card-dark"')
            page = page.replace('</head>', '<link rel="stylesheet" href="/card-dark.css?v=taro-radial"><link rel="stylesheet" href="/card-story.css?v=20261119-continuation"><script src="/card-story.js?v=20261119" defer></script></head>')
            page = page.replace('name="theme-color" content="#f7f5ef"', 'name="theme-color" content="#302a3b"')
            start = page.index('<div class="case-reading card-case-reading">')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + (ROOT / "card-story.html").read_text() + page[end:]
        elif slug == "ai-review":
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
            page = page.replace('class="edition-three e3-case"', 'class="edition-three e3-case e3-review"')
        elif slug == "dual-screen":
            start = page.index('<section class="project-guide"')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + (ROOT / "dual-screen-case.html").read_text() + page[end:]
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
            page = page.replace('<body id="top" class="edition-three e3-case">', '<body id="top" class="edition-three e3-case dual-screen-case">')
            page = re.sub(r'<h1>.*?</h1>', '<h1>提升游戏直播开看播体验</h1>', page, count=1, flags=re.S)
            page = re.sub(r'<div class="detail-top">.*?</div>', '', page, flags=re.S)
            page = re.sub(r'<p class="detail-meta">.*?</p>', '', page, flags=re.S)
            page = page.replace('直播双屏项目 · Yuki Design', '提升游戏直播开看播体验 · Yuki Design')
            page = page.replace('</head>', '<link rel="stylesheet" href="/dual-screen-case.css"></head>')
        page = re.sub(r'<section class="case-assets">.*?</section>', '', page, flags=re.S)
        visible_index = VISIBLE_PROJECT_ORDER.index(slug) if slug in VISIBLE_PROJECT_ORDER else -1
        next_slug = VISIBLE_PROJECT_ORDER[(visible_index + 1) % len(VISIBLE_PROJECT_ORDER)]
        next_link = f'<a class="next-project" href="/work/{next_slug}.html"><span>继续浏览</span><strong>{escape(projects[next_slug]["title"])}</strong></a>'
        if 'class="next-project"' in page:
            page = re.sub(r'<a class="next-project".*?</a>', next_link, page, flags=re.S)
        else:
            page = page.replace('</main>', next_link + '</main>')
        if 'id="art-lightbox"' not in page:
            page = page.replace('</body>', image_preview() + '</body>')
        path.write_text(page)
    for path in [DIST / "index.html", *sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text()
        if path.name != "index.html":
            page = page.replace('href="/favicon-cat.webp" type="image/webp"', 'href="/favicon-cat.webp" type="image/webp"')
            page = page.replace('name="theme-color" content="#f7f5ef"', 'name="theme-color" content="#eae8e3"')
            page = re.sub(r'<link rel="stylesheet" href="/folder-portfolio\.css(?:\?[^"]*)?">', '', page)
            page = page.replace('</head>', stylesheet + '</head>')
        path.write_text(page)
    sitemap = DIST / "sitemap.xml"
    routes = ['/', '/resume.html'] + [f'/work/{slug}.html' for slug in VISIBLE_PROJECT_ORDER]
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{origin}{route}</loc></url>' for route in routes) + '</urlset>')
    (DIST / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    print('Built Edition 3 homepage, case navigation and site metadata.')


if __name__ == "__main__":
    build_edition3()
