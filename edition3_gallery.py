"""Compose the document's project artwork and shared image preview."""
from html import escape
from math import ceil


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
    return '''<dialog class="art-lightbox" id="art-lightbox" aria-label="图片预览">
    <button class="art-close" type="button" data-close-artwork aria-label="关闭图片预览"><span class="art-close-icon" aria-hidden="true"></span></button>
    <div class="art-lightbox-scroll"><img alt=""></div></dialog>'''


def screen_link(project, asset):
    caption = f'{project["title"]} · {asset["label"] or "界面设计"}'
    shape = "desktop" if asset.get("display_bounds") else "image"
    style = ""
    if shape == "desktop":
        x, y, width, height = asset["display_bounds"]
        style = f' style="aspect-ratio:{width} / {height};--screen-width:{asset["width"] / width * 100:.6f}%;--screen-left:{-x / width * 100:.6f}%;--screen-top:{-y / height * 100:.6f}%"'
    return f'<a class="study-screen study-screen--{shape}"{style} href="{asset["src"]}" data-image-preview data-image-title="{escape(caption)}" aria-label="放大{escape(caption)}"><img src="{asset["src"]}" alt="{escape(caption)}" width="{asset["width"]}" height="{asset["height"]}" loading="lazy" decoding="async"></a>'


def study_surface(project, images, kind):
    screens = ''.join(screen_link(project, asset) for asset in images)
    tracks = ' '.join(f'minmax(0, {asset["width"] / asset["height"]:.6f}fr)' for asset in images)
    return f'<div class="event-study study--{kind}" style="--study-tracks:{tracks}">{screens}</div>'


def event_gallery(project, assets):
    groups = {}
    for asset in assets:
        if asset["project"] == "game-events":
            groups.setdefault(asset["label"], []).append(asset)
    sections = []
    for label, images in groups.items():
        kind = "score" if label == "选手评分" else "tournament"
        phones = []
        desktops = []
        for asset in images:
            shape = "desktop" if asset["width"] > asset["height"] else "phone"
            screen = screen_link(project, asset)
            (desktops if shape == "desktop" else phones).append(screen)
        desktop_stack = '<div class="study-desktops">' + ''.join(desktops) + '</div>' if desktops else ''
        sections.append(f'<section class="art-gallery-group"><h2>{escape(label)}</h2><div class="event-study event-study--{kind}">{desktop_stack}{"".join(phones)}</div></section>')
    return '<div class="art-gallery">' + ''.join(sections) + '</div>'


def project_gallery(project, assets):
    if project["slug"] == "game-events":
        return event_gallery(project, assets)
    groups = {}
    for asset in assets:
        if asset["project"] == project["slug"]:
            groups.setdefault(asset["label"] or "界面设计", []).append(asset)
    sections = []
    for label, images in groups.items():
        surfaces = []
        if project["slug"] == "dual-screen":
            desktops = ''.join(screen_link(project, asset) for asset in images if asset.get("display_bounds"))
            phones = ''.join(screen_link(project, asset) for asset in images if not asset.get("display_bounds"))
            surfaces.append(f'<div class="event-study study--dual"><div class="study-desktops">{desktops}</div>{phones}</div>')
        elif project["slug"] == "game-link":
            desktops = [asset for asset in images if asset.get("display_bounds")]
            phones = [asset for asset in images if not asset.get("display_bounds")]
            surfaces.append(study_surface(project, desktops, "desktop"))
            surfaces.extend(study_surface(project, phones[index:index + 2], "pair") for index in range(0, len(phones), 2))
        else:
            short_images = []
            for asset in images:
                if asset["parts"]:
                    # Keep each long page's consecutive sections together.
                    parts = [dict(part, label=label) for part in asset["parts"]]
                    row_size = ceil(len(parts) / ceil(len(parts) / 4))
                    surfaces.extend(study_surface(project, parts[index:index + row_size], "phones") for index in range(0, len(parts), row_size))
                else:
                    short_images.append(asset)
            if short_images:
                kind = "wide" if short_images[0]["width"] > short_images[0]["height"] else "pair"
                surfaces.append(study_surface(project, short_images, kind))
        sections.append(f'<section class="art-gallery-group"><h2>{escape(label)}</h2>{"".join(surfaces)}</section>')
    return f'<div class="art-gallery art-gallery--{project["slug"]}">' + ''.join(sections) + '</div>' if sections else ""
