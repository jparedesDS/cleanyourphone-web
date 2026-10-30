#!/usr/bin/env python3
"""Generate the banner and Open Graph images.

Requires Pillow (`python -m pip install pillow`). The site itself does not use Pillow.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SCALE = 2

INK = (6, 16, 20)
INK_2 = (8, 22, 26)
TEXT = (238, 248, 245)
MUTED = (157, 180, 176)
MUTED_2 = (111, 137, 133)
ACCENT = (100, 244, 196)
ACCENT_2 = (94, 200, 255)
WARM = (255, 184, 107)
TILE_COLORS = [
    (74, 222, 128), (96, 165, 250), (129, 140, 248), (244, 114, 182),
    (52, 211, 153), (56, 189, 248), (251, 191, 36), (52, 211, 153),
    (148, 163, 184), (142, 232, 224), (94, 200, 255), (100, 244, 196),
    (255, 212, 121), (246, 166, 193), (195, 181, 255), (158, 240, 168),
]


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    candidates = []
    if mono:
        candidates += [r"C:\Windows\Fonts\consolab.ttf", r"C:\Windows\Fonts\consola.ttf",
                        "/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"]
    elif bold:
        candidates += [r"C:\Windows\Fonts\segoeuib.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    else:
        candidates += [r"C:\Windows\Fonts\segoeui.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def base_canvas(width: int, height: int) -> Image.Image:
    image = Image.new("RGB", (width * SCALE, height * SCALE), INK)
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse(
        (int(width * SCALE * 0.55), int(-height * SCALE * 0.5),
         int(width * SCALE * 1.1), int(height * SCALE * 0.7)),
        fill=(*ACCENT_2, 42),
    )
    glow_draw.ellipse(
        (int(-width * SCALE * 0.2), int(height * SCALE * 0.1),
         int(width * SCALE * 0.45), int(height * SCALE * 0.95)),
        fill=(*ACCENT, 24),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(120 * SCALE))
    image = Image.alpha_composite(image.convert("RGBA"), glow)

    grid = Image.new("RGBA", image.size, (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid)
    step = 64 * SCALE
    for x in range(0, image.width, step):
        grid_draw.line([(x, 0), (x, image.height)], fill=(238, 248, 245, 7), width=1)
    for y in range(0, image.height, step):
        grid_draw.line([(0, y), (image.width, y)], fill=(238, 248, 245, 7), width=1)
    return Image.alpha_composite(image, grid).convert("RGB")


def draw_phone(draw, x: int, y: int, width: int, height: int, scale: int):
    s = scale
    shadow = Image.new("RGBA", (width * 3, height * 3), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded(shadow_draw, (width, height, width * 2, height * 2), 42 * s, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(24 * s))
    return shadow  # composited by caller


def phone_panel(width: int, height: int, scale: int) -> Image.Image:
    s = scale
    panel = Image.new("RGBA", (width * s, height * s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(panel)
    rounded(draw, (0, 0, width * s - 1, height * s - 1), 34 * s, fill=(3, 9, 11), outline=(238, 248, 245, 55), width=2 * s)
    inner = 10 * s
    rounded(draw, (inner, inner, width * s - inner, height * s - inner), 27 * s, fill=(7, 17, 21))
    # notch
    rounded(draw, ((width * s - 78 * s) // 2, 7 * s, (width * s + 78 * s) // 2, 21 * s), 8 * s, fill=(3, 9, 11))
    # status
    draw.text((24 * s, 30 * s), "9:41", font=font(10 * s, mono=True), fill=MUTED)
    draw.text((width * s - 66 * s, 30 * s), "▮▮▮", font=font(8 * s, mono=True), fill=MUTED)
    # header
    draw.text((24 * s, 56 * s), "Home", font=font(17 * s, bold=True), fill=TEXT)
    draw.text((width * s - 88 * s, 60 * s), "9 apps", font=font(9 * s, mono=True), fill=ACCENT)
    # app grid: a clean 3x3 home screen with the same marks as the site
    cols, rows = 3, 3
    labels = ["Ph", "Ms", "Ca", "Fo", "Ma", "Cl", "Fi", "Pl", "Se"]
    icons = ["phone", "googlemessages", "camera", "googlephotos", "googlemaps",
             "clock", "files", "googleplay", "settings"]
    left, top = 30 * s, 100 * s
    gap_x = 14 * s
    tile = (width * s - left * 2 - gap_x * (cols - 1)) // cols
    gap_y = 14 * s
    for index in range(cols * rows):
        row, col = divmod(index, cols)
        tx = left + col * (tile + gap_x)
        ty = top + row * (tile + gap_y)
        color = TILE_COLORS[index % len(TILE_COLORS)]
        rounded(draw, (tx, ty, tx + tile, ty + tile), 12 * s, fill=color)
        icon_path = ASSETS / "apps" / "png" / f"{icons[index]}.png"
        if icon_path.is_file():
            icon = Image.open(icon_path).convert("RGBA")
            icon_size = int(tile * 0.62)
            icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
            panel.paste(icon, (tx + (tile - icon_size) // 2, ty + (tile - icon_size) // 2), icon)
        else:
            draw.text((tx + tile // 2, ty + tile // 2), labels[index],
                      font=font(11 * s, mono=True, bold=True), fill=INK, anchor="mm")
    # dock
    dock_y = height * s - 34 * s
    rounded(draw, (24 * s, dock_y, width * s - 24 * s, dock_y + 1 * s), 0, fill=(238, 248, 245, 24))
    for index in range(4):
        dx = 54 * s + index * 44 * s
        rounded(draw, (dx, dock_y + 9 * s, dx + 26 * s, dock_y + 35 * s), 8 * s, fill=(238, 248, 245, 24))
    return panel


def compose(width: int, height: int, title_lines, subtitle, eyebrow, chips, phone_size, phone_pos, output):
    image = base_canvas(width, height)
    s = SCALE
    draw = ImageDraw.Draw(image)

    # logo
    lx, ly, size = 72 * s, 58 * s, 48 * s
    rounded(draw, (lx, ly, lx + size, ly + size), 13 * s, fill=INK_2, outline=(*ACCENT, 180), width=2 * s)
    rounded(draw, (lx + size * 0.34, ly + size * 0.16, lx + size * 0.66, ly + size * 0.84), 5 * s, outline=(*ACCENT, 255), width=2 * s)
    draw.line((lx + size * 0.42, ly + size * 0.76, lx + size * 0.58, ly + size * 0.76), fill=(*ACCENT, 255), width=2 * s)
    draw.text((lx + size + 16 * s, ly + 8 * s), "CleanYourPhone", font=font(24 * s, bold=True), fill=TEXT)

    # eyebrow
    draw.text((72 * s, 132 * s), eyebrow, font=font(11 * s, mono=True, bold=True), fill=ACCENT)

    # headline
    y = 156 * s
    for line, color in title_lines:
        draw.text((72 * s, y), line, font=font(64 * s, bold=True), fill=color)
        y += 66 * s

    # subtitle
    draw.multiline_text((72 * s, y + 10 * s), subtitle, font=font(15 * s), fill=MUTED, spacing=6 * s)

    # chips
    chip_y = height * s - 62 * s
    x = 72 * s
    for label in chips:
        label_font = font(10 * s, mono=True)
        bbox = draw.textbbox((0, 0), label, font=label_font)
        w = bbox[2] - bbox[0] + 24 * s
        rounded(draw, (x, chip_y, x + w, chip_y + 30 * s), 15 * s, fill=(238, 248, 245, 14),
                outline=(238, 248, 245, 28), width=1 * s)
        draw.text((x + 12 * s, chip_y + 8 * s), label, font=label_font, fill=MUTED)
        x += w + 10 * s

    # phone
    pw, ph = phone_size
    px, py = phone_pos[0] * s, phone_pos[1] * s
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    rounded(shadow_draw, (px, py, px + pw * s, py + ph * s), 40 * s, fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26 * s))
    image = Image.alpha_composite(image.convert("RGBA"), shadow).convert("RGB")
    panel = phone_panel(pw, ph, s)
    image.paste(panel, (px, py), panel)

    target = ASSETS / output
    target.parent.mkdir(parents=True, exist_ok=True)
    final = image.resize((width, height), Image.LANCZOS)
    final.save(target, optimize=True)
    print("wrote", target)


def compose_skill(width: int, height: int, output: str, scale: int = 2):
    image = base_canvas(width, height)
    draw = ImageDraw.Draw(image)
    s = scale

    lx, ly, size = 72 * s, 58 * s, 48 * s
    rounded(draw, (lx, ly, lx + size, ly + size), 13 * s, fill=INK_2, outline=(*ACCENT, 180), width=2 * s)
    rounded(draw, (lx + size * 0.34, ly + size * 0.16, lx + size * 0.66, ly + size * 0.84), 5 * s,
            outline=(*ACCENT, 255), width=2 * s)
    draw.line((lx + size * 0.42, ly + size * 0.76, lx + size * 0.58, ly + size * 0.76),
              fill=(*ACCENT, 255), width=2 * s)
    draw.text((lx + size + 16 * s, ly + 8 * s), "CleanYourPhone", font=font(24 * s, bold=True), fill=TEXT)

    draw.text((72 * s, 132 * s), "OPEN SOURCE · ADB · REVERSIBLE", font=font(11 * s, mono=True, bold=True), fill=ACCENT)
    draw.text((72 * s, 158 * s), "Your phone,", font=font(58 * s, bold=True), fill=TEXT)
    draw.text((72 * s, 220 * s), "minus the bloat.", font=font(58 * s, bold=True), fill=ACCENT)
    draw.multiline_text((72 * s, 300 * s),
                        "One prompt. One plan.\nOne command to undo.",
                        font=font(16 * s), fill=MUTED, spacing=5 * s)

    # terminal card
    card_w = int(width * 0.42) * s
    card_h = int(height * 0.56) * s
    cx = int(width * 0.52) * s
    cy = int(height * 0.2) * s
    rounded(draw, (cx, cy, cx + card_w, cy + card_h), 16 * s, fill=(3, 9, 11), outline=(*ACCENT, 70), width=2 * s)
    draw.text((cx + 18 * s, cy + 14 * s), "terminal", font=font(9 * s, mono=True), fill=MUTED_2)
    for i in range(3):
        draw.ellipse((cx + 18 * s + i * 12 * s, cy + 34 * s, cx + 24 * s + i * 12 * s, cy + 40 * s),
                     fill=(*ACCENT, 120))
    lines = [
        ("$ python tools/phone.py plan", TEXT),
        ("DISABLE  5 packages", ACCENT),
        ("ASK      3 packages", WARM),
        ("BLOCKED  0 packages", MUTED),
        ("", MUTED),
        ("$ python tools/phone.py apply", TEXT),
        ("Batch 1/1 · verify · done", ACCENT_2),
    ]
    y = cy + 64 * s
    for text, color in lines:
        draw.text((cx + 24 * s, y), text, font=font(11 * s, mono=True), fill=color)
        y += 22 * s

    draw.text((72 * s, height * s - 48 * s), "No root · No telemetry · MIT · 157 profiles",
              font=font(11 * s, mono=True), fill=MUTED_2)

    target = ASSETS / output
    target.parent.mkdir(parents=True, exist_ok=True)
    final = image.resize((width, height), Image.LANCZOS)
    final.save(target, optimize=True)
    print("wrote", target)


def main():
    compose(
        1600, 440,
        [("Your phone,", TEXT), ("minus the bloat.", ACCENT)],
        "Disable preinstalled Android apps over ADB.\nNo root. No ROM. Nothing uninstalled.",
        "OPEN SOURCE · ADB · REVERSIBLE",
        ["No root", "No telemetry", "MIT", "157 profiles"],
        (236, 348), (1288, 42), "banner.png",
    )
    compose(
        1280, 640,
        [("Your phone,", TEXT), ("minus the bloat.", ACCENT)],
        "Disable preinstalled Android apps over ADB.\nNo root. No ROM. Nothing uninstalled.\nEvery change has an undo command.",
        "OPEN SOURCE · ADB · REVERSIBLE",
        ["No root", "No telemetry", "MIT", "157 profiles"],
        (250, 388), (952, 108), "og.png",
    )
    compose_skill(1600, 440, "brand/banner-skill.png")
    compose_skill(1280, 640, "brand/social-skill.png")
    import shutil
    shutil.copyfile(ASSETS / "banner.png", ASSETS / "brand" / "banner-web.png")
    shutil.copyfile(ASSETS / "og.png", ASSETS / "brand" / "social-web.png")
    print("copied brand banner-web.png and social-web.png")


if __name__ == "__main__":
    main()
