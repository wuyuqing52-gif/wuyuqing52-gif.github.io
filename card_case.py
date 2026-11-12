"""Render the AI card game retrospective from the Keynote source copy."""
from html import escape
import json
from pathlib import Path


def render_block(block):
    kind = block["type"]
    if kind == "details":
        content = "".join(render_block(item) for item in block["blocks"])
        return f'<details class="card-case-details"><summary>{escape(block["label"])}</summary><div class="card-case-column">{content}</div></details>'
    if kind == "diagram":
        items = []
        for item in block["items"]:
            label = f'<small>{escape(item["label"])}</small>' if item.get("label") else ""
            body = f'<p>{escape(item["body"])}</p>' if item.get("body") else ""
            output = f'<span class="card-case-output">产出 · {escape(item["output"])}</span>' if item.get("output") else ""
            items.append(f'<li>{label}<strong>{escape(item["title"])}</strong>{body}{output}</li>')
        style = escape(block.get("style", "flow"))
        return f'<ol class="card-case-diagram is-{style}">{"".join(items)}</ol>'
    if kind == "rounds":
        items = []
        for item in block["items"]:
            turns = []
            for turn in item["turns"]:
                speaker = turn["speaker"]
                actor = "我" if speaker == "me" else "AI · Claude"
                body = f'<p>{escape(turn["body"])}</p>' if turn["body"] else ""
                choices = "".join(f'<li>{escape(choice)}</li>' for choice in turn["choices"])
                if choices:
                    choices = f'<ul class="card-case-choices">{choices}</ul>'
                turns.append(
                    f'<div class="card-case-turn is-{speaker}"><small>{actor} / {escape(turn["label"])}</small>'
                    f'<h4>{escape(turn["title"])}</h4>{body}{choices}</div>'
                )
            items.append(f'<li><h4>{escape(item["round"])}</h4><div class="card-case-turns">{"".join(turns)}</div></li>')
        return f'<ol class="card-case-rounds">{"".join(items)}</ol>'
    if kind in {"feature", "group", "split"}:
        columns = [
            '<div class="card-case-column">' + "".join(render_block(item) for item in column) + '</div>'
            for column in block["columns"]
        ]
        layout = f' card-case-{escape(block["layout"])}' if block.get("layout") else ""
        return f'<div class="card-case-group is-{kind}{layout}">{"".join(columns)}</div>'
    if kind == "heading":
        return f'<h3>{escape(block["text"])}</h3>'
    if kind == "prose":
        return "".join(f'<p class="card-case-prose">{escape(p)}</p>' for p in block["paragraphs"])
    if kind == "callout":
        label = f'<h4>{escape(block["title"])}</h4>' if block["title"] else ""
        return f'<aside class="card-case-callout">{label}<p>{escape(block["text"])}</p></aside>'
    if kind in {"cards", "steps", "facts"}:
        tag = "ol" if kind == "steps" else "ul"
        items = []
        for item in block["items"]:
            body = f'<p>{escape(item["body"])}</p>' if item["body"] else ""
            items.append(f'<li><strong>{escape(item["title"])}</strong>{body}</li>')
        return f'<{tag} class="card-case-cards is-{kind}">{"".join(items)}</{tag}>'
    if kind == "media":
        figures = []
        for item in block["items"]:
            src, caption = escape(item["src"]), escape(item["caption"])
            figures.append(
                f'<figure><a href="{src}" target="_blank" rel="noopener">'
                f'<img src="{src}" alt="{caption}" width="{item["width"]}" height="{item["height"]}" loading="lazy" decoding="async"></a>'
                f'<figcaption>{caption}</figcaption></figure>'
            )
        return f'<div class="card-case-media" data-columns="{block["columns"]}">{"".join(figures)}</div>'
    if kind == "jump":
        return f'<a class="text-link card-case-jump" href="{escape(block["href"])}">{escape(block["label"])} ↑</a>'
    raise ValueError(f"Unknown card case block: {kind}")


def render_card_case():
    chapters = json.loads(Path(__file__).with_name("card-case.json").read_text(encoding="utf-8"))
    links, sections = [], []
    for index, chapter in enumerate(chapters):
        anchor, title = escape(chapter["id"]), escape(chapter["title"])
        links.append(f'<li><a href="#{anchor}"><span>{index:02}</span>{title}</a></li>')
        sections.append(
            f'<section class="case-chapter card-case-chapter" id="{anchor}" data-case-chapter>'
            f'<header class="chapter-heading"><span aria-hidden="true">{index:02}</span><h2>{title}</h2></header>'
            '<div class="card-case-body">' + "".join(render_block(block) for block in chapter["blocks"])
            + '</div></section>'
        )
    return (
        '<div class="case-reading card-case-reading"><nav class="case-contents" aria-label="卡牌案例目录">'
        '<span class="eyebrow">案例复盘 / CONTENTS</span><ol>' + "".join(links) + '</ol></nav>'
        '<article aria-label="AI 卡牌游戏设计项目案例复盘">' + "".join(sections) + '</article></div>'
    )
