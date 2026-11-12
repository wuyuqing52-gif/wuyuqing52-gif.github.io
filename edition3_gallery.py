"""Compose the document's project artwork and shared image preview."""
from html import escape


PROJECT_ORDER = ("ai-game", "ai-review", "dual-screen", "spring-gala", "game-link", "game-events")


def selected_projects(content):
    projects = {project["slug"]: project for project in content["projects"]}
    projects.update({
        "spring-gala": {
            "slug": "spring-gala", "title": "抖音游戏新春会",
            "headline": "跨界参与强视觉运营活动设计",
            "summary": "独立负责年度作者活动页设计，深度参与新春会主会场“抓马”打投榜单、许愿池等设计工作。",
        },
        "game-link": {
            "slug": "game-link", "title": "游戏连屏",
            "headline": "连接主播、另一位主播与观众",
            "summary": "连接主播、另一位主播与观众，打磨从发起、接受、配置到结束的完整玩法体验。",
        },
        "game-events": {
            "slug": "game-events", "title": "游戏赛事",
            "headline": "选手评分与自建赛",
            "summary": "围绕选手评分与自建赛，呈现观众参与和主播配置的赛事体验。",
        },
    })
    return {slug: projects[slug] for slug in PROJECT_ORDER}


def image_preview():
    return '''<dialog class="art-lightbox" id="art-lightbox" aria-labelledby="art-lightbox-title">
    <header><p id="art-lightbox-title"></p><button type="button" data-close-artwork aria-label="关闭图片预览">×</button></header>
    <div class="art-lightbox-scroll"><img alt=""></div></dialog>'''


def project_gallery(project, boards):
    sections = []
    for board in boards:
        if board["project"] != project["slug"]:
            continue
        caption = f'{project["title"]} · {board["label"]}'
        sections.append(f'''<section class="art-gallery-group"><h2>{escape(board["label"])}</h2><a class="art-board" href="{board['src']}" data-image-preview data-image-title="{escape(caption)}" aria-label="放大{escape(caption)}"><img src="{board['src']}" alt="{escape(caption)} · 多页面组合展示" width="{board['width']}" height="{board['height']}" loading="lazy" decoding="async"></a></section>''')
    return '<div class="art-gallery">' + ''.join(sections) + '</div>' if sections else ""
