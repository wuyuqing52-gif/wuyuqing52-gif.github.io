"""Build the third portfolio edition using the existing case content."""
from html import escape
import json
from pathlib import Path
import re
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


def flower(kind):
    original = (
        '<span class="flower-frame flower-frame-ink">'
        f'<img src="/assets/edition3/hero-flower-{kind}.svg" alt="" '
        'width="775" height="775" loading="eager" fetchpriority="high" decoding="async" draggable="false"></span>'
    )
    variants = "".join(
        f'<span class="flower-frame flower-frame-{style}">'
        f'<img src="/assets/hero-flowers/{style}-{kind}.webp" alt="" width="775" height="775" loading="eager" decoding="async" draggable="false"></span>'
        for style in ("neon", "crayon", "paint")
    )
    return (
        f'<button class="flower flower-{kind}" data-flower data-start="{(-18 if kind == "blue" else 12)}" '
        'type="button" aria-label="旋转花朵并切换形态">'
        f'<span class="flower-art" aria-hidden="true">{original}{variants}</span></button>'
    )


def add_button_blooms(page):
    def decorate(match):
        attributes, content = match.group(1), match.group(2)
        if 'class="button-bloom"' in content:
            return match.group(0)
        class_match = re.search(r'class="([^"]*)"', attributes)
        class_names = class_match.group(1).split()
        if "e3-button" not in class_names:
            classes = class_match.group(1) + " e3-button"
            attributes = attributes.replace(class_match.group(0), f'class="{classes}"', 1)
        bloom = flower_shape("blue", "#0636ce", "#ffffff")
        return (f'<a{attributes}><span class="button-label">{content}</span>'
                f'<span class="button-bloom" aria-hidden="true">{bloom}</span></a>')
    return re.sub(
        r'<a(\s[^>]*class="[^"]*\b(?:primary-button|e3-button)\b[^"]*"[^>]*)>(.*?)</a>',
        decorate,
        page,
        flags=re.S,
    )


def build_edition3():
    content = json.loads((ROOT / "content.json").read_text())
    origin = json.loads((ROOT / ".openai/hosting.json").read_text()).get("site_url", "https://yuki-edition-3.yuki3316950442.chatgpt.site")
    projects = selected_projects(content)
    assets = json.loads((ROOT / "edition3-assets.json").read_text())
    figma_boards = json.loads((ROOT / "edition3-figma.json").read_text())
    wordmark = (DIST / 'assets/yuki-wordmark.svg').read_text().replace('<svg ', '<svg class="yuki-wordmark" aria-hidden="true" focusable="false" ', 1)
    navigation = f'''<header class="e3-header"><nav class="e3-nav" aria-label="主导航"><a class="nav-link" href="/#work">作品</a><a class="e3-brand" href="/" aria-label="Yuki 第三版首页">{wordmark}</a><a class="nav-link" href="/#about">关于我</a></nav></header>'''
    footer = f'''<footer class="e3-footer e3-wrap"><a class="e3-brand" href="/" aria-label="Yuki 首页">{wordmark}</a><p>© 2026 吴雨晴</p><a class="footer-top" href="#top">回到顶部</a></footer>'''
    (DIST / "favicon-flower.svg").write_text(flower_shape("blue", "#0636ce", "#ffd23c"))
    palettes = [
        ("#0636ce", "#ffd23c", "#f32312", "#ffcf4c"),
        ("#ff8fca", "#0636ce", "#ffffff", "#ff8fca"),
        ("#ffcf4c", "#f32312", "#ffffff", "#84def9"),
        ("#84def9", "#0636ce", "#ffffff", "#ffcf4c"),
        ("#f32312", "#ffcf4c", "#0636ce", "#ff8fca"),
        ("#ffcf4c", "#0636ce", "#ffffff", "#84def9"),
    ]
    marks = {
        "ai-game": "用AI<br>拓展设计师<br>能力边界",
        "ai-review": "用AI<br>改变设计师<br>工作流",
        "dual-screen": "发现核心问题<br>自驱动力",
        "spring-gala": "不设边界<br>挑战自我",
        "game-events": "深耕行业<br>解决复杂问题",
    }
    design_covers = {
        "ai-game": ("card-cover.webp", "card-detail.webp"),
        "ai-review": ("review-cover.webp", "review-detail.webp"),
        "dual-screen": ("dual-desktop.webp", "dual-phone.webp"),
        "spring-gala": ("spring-main.webp", "spring-detail.webp"),
        "game-events": ("events-desktop.webp", "events-phone.webp"),
    }
    cards = []
    for index, slug in enumerate(VISIBLE_PROJECT_ORDER):
        project = projects[slug]
        tile, petal, center, bloom = palettes[index]
        card_flower = flower_shape("blue", bloom, bloom).replace('</svg>', f'<circle cx="300" cy="300" r="190" fill="{bloom}" /></svg>')
        main, small = design_covers[slug]
        main_class = "original-cover" if slug in ("ai-game", "ai-review") else "has-alpha" if slug == "game-events" else ""
        small_class = "original-detail" if slug in ("ai-game", "ai-review") else ""
        collage = (
            f'<div class="collage-main {main_class}"><img src="/assets/edition3/{main}" '
            f'alt="{escape(project["title"])}" loading="lazy" decoding="async"></div>'
            f'<div class="collage-small {small_class}"><img src="/assets/edition3/{small}" '
            f'alt="{escape(project["title"])}项目细节" loading="lazy" decoding="async"></div>'
        )
        cards.append(f'''<article class="e3-project-row project-{slug}" id="project-{slug}">
          <a class="e3-project" href="/work/{slug}.html" aria-describedby="summary-{slug}">
            <span class="card-bloom" aria-hidden="true">{card_flower}</span>
            <div class="project-collage" aria-hidden="true">{collage}</div>
            <div class="project-copy"><div class="project-caption"><h3>{escape(project['title'])}</h3></div><p class="project-description" id="summary-{slug}">{escape(project['summary'])}</p><span class="case-action" aria-hidden="true">查看案例</span></div>
          </a>
          <div class="project-side"><a class="flower-tile" href="/work/{slug}.html" data-flower data-start="-9" style="background:{tile}" aria-label="查看{escape(project['title'])}"><span class="flower-art">{flower_shape("blue", petal, center)}</span></a><a class="project-wordmark" href="/work/{slug}.html" aria-label="查看{escape(project['title'])}">{marks[slug]}</a></div>
        </article>''')
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f5ef"><title>Yuki · 吴雨晴｜体验与 AI 设计师</title>
<meta name="description" content="设计是我的起点，不是我的边界。吴雨晴的抖音 IP、游戏直播、AI 产品与设计工作流作品集。">
<meta property="og:title" content="Yuki · 吴雨晴｜体验与 AI 设计师"><meta property="og:type" content="website"><meta property="og:url" content="{origin}/"><meta property="og:image" content="{origin}/assets/ai-card-cover.png">
<link rel="canonical" href="{origin}/"><link rel="icon" href="/favicon-flower.svg" type="image/svg+xml"><link rel="stylesheet" href="/edition3.css?v=figma-20261114"><script src="/edition3.js?v=flower-stop" defer></script></head>
<body class="edition-three" id="top"><a class="e3-skip" href="#main">跳到主要内容</a>{navigation}
<main id="main"><section class="e3-hero" aria-labelledby="hero-title">
{flower('blue')}{flower('red')}
<div class="hero-copy"><h1 id="hero-title"><span class="hero-line">设计是我的起点，</span><span class="hero-line">不是我的<span class="hero-word">边界<i aria-hidden="true"></i></span></span></h1>
<p class="hero-summary">你好，我是 Yuki / 吴雨晴。一名以设计为起点、不设边界的设计师。既打磨复杂流程、系统框架与协作体验，也探索代码、视觉、与动态表达。</p>
<div class="hero-actions"><a class="e3-button" href="#work"><span>看看我的作品</span><span class="button-bloom" aria-hidden="true">{flower_shape("blue", "#0636ce", "#ffffff")}</span></a></div></div>
<a class="hero-scroll" href="#work" aria-label="向下查看作品"><img src="/assets/edition3/hero-scroll.png" alt="" width="70" height="70" loading="eager" decoding="async"></a>
<p class="flower-status visually-hidden" role="status" aria-live="polite"></p>
</section>
<section class="e3-work e3-wrap" id="work" aria-labelledby="work-title"><div class="section-intro"><h2 id="work-title">My Work</h2></div><div class="e3-project-grid">{''.join(cards)}</div>
</section>
<section class="e3-about e3-wrap" id="about" aria-labelledby="about-title"><div class="about-heading"><p class="section-kicker">A LITTLE ABOUT ME</p><h2 id="about-title">设计之外，<br>还有<span class="serif-accent">好奇心。</span></h2><a class="e3-text-link" href="/resume.html">查看完整简历</a></div><div class="about-copy"><p class="about-lead">我喜欢把复杂的事情理清楚，<br>再把它做成可以体验的东西。</p><p>{escape(content['intro'])}</p><div class="expertise" aria-label="设计方向"><a href="/work/dual-screen.html">交互体验</a><a href="/work/ai-review.html">AI 工作流</a><a href="/work/ai-game.html">视觉与动态</a></div><ol class="about-career"><li><time>2021.04 — 至今</time><div><strong>字节跳动</strong><span>抖音 IP 与游戏 · 体验 / AI 设计</span></div></li><li><time>2020.12 — 2021.04</time><div><strong>拼多多</strong><span>用户增长 · 交互设计</span></div></li><li><time>2019.11 — 2020.12</time><div><strong>腾讯</strong><span>理财通 · 交互设计</span></div></li></ol></div></section>
<section class="e3-contact" id="contact" aria-labelledby="contact-title"><div class="contact-flower" aria-hidden="true">{flower_shape("blue", "#84def9", "#ffffff")}</div><p>关于体验、AI，或是一个有趣的想法</p><h2 id="contact-title"><a href="mailto:435456341@qq.com">一起聊聊</a></h2><div class="contact-email"><a href="mailto:435456341@qq.com">435456341@qq.com</a><button type="button" class="copy-email" data-copy-email aria-label="复制邮箱地址">复制邮箱</button><span data-copy-status role="status" aria-live="polite"></span></div></section>
</main>{footer}</body></html>'''
    (DIST / "index.html").write_text(html)
    # Case demos keep their original scripts and receive the third-edition shell.
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text().replace('content="#101210"', 'content="#f7f5ef"')
        page = page.replace('href="/favicon.svg"', 'href="/favicon-flower.svg"')
        page = re.sub(r'<link rel="stylesheet" href="/edition3\.css(?:\?[^"]*)?">', "", page)
        page = re.sub(r'<script src="/edition3\.js(?:\?[^"]*)?" defer></script>', "", page)
        page = re.sub(r'<header class="(?:site-header|e3-header)">.*?</header>', navigation, page, flags=re.S)
        page = re.sub(r'<footer class="(?:footer|e3-footer e3-wrap)">.*?</footer>', footer, page, flags=re.S)
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
        page += navigation + f'<main class="wrap detail" id="main"><a class="back-link" href="/#project-{slug}">返回作品</a><h1>{escape(project["title"])}</h1><p class="case-lead">{escape(project["summary"])}</p>{project_gallery(project, assets, figma_boards)}</main>' + footer + image_preview() + '</body></html>'
        (DIST / 'work' / f'{slug}.html').write_text(page)

    for index, slug in enumerate(PROJECT_ORDER):
        path = DIST / 'work' / f'{slug}.html'
        page = path.read_text()
        if slug == "ai-game":
            page = page.replace('class="edition-three e3-case"', 'class="edition-three e3-case e3-card-dark"')
            page = page.replace('</head>', '<link rel="stylesheet" href="/card-dark.css?v=taro-radial"></head>')
            page = page.replace('name="theme-color" content="#f7f5ef"', 'name="theme-color" content="#302a3b"')
            start = page.index('<div class="case-reading card-case-reading">')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + project_gallery(projects[slug], assets, figma_boards) + page[end:]
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
        path.write_text(add_button_blooms(path.read_text()))
    sitemap = DIST / "sitemap.xml"
    routes = ['/', '/resume.html'] + [f'/work/{slug}.html' for slug in VISIBLE_PROJECT_ORDER]
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{origin}{route}</loc></url>' for route in routes) + '</urlset>')
    (DIST / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    print('Built Edition 3 homepage, case navigation and site metadata.')


if __name__ == "__main__":
    build_edition3()
