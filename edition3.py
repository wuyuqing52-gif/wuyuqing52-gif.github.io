"""Build the third portfolio edition using the existing case content."""
from html import escape
import json
from pathlib import Path
import re


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


def flower(kind):
    color, center = ("#84def9", "#0636ce") if kind == "blue" else ("#f32312", "#ffffff")
    return (
        f'<button class="flower flower-{kind}" data-flower data-start="{(-18 if kind == "blue" else 12)}" '
        'type="button" aria-label="让手绘花朵转起来">'
        f'<span class="flower-art">{flower_shape(kind, color, center)}</span></button>'
    )


def build_edition3():
    content = json.loads((ROOT / "content.json").read_text())
    origin = json.loads((ROOT / ".openai/hosting.json").read_text()).get("site_url", "https://yuki-edition-3.yuki3316950442.chatgpt.site")
    projects = {project["slug"]: project for project in content["projects"]}
    covers = {
        "ai-game": ("/assets/ai-card-cover.png", "卡牌游戏的抽卡与卡牌详情界面"),
        "ai-review": ("/assets/portfolio/review-cover.png", "AI 走查助手的网页工具与 Figma 插件"),
        "ip-worldbook": ("/assets/portfolio/worldbook-preview.webp", "IP 世界书的产品界面"),
        "ai-editor": ("/assets/portfolio/desk-editor.png", "AI 游戏编辑器主题示意"),
        "dual-screen": ("/assets/portfolio/desk-livestream.png", "直播双屏主题示意"),
    }
    navigation = '''<header class="e3-header"><nav class="e3-nav" aria-label="主导航"><a class="nav-link" href="/#work">作品</a><a class="e3-brand" href="/" aria-label="Yuki 第三版首页">yuki<span>.</span></a><a class="nav-link" href="/#about">关于我</a></nav></header>'''
    footer = f'''<footer class="e3-footer e3-wrap"><a class="e3-brand" href="/">yuki<span>.</span></a><p>© 2026 吴雨晴</p><div class="edition-links" aria-label="其他作品集版本"><a href="https://yuki-design.yuki3316950442.chatgpt.site/">深色版</a><a href="https://yuki-design-studio.yuki3316950442.chatgpt.site/">年轻版</a><a href="#top">回到顶部</a></div></footer>'''
    secondary = {
        "ai-game": ("/assets/card-case/figure-16.webp", "卡牌稀有度与视觉效果"),
        "ai-review": ("/demos/review-assistant/design.png", "AI 走查助手的手机设计稿"),
        "ip-worldbook": ("/assets/card-case/figure-01.webp", "IP 世界书产品界面"),
        "ai-editor": ("/assets/portfolio/desk-code.png", "游戏编辑器主题示意"),
        "dual-screen": ("/assets/portfolio/desk-game.png", "游戏直播主题示意"),
    }
    palettes = [
        ("#0636ce", "#ffd23c", "#f32312", "#ffcf4c"),
        ("#ff8fca", "#0636ce", "#ffffff", "#ff8fca"),
        ("#ffcf4c", "#f32312", "#ffffff", "#84def9"),
        ("#84def9", "#0636ce", "#ffffff", "#ffcf4c"),
        ("#f32312", "#ffcf4c", "#0636ce", "#ff8fca"),
    ]
    marks = {"ai-game": "卡牌游戏", "ai-review": "AI 走查", "ip-worldbook": "IP 世界书", "ai-editor": "游戏编辑器", "dual-screen": "直播双屏"}
    cards = []
    for index, slug in enumerate(("ai-game", "ai-review", "ip-worldbook", "ai-editor", "dual-screen")):
        project = projects[slug]
        src, alt = covers[slug]
        small_src, small_alt = secondary[slug]
        tile, petal, center, bloom = palettes[index]
        illustration = '<span class="image-note">主题示意</span>' if slug in {"ai-editor", "dual-screen"} else ""
        cards.append(f'''<article class="e3-project-row project-{slug}" id="project-{slug}">
          <a class="e3-project" href="/work/{slug}.html" aria-describedby="summary-{slug}">
            <span class="card-bloom" aria-hidden="true">{flower_shape("blue", bloom, bloom)}</span>
            <div class="project-collage" aria-hidden="true"><div class="collage-main"><img src="{src}" alt="{alt}" loading="lazy" decoding="async"></div><div class="collage-small"><img src="{small_src}" alt="{small_alt}" loading="lazy" decoding="async"></div>{illustration}</div>
            <div class="project-copy"><div class="project-caption"><h3>{escape(project['title'])}</h3><p>{escape(project['headline'])}</p></div><p class="project-description" id="summary-{slug}">{escape(project['summary'])}</p><span class="case-action" aria-hidden="true">查看案例</span></div>
          </a>
          <div class="project-side"><a class="flower-tile" href="/work/{slug}.html" data-flower data-start="-9" style="background:{tile}" aria-label="查看{escape(project['title'])}"><span class="flower-art">{flower_shape("blue", petal, center)}</span></a><a class="project-wordmark" href="/work/{slug}.html" aria-label="查看{escape(project['title'])}">{marks[slug]}</a></div>
        </article>''')
    slides = []
    for slug in ("ai-game", "ai-review", "ip-worldbook", "ai-editor"):
        src, alt = covers[slug]
        slides.append(f'<a class="peek-slide peek-{slug}" href="/work/{slug}.html" aria-label="查看{projects[slug]["title"]}"><img src="{src}" alt="{alt}" loading="lazy"></a>')
    slide_markup = "".join(slides)
    clone_markup = slide_markup.replace('<a ', '<a tabindex="-1" ')
    gallery = f'<div class="peek-gallery" aria-label="项目速览，悬停或聚焦时暂停"><div class="peek-track"><div class="peek-group">{slide_markup}</div><div class="peek-group" aria-hidden="true" inert>{clone_markup}</div></div></div>'
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#f7f5ef"><title>Yuki · 吴雨晴｜体验与 AI 设计师</title>
<meta name="description" content="设计是我的起点，不是我的边界。吴雨晴的抖音 IP、游戏直播、AI 产品与设计工作流作品集。">
<meta property="og:title" content="Yuki · 吴雨晴｜体验与 AI 设计师"><meta property="og:type" content="website"><meta property="og:url" content="{origin}/"><meta property="og:image" content="{origin}/assets/ai-card-cover.png">
<link rel="canonical" href="{origin}/"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script></head>
<body class="edition-three" id="top"><a class="e3-skip" href="#main">跳到主要内容</a>{navigation}
<main id="main"><section class="e3-hero" aria-labelledby="hero-title">
{flower('blue')}{flower('red')}
<div class="hero-copy"><p class="hero-intro">你好，我是 Yuki / 吴雨晴。</p>
<h1 id="hero-title">设计是我的起点，<br>不是我的<span class="hero-word">边界<i aria-hidden="true"></i></span></h1>
<p class="hero-summary">一名以设计为起点、不设边界的设计师。既打磨复杂流程、系统框架与协作体验，也探索代码、视觉、与动态表达。</p>
<div class="hero-actions"><a class="e3-button" href="#work"><span>看看我的作品</span><span class="button-bloom" aria-hidden="true">{flower_shape("blue", "#0636ce", "#ffffff")}</span></a><a class="e3-text-link" href="/resume.html">我的简历</a></div></div>
<p class="flower-status visually-hidden" role="status" aria-live="polite"></p>
</section>{gallery}
<section class="e3-work e3-wrap" id="work" aria-labelledby="work-title"><div class="section-intro"><h2 id="work-title">一些探索，一些认真。</h2><p>围绕真实的问题，寻找合适的设计。<br>这是我在体验、AI 与游戏之间的实践。</p></div><div class="e3-project-grid">{''.join(cards)}</div>
<a class="earlier-project" id="project-licaitong" href="/work/licaitong.html"><span>更早的设计实践</span><strong>理财通产品体验设计</strong><span class="earlier-label">查看概览</span></a></section>
<section class="e3-about e3-wrap" id="about" aria-labelledby="about-title"><div class="about-heading"><p class="section-kicker">A LITTLE ABOUT ME</p><h2 id="about-title">设计之外，<br>还有<span class="serif-accent">好奇心。</span></h2><a class="e3-text-link" href="/resume.html">查看完整简历</a></div><div class="about-copy"><p class="about-lead">我喜欢把复杂的事情理清楚，<br>再把它做成可以体验的东西。</p><p>{escape(content['intro'])}</p><div class="expertise" aria-label="设计方向"><a href="/work/dual-screen.html">交互体验</a><a href="/work/ai-review.html">AI 工作流</a><a href="/work/ai-game.html">视觉与动态</a></div><ol class="about-career"><li><time>2021.04 — 至今</time><div><strong>字节跳动</strong><span>抖音 IP 与游戏 · 体验 / AI 设计</span></div></li><li><time>2020.12 — 2021.04</time><div><strong>拼多多</strong><span>用户增长 · 交互设计</span></div></li><li><time>2019.11 — 2020.12</time><div><strong>腾讯</strong><span>理财通 · 交互设计</span></div></li></ol></div></section>
<section class="e3-contact" id="contact" aria-labelledby="contact-title"><div class="contact-flower" aria-hidden="true">{flower_shape("blue", "#84def9", "#ffffff")}</div><p>关于体验、AI，或是一个有趣的想法</p><h2 id="contact-title"><a href="mailto:435456341@qq.com">一起聊聊</a></h2><div class="contact-email"><a href="mailto:435456341@qq.com">435456341@qq.com</a><button type="button" class="copy-email" data-copy-email aria-label="复制邮箱地址">复制邮箱</button><span data-copy-status role="status" aria-live="polite"></span></div></section>
</main>{footer}</body></html>'''
    (DIST / "index.html").write_text(html)
    # Case demos keep their original scripts and receive the third-edition shell.
    for path in [*sorted((DIST / "work").glob("*.html")), DIST / "resume.html", DIST / "404.html"]:
        page = path.read_text().replace('content="#101210"', 'content="#f7f5ef"')
        page = page.replace('<link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script>', "")
        page = re.sub(r'<header class="(?:site-header|e3-header)">.*?</header>', navigation, page, flags=re.S)
        page = re.sub(r'<footer class="(?:footer|e3-footer e3-wrap)">.*?</footer>', footer, page, flags=re.S)
        page = page.replace('<body id="top">', '<body id="top" class="edition-three e3-case">')
        page = page.replace('</head>', '<link rel="stylesheet" href="/edition3.css"><script src="/edition3.js" defer></script></head>')
        page = page.replace('https://yuki-design.yuki3316950442.chatgpt.site', origin)
        # Keep edition switchers pointed at the original published sites.
        page = page.replace(f'<a href="{origin}/">深色版</a>', '<a href="https://yuki-design.yuki3316950442.chatgpt.site/">深色版</a>')
        (path).write_text(page)
    sitemap = DIST / "sitemap.xml"
    sitemap.write_text(sitemap.read_text().replace('https://yuki-design.yuki3316950442.chatgpt.site', origin))
    (DIST / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
    print('Built Edition 3 homepage, case navigation and site metadata.')


if __name__ == "__main__":
    build_edition3()
