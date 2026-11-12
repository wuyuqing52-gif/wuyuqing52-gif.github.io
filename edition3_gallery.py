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


def project_gallery(project, assets):
    groups = {}
    for asset in assets:
        if asset["project"] == project["slug"]:
            groups.setdefault(asset["label"] or "界面设计", []).append(asset)
    sections = []
    for label, images in groups.items():
        pieces = []
        for asset in images:
            for index, image in enumerate(asset["parts"] or [asset]):
                shape = "wide" if image["width"] > image["height"] else "portrait"
                caption = f'{project["title"]} · {label}'
                alt = caption + (f' · 分段 {index + 1}' if asset["parts"] else "")
                pieces.append((shape, f'''<a class="art-piece is-{shape}" href="{asset['src']}" data-image-preview data-image-title="{escape(caption)}" aria-label="放大{escape(alt)}"><img src="{image['src']}" alt="{escape(alt)}" width="{image['width']}" height="{image['height']}" loading="lazy" decoding="async"></a>'''))
        shapes = {shape for shape, _ in pieces}
        kind = "mixed" if len(shapes) == 2 else "boards" if "wide" in shapes else "phones"
        if kind == "phones":
            count = min(4, len(pieces))
            columns = ['<div class="art-column">' + ''.join(piece for _, piece in pieces[i::count]) + '</div>' for i in range(count)]
            markup = ''.join(columns)
        else:
            count = 4
            markup = ''.join(piece for _, piece in sorted(pieces, key=lambda item: item[0] != "wide"))
        sections.append(f'<section class="art-gallery-group"><h2>{escape(label)}</h2><div class="art-stage art-stage--{kind}" style="--art-columns:{count}">{markup}</div></section>')
    return '<div class="art-gallery">' + ''.join(sections) + '</div>' if sections else ""
