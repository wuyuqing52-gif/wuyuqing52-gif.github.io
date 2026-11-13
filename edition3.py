"""Build the third portfolio edition using the existing case content."""
from html import escape
import json
from pathlib import Path
import re
from edition3_gallery import PROJECT_ORDER, selected_projects, project_gallery, image_preview


ROOT = Path(__file__).parent
DIST = ROOT / "dist"


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


HERO_FLOWER_PATHS = {
    "blue": (
        "M241 207 C210 157 188 100 202 55 C213 18 246 8 276 13 "
        "C321 5 349 28 361 70 C379 113 367 171 351 211 "
        "C411 173 473 151 527 172 C560 180 574 212 584 245 "
        "C605 282 586 319 552 346 C520 373 467 391 419 397 "
        "C449 436 470 474 459 514 C451 550 416 572 381 571 "
        "C343 584 302 545 279 505 C271 492 263 476 258 458 "
        "C267 514 238 544 197 566 C162 587 114 599 87 577 "
        "C55 549 40 510 48 473 C57 426 89 386 128 355 "
        "C86 367 40 370 14 342 C-2 322 5 284 12 257 "
        "C15 222 46 203 82 200 C142 192 199 203 241 207 Z"
    ),
    "red": (
        "M264 180 C241 133 215 82 226 40 C232 14 257 2 281 12 "
        "C318 26 340 106 348 175 C366 131 389 76 422 57 "
        "C444 42 470 46 476 66 C488 102 465 183 450 229 "
        "C489 202 532 168 562 177 C590 180 603 204 592 230 "
        "C579 270 524 301 478 323 C522 319 565 319 583 340 "
        "C605 364 593 393 571 405 C549 422 506 416 462 411 "
        "C498 438 538 480 529 516 C524 542 502 557 476 552 "
        "C438 546 403 493 378 457 C389 509 390 560 369 582 "
        "C350 603 322 602 303 583 C280 556 283 497 287 460 "
        "C266 503 239 554 206 564 C177 578 145 563 140 533 "
        "C129 497 160 449 181 417 C142 435 96 449 72 437 "
        "C45 426 37 402 49 379 C68 346 120 335 163 328 "
        "C109 309 51 283 30 254 C13 233 9 210 24 198 "
        "C46 180 110 201 166 225 C142 199 106 173 109 142 "
        "C110 119 130 103 151 107 C189 110 233 148 264 180 Z"
    ),
}

HERO_FLOWER_CENTERS = {
    "blue": "M269 259 C295 241 326 249 346 266 C368 282 373 313 360 339 C347 366 309 377 282 366 C254 358 237 331 241 304 C242 286 252 269 269 259 Z",
    "red": "M282 277 C303 262 334 271 352 290 C374 310 377 337 362 357 C346 379 322 382 295 370 C270 361 254 345 254 324 C250 305 264 286 282 277 Z",
}


def flower(kind):
    color, center = ("#84def9", "#0636ce") if kind == "blue" else ("#f32312", "#ffffff")
    return (
        f'<button class="flower flower-{kind}" data-flower data-start="{(-18 if kind == "blue" else 12)}" '
        'type="button" aria-label="让手绘花朵转起来">'
        '<span class="flower-art"><svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg" '
        'aria-hidden="true" focusable="false">'
        f'<path d="{HERO_FLOWER_PATHS[kind]}" fill="{color}" />'
        f'<path d="{HERO_FLOWER_CENTERS[kind]}" fill="{center}" /></svg></span></button>'
    )


def build_edition3():
    content = json.loads((ROOT / "content.json").read_text())
    origin = json.loads((ROOT / ".openai/hosting.json").read_text()).get("site_url", "https://yuki-edition-3.yuki3316950442.chatgpt.site")
    projects = selected_projects(content)
    assets = json.loads((ROOT / "edition3-assets.json").read_text())
    covers = {
        "dual-screen": ("dual-screen-02", "dual-screen-01"),
        "spring-gala": ("spring-gala-03", "spring-gala-05"),
        "game-link": ("game-link-05", "game-link-02"),
        "game-events": ("game-events-06", "game-events-01"),
    }
    by_name = {asset["name"]: asset for asset in assets}
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
    marks = {slug: project["title"] for slug, project in projects.items()}
    marks["ai-game"] = "卡牌游戏"
    marks["ai-review"] = "AI 走查"
    cards = []
    for index, slug in enumerate(PROJECT_ORDER):
        project = projects[slug]
        tile, petal, center, bloom = palettes[index]
        card_flower = flower_shape("blue", bloom, bloom).replace('</svg>', f'<circle cx="300" cy="300" r="190" fill="{bloom}" /></svg>')
        if slug == "ai-game":
            collage = '<div class="collage-main original-cover"><img src="/assets/ai-card-cover.png" alt="集换式卡牌游戏" loading="lazy"></div><div class="collage-small original-detail"><img src="/assets/card-case/figure-16.webp" alt="卡牌稀有度与视觉效果" loading="lazy"></div>'
        elif slug == "ai-review":
            collage = '<div class="collage-main original-cover"><img src="/assets/portfolio/review-cover.png" alt="AI 走查助手" loading="lazy"></div><div class="collage-small original-detail"><img src="/demos/review-assistant/design.png" alt="走查工具设计稿" loading="lazy"></div>'
        else:
            main, small = [by_name[name] for name in covers[slug]]
            src = main["parts"][0]["src"] if main["parts"] else main["src"]
            transparency = " has-alpha" if main.get("transparent") else ""
            collage = f'<div class="collage-main{transparency}"><img src="{src}" alt="{project["title"]}" loading="lazy" decoding="async"></div><div class="collage-small"><img src="{small["src"]}" alt="{project["title"]}" loading="lazy" decoding="async"></div>'
        cards.append(f'''<article class="e3-project-row project-{slug}" id="project-{slug}">
          <a class="e3-project" href="/work/{slug}.html" aria-describedby="summary-{slug}">
            <span class="card-bloom" aria-hidden="true">{card_flower}</span>
            <div class="project-collage" aria-hidden="true">{collage}</div>
            <div class="project-copy"><div class="project-caption"><h3>{escape(project['title'])}</h3><p>{escape(project['headline'])}</p></div><p class="project-description" id="summary-{slug}">{escape(project['summary'])}</p><span class="case-action" aria-hidden="true">查看案例</span></div>
          </a>
          <div class="project-side"><a class="flower-tile" href="/work/{slug}.html" data-flower data-start="-9" style="background:{tile}" aria-label="查看{escape(project['title'])}"><span class="flower-art">{flower_shape("blue", petal, center)}</span></a><a class="project-wordmark" href="/work/{slug}.html" aria-label="查看{escape(project['title'])}">{marks[slug]}</a></div>
        </article>''')
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f5ef"><title>Yuki · 吴雨晴｜体验与 AI 设计师</title>
<meta name="description" content="设计是我的起点，不是我的边界。吴雨晴的抖音 IP、游戏直播、AI 产品与设计工作流作品集。">
<meta property="og:title" content="Yuki · 吴雨晴｜体验与 AI 设计师"><meta property="og:type" content="website"><meta property="og:url" content="{origin}/"><meta property="og:image" content="{origin}/assets/ai-card-cover.png">
<link rel="canonical" href="{origin}/"><link rel="icon" href="/favicon-flower.svg" type="image/svg+xml"><link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script></head>
<body class="edition-three" id="top"><a class="e3-skip" href="#main">跳到主要内容</a>{navigation}
<main id="main"><section class="e3-hero" aria-labelledby="hero-title">
{flower('blue')}{flower('red')}
<div class="hero-copy"><h1 id="hero-title"><span class="hero-line">设计是我的起点，</span><span class="hero-line">不是我的<span class="hero-word">边界<i aria-hidden="true"></i></span></span></h1>
<p class="hero-intro">你好，我是 Yuki / 吴雨晴。</p>
<p class="hero-summary">一名以设计为起点、不设边界的设计师。既打磨复杂流程、系统框架与协作体验，也探索代码、视觉、与动态表达。</p>
<div class="hero-actions"><a class="e3-button" href="#work"><span>看看我的作品</span><span class="button-bloom" aria-hidden="true">{flower_shape("blue", "#0636ce", "#ffffff")}</span></a><a class="e3-text-link" href="/resume.html">我的简历</a></div></div>
<p class="flower-status visually-hidden" role="status" aria-live="polite"></p>
</section>
<section class="e3-work e3-wrap" id="work" aria-labelledby="work-title"><div class="section-intro"><h2 id="work-title">一些探索，一些认真。</h2></div><div class="e3-project-grid">{''.join(cards)}</div>
</section>
<section class="e3-about e3-wrap" id="about" aria-labelledby="about-title"><div class="about-heading"><p class="section-kicker">A LITTLE ABOUT ME</p><h2 id="about-title">设计之外，<br>还有<span class="serif-accent">好奇心。</span></h2><a class="e3-text-link" href="/resume.html">查看完整简历</a></div><div class="about-copy"><p class="about-lead">我喜欢把复杂的事情理清楚，<br>再把它做成可以体验的东西。</p><p>{escape(content['intro'])}</p><div class="expertise" aria-label="设计方向"><a href="/work/dual-screen.html">交互体验</a><a href="/work/ai-review.html">AI 工作流</a><a href="/work/ai-game.html">视觉与动态</a></div><ol class="about-career"><li><time>2021.04 — 至今</time><div><strong>字节跳动</strong><span>抖音 IP 与游戏 · 体验 / AI 设计</span></div></li><li><time>2020.12 — 2021.04</time><div><strong>拼多多</strong><span>用户增长 · 交互设计</span></div></li><li><time>2019.11 — 2020.12</time><div><strong>腾讯</strong><span>理财通 · 交互设计</span></div></li></ol></div></section>
<section class="e3-contact" id="contact" aria-labelledby="contact-title"><div class="contact-flower" aria-hidden="true">{flower_shape("blue", "#84def9", "#ffffff")}</div><p>关于体验、AI，或是一个有趣的想法</p><h2 id="contact-title"><a href="mailto:435456341@qq.com">一起聊聊</a></h2><div class="contact-email"><a href="mailto:435456341@qq.com">435456341@qq.com</a><button type="button" class="copy-email" data-copy-email aria-label="复制邮箱地址">复制邮箱</button><span data-copy-status role="status" aria-live="polite"></span></div></section>
</main>{footer}</body></html>'''
    (DIST / "index.html").write_text(html)
    # Case demos keep their original scripts and receive the third-edition shell.
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text().replace('content="#101210"', 'content="#f7f5ef"')
        page = page.replace('href="/favicon.svg"', 'href="/favicon-flower.svg"')
        page = page.replace('<link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script>', "")
        page = re.sub(r'<header class="(?:site-header|e3-header)">.*?</header>', navigation, page, flags=re.S)
        page = re.sub(r'<footer class="(?:footer|e3-footer e3-wrap)">.*?</footer>', footer, page, flags=re.S)
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script></head>')
        page = page.replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        (path).write_text(page)
    from site_base import head
    for slug in ("spring-gala", "game-link", "game-events"):
        project = projects[slug]
        page = head(project["title"] + ' · Yuki Design', project["summary"], '/work/' + slug + '.html').replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script></head>')
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page += navigation + f'<main class="wrap detail" id="main"><a class="back-link" href="/#project-{slug}">返回作品</a><h1>{escape(project["title"])}</h1><p class="case-lead">{escape(project["summary"])}</p>{project_gallery(project, assets)}</main>' + footer + image_preview() + '</body></html>'
        (DIST / 'work' / f'{slug}.html').write_text(page)

    for index, slug in enumerate(PROJECT_ORDER):
        path = DIST / 'work' / f'{slug}.html'
        page = path.read_text()
        if slug == "ai-game":
            start = page.index('<div class="case-reading card-case-reading">')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + project_gallery(projects[slug], assets) + page[end:]
        elif slug == "ai-review":
            start = page.index('<div class="case-reading">')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + page[end:]
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
        elif slug == "dual-screen":
            start = page.index('<section class="project-guide"')
            end = page.index('<a class="next-project"', start)
            page = page[:start] + project_gallery(projects[slug], assets) + page[end:]
            page = re.sub(r'<p class="case-lead">.*?</p>', '', page, flags=re.S)
        page = re.sub(r'<section class="case-assets">.*?</section>', '', page, flags=re.S)
        next_slug = PROJECT_ORDER[(index + 1) % len(PROJECT_ORDER)]
        next_link = f'<a class="next-project" href="/work/{next_slug}.html"><span>继续浏览</span><strong>{escape(projects[next_slug]["title"])}</strong></a>'
        if 'class="next-project"' in page:
            page = re.sub(r'<a class="next-project".*?</a>', next_link, page, flags=re.S)
        else:
            page = page.replace('</main>', next_link + '</main>')
        if 'id="art-lightbox"' not in page:
            page = page.replace('</body>', image_preview() + '</body>')
        path.write_text(page)
    sitemap = DIST / "sitemap.xml"
    routes = ['/', '/resume.html'] + [f'/work/{slug}.html' for slug in PROJECT_ORDER]
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{origin}{route}</loc></url>' for route in routes) + '</urlset>')
    (DIST / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    print('Built Edition 3 homepage, case navigation and site metadata.')


if __name__ == "__main__":
    build_edition3()
