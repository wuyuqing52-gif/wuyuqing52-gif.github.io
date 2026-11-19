"""Render the scrapbook-style portfolio homepage."""

from hashlib import sha256
from pathlib import Path

DIST = Path(__file__).parent / "dist"

FEATURED = (
    ("ai-game", "卡牌游戏产品设计", "从世界观到界面体验，打造沉浸式游戏产品", "游戏产品", "scrapbook/card-paper-cover", None),
    ("ai-review", "AI 设计助手", "让创作更高效，让灵感随时发生", "AI 工具", "scrapbook/review-paper-cover", None),
    ("dual-screen", "直播双屏项目", "打通内容与互动，探索新的直播体验", "直播体验", "edition3/dual-desktop", "edition3/dual-phone"),
    ("spring-gala", "抖音游戏新春会", "从创意策划到落地执行，打造节日氛围与用户互动", "活动设计", "edition3/spring-main", "edition3/spring-detail"),
    ("game-events", "游戏赛事", "围绕选手评分与自建赛，打磨观众参与和主播配置体验", "赛事体验", "edition3/events-desktop", "edition3/events-phone"),
)
EMAIL = "435456341@qq.com"


def icon(name):
    extension = "png" if name == "about" else "svg"
    return f'<img class="icon" src="/assets/scrapbook/{name}.{extension}" alt="" width="24" height="24">'


def asset_url(path):
    version = sha256((DIST / path).read_bytes()).hexdigest()[:12]
    return f"/{path}?v={version}"


def photo(name, caption, alt, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<figure class="polaroid polaroid-{name}">
      <img src="{asset_url(f'assets/scrapbook/{name}.webp')}" alt="{alt}" width="280" height="307" {loading} decoding="async">
      <figcaption>{caption}</figcaption>
    </figure>'''


def project_card(featured):
    slug, title, summary, category, cover, detail = featured
    detail_image = (
        f'\n            <img class="project-detail" src="/assets/{detail}.webp" alt="" loading="lazy" decoding="async">'
        if detail else ""
    )
    return f'''<article class="project" id="project-{slug}">
      <a class="project-link" href="/work/{slug}.html" aria-labelledby="title-{slug}" aria-describedby="summary-{slug}">
        <div class="project-folder">
          <div class="folder-tab">{category}</div>
          <div class="project-art" aria-hidden="true">
            <img class="project-main" src="/assets/{cover}.webp" alt="" loading="lazy" decoding="async">{detail_image}
          </div>
        </div>
        <div class="project-copy">
          <h3 id="title-{slug}">{title}</h3>
          <p id="summary-{slug}">{summary}</p>
        </div>
      </a>
    </article>'''


def render_navigation(active="top", *, home=False):
    prefix = "" if home else "/"
    current = ' aria-current="location"' if home else ' data-active'
    nav = "".join(
        f'<a href="{prefix}#{target}"{current if target == active else ""}>{icon(symbol)}<span>{label}</span></a>'
        for target, symbol, label in (
            ("top", "home", "HOME"), ("work", "work", "WORK"),
            ("about", "about", "ABOUT"), ("contact", "mail", "CONTACT"),
        )
    )
    return f'''<header class="site-header">
    <div class="header-inner">
      <a class="site-mark" href="{prefix}#top" aria-label="Yuki 首页"><span aria-hidden="true"></span></a>
      <nav class="main-nav" aria-label="主导航">{nav}</nav>
      <div class="header-shortcuts" aria-label="快捷入口">
        <a href="/resume.html" aria-label="查看简历" title="查看简历">{icon("resume")}</a>
        <a href="/work/ai-game.html#card-effects" aria-label="体验卡牌演示" title="体验卡牌演示">{icon("play")}</a>
        <a href="mailto:{EMAIL}" aria-label="发送邮件" title="发送邮件">{icon("mail")}</a>
      </div>
    </div>
  </header>'''


def render_footer(*, home=False):
    end = '<span>设计，让世界多一种可能。</span>' if home else '<a href="#top">回到顶部 ↑</a>'
    return f'<footer class="site-footer"><div class="wrap"><span>© 2026 YUKI</span>{end}</div></footer>'


def selection_controls():
    handles = "".join(
        f'<button class="frame-handle" type="button" data-resize="{direction}" '
        f'aria-label="{label}缩放文字" title="拖动缩放"></button>'
        for direction, label in (
            ("nw", "左上角"), ("n", "上边"), ("ne", "右上角"),
            ("w", "左边"), ("e", "右边"), ("sw", "左下角"),
            ("s", "下边"), ("se", "右下角"),
        )
    )
    corners = "".join(
        f'<button class="frame-rotate frame-rotate-{direction}" type="button" '
        f'data-rotate aria-label="{label}旋转文字" title="拖动旋转"></button>'
        for direction, label in (("nw", "左上角"), ("ne", "右上角"), ("sw", "左下角"), ("se", "右下角"))
    )
    return f'<span class="frame-handles">{handles}{corners}</span>'


def render_scrapbook(origin):
    cards = "".join(project_card(item) for item in FEATURED)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f7f6f1">
  <title>Yuki · 吴雨晴｜体验与 AI 设计师</title>
  <meta name="description" content="设计是我的起点，不是我的边界。吴雨晴的游戏、直播与 AI 作品集。">
  <meta property="og:title" content="Yuki · 吴雨晴｜体验与 AI 设计师">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{origin}/">
  <meta property="og:image" content="{origin}/assets/ai-card-cover.png">
  <link rel="canonical" href="{origin}/">
  <link rel="icon" href="/favicon-flower.svg" type="image/svg+xml">
  <link rel="preload" href="/assets/fonts/jersey-10.ttf" as="font" type="font/ttf" crossorigin>
  <link rel="stylesheet" href="{asset_url('scrapbook.css')}">
  <script src="{asset_url('scrapbook.js')}" defer></script>
</head>
<body id="top">
  <a class="skip" href="#main">跳到主要内容</a>
  {render_navigation(home=True)}
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-inner">
        {photo("coast", "Creative", "站在船边的 Yuki", True)}
        {photo("plant", "Design Life", "阳光下手中举起的银杏叶", True)}
        <div class="hero-notes"><span>HELLO, I’M</span><span>UI / PRODUCT DESIGNER</span></div>
        <div class="wordmark selection-frame" data-selection-frame>
          {selection_controls()}
          <h1 id="hero-title">YUKI</h1>
        </div>
        <div class="hero-stickers"><span>用设计</span><span>连接想象</span></div>
        <p class="hero-line"><span>设计是我的起点</span> <span>不是我的边界</span></p>
        <div class="work-slide">
          <span class="work-slide-label" aria-hidden="true">查看我的作品</span>
          <a class="work-slide-handle" href="#work" aria-label="查看我的作品" draggable="false">{icon("arrow")}</a>
        </div>
      </div>
    </section>
    <section class="work section" id="work" aria-labelledby="work-title">
      <div class="wrap">
        <div class="section-header">
          <span class="section-title">我的作品</span>
          <a class="section-link" href="/resume.html" aria-label="更多关于我，查看简历">MORE ABOUT ME {icon("arrow")}</a>
        </div>
        <h2 class="work-title" id="work-title">FEATURED WORKS</h2>
        <div class="projects">{cards}</div>
      </div>
    </section>
    <section class="about section" id="about" aria-labelledby="about-title">
      <div class="wrap">
        <div class="section-header">
          <h2 class="section-title" id="about-title">关于我</h2>
          <a class="section-link" href="/resume.html" aria-label="更多关于我，查看简历">MORE ABOUT ME {icon("arrow")}</a>
        </div>
        <div class="about-grid">
          {photo("portrait", "yuki", "坐在街边建筑前的 Yuki")}
          <div class="about-copy">
            <h3>我是一名产品设计师，<br>不设边界探索更多可能。</h3>
            <p>从用户需求出发，结合创意与技术，<br class="wide-break">在游戏、AI 工具和直播等领域探索更好的体验方式。<br class="wide-break">我相信设计能让想法落地，也能推动改变。</p>
            <ul class="skills" aria-label="设计方向"><li>UX设计</li><li>AI能力</li><li>用户研究</li><li>视觉设计</li></ul>
          </div>
        </div>
      </div>
    </section>
    <section class="contact section" id="contact" aria-labelledby="contact-title">
      <h2 class="section-title" id="contact-title">联系我</h2>
      <div class="contact-frame selection-frame" data-selection-frame>
        {selection_controls()}
        <p class="contact-wordmark" aria-hidden="true">CONTACT</p>
      </div>
      <p class="contact-line">一起把想法变成现实。</p>
      <a class="button contact-button" href="mailto:{EMAIL}">发送消息 {icon("arrow")}</a>
      <button class="copy-email" type="button" data-copy-email="{EMAIL}" hidden>复制邮箱 {icon("copy")}</button>
      <span class="copy-status" role="status"></span>
    </section>
  </main>
  {render_footer(home=True)}
</body>
</html>
'''
