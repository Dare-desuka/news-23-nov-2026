#!/usr/bin/env python3
"""Draw the 23 November 2026 news front page (1024x1024 PNG).

Everything here is drawn with plain PIL shapes and text; no external
assets, no network, no clock, no randomness, so repeated runs produce
the exact same file.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
MARGIN = 36
GAP = 16
PANEL_W = 468
PANEL_H = 322

PAPER = (246, 240, 225)
INK = (22, 22, 22)
SOFT = (74, 74, 74)
RULE_RED = (176, 32, 32)
GOLD = (214, 164, 32)

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD_PATH if bold else PLAIN_PATH, size)


def split_lines(draw, text, fnt, max_width):
    """Greedy word wrap using the font's real pixel widths."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- art panels

def art_rubble(d, x, y, w, h):
    """Collapsed apartment block with a rescuer on the mound."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 216))
    # leaning block, left side
    d.polygon([(x + 18, y + 22), (x + 178, y + 22), (x + 168, y + 128),
               (x + 8, y + 128)], fill=(122, 122, 118))
    for row in range(3):
        for col in range(3):
            wx = x + 34 + col * 44
            wy = y + 36 + row * 34
            d.rectangle([wx, wy, wx + 26, wy + 20], fill=(52, 52, 52))
    # rubble mound
    d.polygon([(x + 120, y + h), (x + 230, y + 62), (x + 330, y + 96),
               (x + w - 8, y + h)], fill=(152, 148, 138))
    d.polygon([(x + 250, y + 96), (x + 300, y + 76), (x + 350, y + 96)],
              fill=(132, 128, 118))
    d.rectangle([x + 262, y + 104, x + 296, y + 122], fill=(96, 96, 92))
    d.rectangle([x + 318, y + 110, x + 348, y + 126], fill=(96, 96, 92))
    # dust puffs
    for cx, cy, r in [(x + 240, y + 40, 7), (x + 268, y + 30, 5),
                      (x + 300, y + 46, 6)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(206, 200, 188))
    # rescuer, orange helmet and vest
    d.ellipse([x + 372, y + 34, x + 396, y + 58], fill=(232, 146, 44))
    d.rectangle([x + 370, y + 58, x + 398, y + 66], fill=(232, 146, 44))
    d.rectangle([x + 372, y + 66, x + 396, y + 104], fill=(226, 106, 44))
    d.rectangle([x + 372, y + 104, x + 382, y + 128], fill=(48, 48, 48))
    d.rectangle([x + 386, y + 104, x + 396, y + 128], fill=(48, 48, 48))
    # small child figure beside the rescuer
    d.ellipse([x + 402, y + 66, x + 418, y + 82], fill=(240, 196, 150))
    d.rectangle([x + 402, y + 82, x + 418, y + 112], fill=(52, 96, 178))
    d.rectangle([x + 404, y + 112, x + 412, y + 128], fill=(48, 48, 48))
    d.rectangle([x + 412, y + 112, x + 418, y + 128], fill=(48, 48, 48))


def art_chart(d, x, y, w, h):
    """Falling market line with a gold safe-haven note."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 239, 248))
    for gy in range(1, 4):
        yy = y + gy * h // 4
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(210, 218, 232), width=1)
    pts = [(x + 16, y + 26), (x + 90, y + 40), (x + 170, y + 34),
           (x + 250, y + 38), (x + 330, y + 78), (x + 400, y + 104),
           (x + w - 16, y + 118)]
    d.line(pts, fill=(176, 32, 32), width=5, joint="curve")
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(176, 32, 32))
    d.text((x + 18, y + 78), "-5.06%", font=font(36), fill=(176, 32, 32))
    d.text((x + w - 168, y + 16), "+2.7% GOLD", font=font(21),
           fill=(158, 116, 10))
    # gold bars, bottom right
    for i, bh in enumerate((16, 26, 38)):
        bx = x + w - 118 + i * 38
        d.rectangle([bx, y + h - 12 - bh, bx + 30, y + h - 12],
                    fill=(214, 164, 32), outline=(150, 108, 8))


def art_airport(d, x, y, w, h):
    """Grounded plane under a control tower, flights cancelled."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 218, 240))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(128, 128, 126))
    d.line([(x, y + h - 34), (x + w, y + h - 34)], fill=(90, 90, 88),
           width=3)
    # control tower
    d.rectangle([x + 34, y + 48, x + 52, y + h - 34], fill=(150, 150, 148))
    d.rectangle([x + 22, y + 26, x + 64, y + 50], fill=(52, 96, 178))
    d.rectangle([x + 22, y + 26, x + 64, y + 34], fill=(120, 200, 240))
    # plane fuselage
    d.polygon([(x + 96, y + 92), (x + 330, y + 92), (x + 372, y + 104),
               (x + 330, y + 116), (x + 96, y + 116)], fill=(244, 244, 244),
              outline=(60, 60, 60))
    d.polygon([(x + 150, y + 92), (x + 176, y + 62), (x + 196, y + 92)],
              fill=(244, 244, 244), outline=(60, 60, 60))
    d.polygon([(x + 300, y + 92), (x + 322, y + 66), (x + 336, y + 92)],
              fill=(244, 244, 244), outline=(60, 60, 60))
    d.polygon([(x + 96, y + 104), (x + 70, y + 92), (x + 70, y + 116)],
              fill=(244, 244, 244), outline=(60, 60, 60))
    for wx in (150, 200, 250, 300):
        d.ellipse([x + wx, y + 98, x + wx + 12, y + 110],
                  fill=(52, 96, 178))
    # cancelled box
    d.rectangle([x + w - 178, y + 12, x + w - 12, y + 62], fill=(10, 10, 10))
    d.text((x + w - 168, y + 16), "CANCELLED", font=font(19),
           fill=(232, 52, 52))
    d.text((x + w - 168, y + 38), "429 FLIGHTS", font=font(16),
           fill=(255, 255, 255))


def art_ship(d, x, y, w, h):
    """Container ship carrying the trillion-dollar export story."""
    # banner strip across the top keeps the label clear of the cargo
    d.rectangle([x, y, x + w, y + h], fill=(188, 220, 240))
    d.rectangle([x, y, x + w, y + 34], fill=(255, 255, 255))
    d.rectangle([x + 10, y + 4, x + 38, y + 30], fill=(14, 14, 14))
    d.text((x + 16, y + 9), "AI", font=font(18), fill=(255, 255, 255))
    d.text((x + 48, y + 7), "$1 TRILLION", font=font(24), fill=INK)
    sea_top = y + h - 30
    d.rectangle([x, sea_top, x + w, y + h], fill=(52, 128, 196))
    for wx in (20, 120, 220, 320):
        d.arc([x + wx, sea_top + 8, x + wx + 60, sea_top + 22],
              start=200, end=340, fill=(255, 255, 255), width=2)
    # hull
    d.polygon([(x + 24, sea_top - 26), (x + w - 24, sea_top - 26),
               (x + w - 52, sea_top + 12), (x + 52, sea_top + 12)],
              fill=(30, 30, 34))
    # container stacks
    palette = [(176, 32, 32), (36, 86, 178), (16, 122, 110),
               (214, 164, 32), (46, 128, 60)]
    for row in range(2):
        for col in range(5):
            cx = x + 52 + col * 76
            cy = sea_top - 26 - (row + 1) * 26
            d.rectangle([cx, cy, cx + 70, cy + 22],
                        fill=palette[(row * 5 + col) % len(palette)],
                        outline=(20, 20, 20))


# ------------------------------------------------------------------ panels

STORIES = [
    {
        "tag": "DYMER  •  UKRAINE",
        "bar": (176, 32, 32),
        "art": art_rubble,
        "headline": "Boy, 7, pulled alive after 14 hours in rubble",
        "caption": ("Rescuers freed David from the rubble; at least 10 "
                    "died in the drone strike."),
    },
    {
        "tag": "TOKYO  •  MARKETS",
        "bar": (30, 80, 180),
        "art": art_chart,
        "headline": "AI sell-off rattles Asia's markets",
        "caption": ("Nikkei -5.06%, Korea and Hong Kong down again; gold "
                    "+2.7% as investors seek safety."),
    },
    {
        "tag": "BRUSSELS  •  EUROPE",
        "bar": (14, 122, 110),
        "art": art_airport,
        "headline": "Belgium's airports shut down by strike",
        "caption": ("Air traffic control halted 7am-9pm; 429 flights "
                    "cancelled, 60,000 passengers hit."),
    },
    {
        "tag": "SEOUL  •  TRADE",
        "bar": (176, 32, 32),
        "art": art_ship,
        "headline": "South Korea passes $1 trillion in exports",
        "caption": ("Monday customs data put exports at $1.0076 trillion, "
                    "a first, driven by AI chips."),
    },
]

ALSO_TODAY = [
    ("Marquez takes eighth MotoGP title at Portim\u00e3o, level with "
     "Agostini  \u2022  Liverpool thrash Man Utd 4-0"),
    ("Houthis claim a strike on Saudi Arabia's Rabigh refinery; Saudi "
     "strike on Hodeida kills at least 4"),
    ("Search resumes at the Cikande candy factory fire; 24 body bags, "
     "29 workers still missing"),
]


def draw_story(draw, story, x, y):
    draw.rectangle([x, y, x + PANEL_W, y + PANEL_H], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.rectangle([x, y, x + PANEL_W, y + 36], fill=story["bar"])
    draw.text((x + 14, y + 7), story["tag"], font=font(20), fill=(255, 255, 255))
    story["art"](draw, x + 10, y + 46, PANEL_W - 20, 144)
    head_f = font(28)
    lines = split_lines(draw, story["headline"], head_f, PANEL_W - 28)
    hy = y + 200
    for line in lines:
        draw.text((x + 14, hy), line, font=head_f, fill=INK)
        hy += 30
    cap_f = font(20, bold=False)
    for line in split_lines(draw, story["caption"], cap_f, PANEL_W - 28):
        draw.text((x + 14, hy + 2), line, font=cap_f, fill=SOFT)
        hy += 22


def build_page():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)

    centred(d, CANVAS_W // 2, 24, "THE WORLD IN ONE DAY", font(52), INK)
    centred(d, CANVAS_W // 2, 92, "MONDAY, 23 NOVEMBER 2026", font(38),
            RULE_RED)
    d.line([(MARGIN, 148), (CANVAS_W - MARGIN, 148)], fill=INK, width=3)
    centred(d, CANVAS_W // 2, 158,
            "Four stories that defined the day \u2014 as reported",
            font(22, bold=False), SOFT)

    for i, story in enumerate(STORIES):
        px = MARGIN + (i % 2) * (PANEL_W + GAP)
        py = 196 + (i // 2) * (PANEL_H + GAP)
        draw_story(d, story, px, py)

    strip_y = 872
    d.rectangle([MARGIN, strip_y, CANVAS_W - MARGIN, strip_y + 96],
                fill=(12, 12, 12))
    centred(d, CANVAS_W // 2, strip_y + 8, "ALSO TODAY", font(22), GOLD)
    item_f = font(18, bold=False)
    iy = strip_y + 36
    for item in ALSO_TODAY:
        centred(d, CANVAS_W // 2, iy, item, item_f, (255, 255, 255))
        iy += 21

    centred(d, CANVAS_W // 2, 980,
            "Stories as reported on 23 November 2026  \u2022  BBC  \u2022  "
            "Reuters  \u2022  AFP",
            font(16, bold=False), SOFT)
    return img


if __name__ == "__main__":
    page = build_page()
    page.save("entry.png")
    print("Wrote entry.png", page.size)
