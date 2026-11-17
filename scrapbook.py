"""Render the scrapbook-style portfolio homepage."""

from html import escape

FEATURED = (
    ("ai-game", ("卡牌游戏", "产品设计"), ("从世界观到界面体验", "打造沉浸式游戏产品"), "card-cover", "card-detail"),
    ("ai-review", ("AI 设计助手",), ("让创作更高效", "让灵感随时发生"), "review-cover", "review-detail"),
    ("dual-screen", ("直播双屏项目",), ("打通内容与互动", "探索新的直播体验"), "dual-desktop", "dual-phone"),
    ("spring-gala", ("抖音游戏新春会",), ("从创意策划到落地执行", "打造节日氛围与用户互动"), "spring-main", "spring-detail"),
)
ARCHIVE = (
    ("game-events", "抖音游戏赛事"),
    ("licaitong", "理财通产品体验设计"),
)
EMAIL = "435456341@qq.com"


def icon(name):
    extension = "png" if name == "about" else "svg"
    return f'<img class="icon" src="/assets/scrapbook/{name}.{extension}" alt="" width="24" height="24">'


def photo(name, caption, alt, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'''<figure class="polaroid polaroid-{name}">
      <img src="/assets/scrapbook/{name}.webp" alt="{alt}" width="280" height="307" {loading} decoding="async">
      <figcaption>{caption}</figcaption>
    </figure>'''


def project_row(index, featured):
    slug, title, summary, cover, detail = featured
    title_html = "<br>".join(title)
    summary_html = ' '.join(f"<span>{line}</span>" for line in summary)
    return f'''<article class="project" id="project-{slug}">
      <a class="project-link" href="/work/{slug}.html" aria-labelledby="title-{slug}" aria-describedby="summary-{slug}">
        <div class="project-copy">
          <span class="project-number" aria-hidden="true">{index:02}</span>
          <h3 id="title-{slug}">{title_html}</h3>
          <p id="summary-{slug}">{summary_html}</p>
          <span class="project-arrow">{icon("arrow")}</span>
        </div>
        <div class="project-art" aria-hidden="true">
          <span class="paper-panel"></span><span class="paper-block"></span><span class="paper-accent"></span>
          <img class="project-main" src="/assets/edition3/{cover}.webp" alt="" loading="lazy" decoding="async">
          <img class="project-detail" src="/assets/edition3/{detail}.webp" alt="" loading="lazy" decoding="async">
        </div>
      </a>
    </article>'''


def render_scrapbook(origin, projects):
    current = ' aria-current="location"'
    nav = "".join(
        f'<a href="#{target}"{current if target == "top" else ""}>{icon(symbol)}<span>{label}</span></a>'
        for target, symbol, label in (
            ("top", "home", "HOME"), ("work", "work", "WORK"),
            ("about", "about", "ABOUT"), ("contact", "mail", "CONTACT"),
        )
    )
    rows = "".join(project_row(index, item) for index, item in enumerate(FEATURED, 1))
    archived = "".join(
        f'<li id="project-{slug}"><a href="/work/{slug}.html">{escape(projects.get(slug, {}).get("title", title))}{icon("arrow")}</a></li>'
        for slug, title in ARCHIVE
    )
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
  <link rel="stylesheet" href="/scrapbook.css">
  <script src="/scrapbook.js" defer></script>
</head>
<body id="top">
  <a class="skip" href="#main">跳到主要内容</a>
  <header class="site-header">
    <div class="header-inner">
      <a class="site-mark" href="#top" aria-label="Yuki 首页"><span aria-hidden="true"></span></a>
      <nav class="main-nav" aria-label="主导航">{nav}</nav>
      <div class="header-shortcuts" aria-label="快捷入口">
        <a href="/resume.html" aria-label="查看简历" title="查看简历">{icon("resume")}</a>
        <a href="/work/ai-game.html#card-effects" aria-label="体验卡牌演示" title="体验卡牌演示">{icon("play")}</a>
        <a href="mailto:{EMAIL}" aria-label="发送邮件" title="发送邮件">{icon("mail")}</a>
      </div>
    </div>
  </header>
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-inner">
        {photo("coast", "Creative", "海边暮色中的人物侧影", True)}
        {photo("plant", "Design Life", "窗边绿植和斜照的阳光", True)}
        <div class="hero-notes"><span>HELLO, I’M</span><span>UI / PRODUCT DESIGNER</span></div>
        <div class="wordmark">
          <span class="frame-handles" aria-hidden="true">{'<i></i>' * 8}</span>
          <h1 id="hero-title">YUKI</h1>
        </div>
        <div class="hero-stickers"><span>用设计</span><span>连接想象</span></div>
        <p class="hero-line"><span>设计是我的起点</span> <span>不是我的边界</span></p>
        <a class="button hero-button" href="#work"><span class="button-tile">{icon("arrow")}</span>查看我的作品</a>
      </div>
    </section>
    <section class="work section" id="work" aria-labelledby="work-title">
      <div class="wrap">
        <div class="section-header">
          <h2 class="section-title" id="work-title">我的作品</h2>
          <a class="section-link" href="#all-work">查看全部 {icon("arrow")}</a>
        </div>
        <div class="projects">{rows}</div>
        <details class="work-archive" id="all-work">
          <summary>更多作品 {icon("arrow")}</summary>
          <ul>{archived}</ul>
        </details>
      </div>
    </section>
    <section class="about section" id="about" aria-labelledby="about-title">
      <div class="wrap">
        <div class="section-header">
          <h2 class="section-title" id="about-title">关于我</h2>
          <a class="section-link" href="/resume.html" aria-label="更多关于我，查看简历">MORE ABOUT ME {icon("arrow")}</a>
        </div>
        <div class="about-grid">
          {photo("portrait", "yuki", "戴黄色帽子的人望向远处")}
          <div class="about-copy">
            <h3>我是一名产品设计师，<br>专注于用设计解决真实问题。</h3>
            <p>从用户需求出发，结合创意与技术，<br class="wide-break">在游戏、AI 工具和直播等领域探索更好的体验方式。<br class="wide-break">我相信设计能让想法落地，也能推动改变。</p>
            <ul class="skills" aria-label="设计方向"><li>产品设计</li><li>交互设计</li><li>用户研究</li><li>创意策划</li></ul>
          </div>
        </div>
      </div>
    </section>
    <section class="contact section" id="contact" aria-labelledby="contact-title">
      <h2 class="section-title" id="contact-title">联系我</h2>
      <p class="contact-wordmark" aria-hidden="true">CONTACT</p>
      <p class="contact-line">一起把想法变成现实。</p>
      <a class="button contact-button" href="mailto:{EMAIL}">发送消息 {icon("arrow")}</a>
      <button class="copy-email" type="button" data-copy-email="{EMAIL}" hidden>复制邮箱 {icon("copy")}</button>
      <span class="copy-status" role="status"></span>
    </section>
  </main>
  <footer class="site-footer"><div class="wrap"><span>© 2026 YUKI</span><span>设计，让世界多一种可能。</span></div></footer>
</body>
</html>
'''
