"""Stitch the supplied screens into landscape portfolio boards."""
from collections import defaultdict
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


ROOT = Path(__file__).parent
DIST = ROOT / "dist"
PAPER = "#eeede6"


def paste_screen(canvas, source, box):
    image = source.copy().convert("RGBA")
    x, y, width, height = box
    image.thumbnail((width, height), Image.Resampling.LANCZOS)
    if image.width <= image.height:
        corners = Image.new("L", image.size)
        ImageDraw.Draw(corners).rounded_rectangle((0, 0, image.width - 1, image.height - 1), radius=24, fill=255)
        image.putalpha(ImageChops.multiply(image.getchannel("A"), corners))
    position = (round(x + (width - image.width) / 2), round(y + (height - image.height) / 2))
    canvas.alpha_composite(image, position)


def build_boards():
    assets = json.loads((ROOT / "edition3-assets.json").read_text())
    groups = defaultdict(list)
    for asset in assets:
        groups[(asset["project"], asset["label"] or "界面设计")].append(asset)
    output = DIST / "assets" / "edition3-projects" / "boards"
    output.mkdir(exist_ok=True)
    boards = []
    for (project, label), sources in groups.items():
        screens = []
        for source in sources:
            for part in source["parts"] or [source]:
                screens.append(Image.open(DIST / part["src"].lstrip("/")).convert("RGBA"))
        wide = [image for image in screens if image.width > image.height]
        phones = [image for image in screens if image.width <= image.height]
        width, height = (3200, 1600) if wide and phones else (3200, 1400)
        if not wide:
            total_ratio = sum(image.width / image.height for image in phones)
            content_width = total_ratio * 1160
            width = max(2200, min(3600, round(content_width + 36 * (len(phones) - 1) + 160)))
            height = round(min(1160, (width - 160 - 36 * (len(phones) - 1)) / total_ratio) + 160)
        elif not phones:
            width = 2400
        canvas = Image.new("RGBA", (width, height), PAPER)
        if wide and phones:
            row_height = 1440 / len(wide)
            for index, image in enumerate(wide):
                paste_screen(canvas, image, (80, 80 + index * row_height, 1750, row_height - 24))
            columns = min(2, len(phones))
            rows = (len(phones) + columns - 1) // columns
            for index, image in enumerate(phones):
                cell_width = 1210 / columns
                cell_height = 1440 / rows
                paste_screen(canvas, image, (1910 + index % columns * cell_width, 80 + index // columns * cell_height, cell_width - 24, cell_height - 24))
        elif phones:
            screen_height = 1160
            gap = 36
            ratios = [image.width / image.height for image in phones]
            screen_height = min(screen_height, (width - 160 - gap * (len(phones) - 1)) / sum(ratios))
            screen_widths = [round(ratio * screen_height) for ratio in ratios]
            x = (width - sum(screen_widths) - gap * (len(phones) - 1)) / 2
            for image, screen_width in zip(phones, screen_widths):
                paste_screen(canvas, image, (x, (height - screen_height) / 2, screen_width, screen_height))
                x += screen_width + gap
        else:
            cell_width = (width - 160) / len(wide)
            for index, image in enumerate(wide):
                paste_screen(canvas, image, (80 + index * cell_width, 80, cell_width - 24, height - 160))
        number = 1 + sum(board["project"] == project for board in boards)
        filename = f"{project}-{number:02d}.webp"
        canvas.convert("RGB").save(output / filename, "WEBP", quality=92, method=6)
        boards.append({"project": project, "label": label, "src": f"/assets/edition3-projects/boards/{filename}", "width": width, "height": height, "sources": [source["name"] for source in sources]})
    (ROOT / "edition3-boards.json").write_text(json.dumps(boards, ensure_ascii=False, indent=2) + "\n")
    print(f"Built {len(boards)} landscape boards from {len(assets)} supplied images.")


if __name__ == "__main__":
    build_boards()
