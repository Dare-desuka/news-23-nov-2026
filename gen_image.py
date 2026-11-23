"""Generate entry.png: a newspaper front page summing up 23 Nov 2026.

Run: python3 gen_image.py  -> writes entry.png (1024x1024, PNG, <1 MiB)
Facts used (as reported on 23 Nov 2026 by BBC/Reuters/AFP and wire services):
 1. Rescuers in Dymer, Ukraine, pulled 7-year-old David alive from the
    rubble of an apartment block 14 hours after a Russian drone strike;
    at least 10 people were killed.
 2. The AI stock sell-off spread across Asia: Japan's Nikkei fell 5.06%,
    South Korea and Hong Kong slid again on Monday; gold rose about 2.7%
    as investors sought safety.
 3. Belgian air-traffic control provider Skeyes suspended services from
    07:00 to 21:00 in a nationwide strike; 429 flights cancelled and
    about 60,000 passengers affected.
 4. South Korean customs data released on Monday put 2026 exports at
    $1.0076 trillion, a first for the country, driven by AI-chip demand.
Also: Marc Marquez took his eighth MotoGP title at Portimao, level with
Giacomo Agostini; Liverpool beat Manchester United 4-0 in Mauricio
Pochettino's first game as United manager; Houthis claimed a strike on
Saudi Arabia's Rabigh refinery while a Saudi strike on Hodeida killed at
least four; the search resumed at the Cikande candy factory fire, with
24 body bags removed and 29 workers still missing.
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (14, 124, 123)
GREY = (90, 90, 90)
LIGHT = (255, 255, 255)
GOLD = (212, 160, 40)
SKY = (178, 216, 240)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, x, y, w, h, kicker, kcolor, headline, summary, art):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, outline=INK, width=3, fill=LIGHT)
    draw.rounded_rectangle([x, y, x + w, y + 34], radius=10, fill=kcolor)
    draw.rectangle([x, y + 20, x + w, y + 34], fill=kcolor)
    draw.text((x + 14, y + 7), kicker, font=font(BOLD, 19), fill=LIGHT)
    art(draw, x + 14, y + 48, w - 28, 118)
    ty = y + 178
    for line in wrap(draw, headline, font(BOLD, 26), w - 28):
        draw.text((x + 14, ty), line, font=font(BOLD, 26), fill=INK)
        ty += 32
    ty += 4
    for line in wrap(draw, summary, font(REG, 19), w - 28):
        draw.text((x + 14, ty), line, font=font(REG, 19), fill=(60, 60, 60))
        ty += 25


def art_rubble(draw, x, y, w, h):
    # collapsed apartment block, rubble mound, rescuer lifting a child
    draw.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    # standing half of the block
    draw.rectangle([x + 20, y + 10, x + 150, y + h - 30], fill=(150, 148, 140), outline=INK, width=3)
    for r in range(3):
        for c in range(3):
            draw.rectangle([x + 32 + c * 38, y + 22 + r * 30, x + 58 + c * 38, y + 42 + r * 30],
                           fill=(90, 90, 90))
    # broken edge of the collapsed half
    draw.polygon([(x + 150, y + 10), (x + 210, y + 55), (x + 150, y + h - 30)], fill=(120, 118, 110))
    # rubble mound
    draw.polygon([(x + 150, y + h), (x + 220, y + 60), (x + 300, y + 80), (x + 380, y + 55),
                  (x + 440, y + h)], fill=(170, 165, 150), outline=INK, width=2)
    draw.rectangle([x + 250, y + 78, x + 290, y + 96], fill=(120, 118, 110), outline=INK)
    draw.rectangle([x + 320, y + 72, x + 355, y + 92], fill=(140, 135, 125), outline=INK)
    # rescuer in orange helmet and vest, lifting a small figure
    draw.ellipse([x + 380, y + 28, x + 404, y + 50], fill=(255, 200, 140), outline=INK, width=2)
    draw.polygon([(x + 378, y + 32), (x + 406, y + 32), (x + 392, y + 20)], fill=(230, 120, 20), outline=INK)
    draw.rectangle([x + 378, y + 52, x + 406, y + 86], fill=(230, 120, 20), outline=INK, width=2)
    draw.rectangle([x + 372, y + 54, x + 380, y + 84], fill=(255, 200, 140), outline=INK)
    draw.rectangle([x + 404, y + 54, x + 412, y + 84], fill=(255, 200, 140), outline=INK)
    # child being carried, wrapped in a blanket
    draw.ellipse([x + 414, y + 58, x + 428, y + 70], fill=(255, 200, 140), outline=INK, width=2)
    draw.rectangle([x + 410, y + 70, x + 432, y + 92], fill=(60, 120, 200), outline=INK, width=2)
    # dust puffs
    for cx, cy, r in [(x + 240, y + 40, 8), (x + 270, y + 30, 6), (x + 300, y + 45, 7)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 195, 180))


def art_chart(draw, x, y, w, h):
    # red falling market line, gold bar, big -5.06%
    draw.rectangle([x, y, x + w, y + h], fill=(240, 244, 250))
    for i in range(5):
        yy = y + 18 + i * 20
        draw.line([x + 10, yy, x + w - 10, yy], fill=(220, 225, 232), width=1)
    pts = [(x + 20, y + 18), (x + 110, y + 30), (x + 190, y + 26),
           (x + 270, y + 62), (x + 350, y + 78), (x + 420, y + 108)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    draw.polygon([(x + 420, y + 108), (x + 404, y + 96), (x + 404, y + 112)], fill=RED)
    draw.text((x + 16, y + 66), "-5.06%", font=font(BOLD, 34), fill=RED)
    # gold bar rising in the corner
    draw.polygon([(x + 330, y + 100), (x + 360, y + 82), (x + 410, y + 82),
                  (x + 440, y + 100)], fill=GOLD, outline=INK, width=2)
    draw.rectangle([x + 330, y + 100, x + 440, y + 112], fill=(180, 135, 25), outline=INK, width=2)
    draw.text((x + 300, y + 6), "+2.7% GOLD", font=font(BOLD, 18), fill=(150, 110, 10))


def art_airport(draw, x, y, w, h):
    # control tower, grounded plane, cancelled departures board
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 92, x + w, y + h], fill=(150, 150, 150))
    draw.line([x, y + 92, x + w, y + 92], fill=INK, width=3)
    # control tower
    draw.rectangle([x + 30, y + 20, x + 58, y + 92], fill=(200, 200, 200), outline=INK, width=3)
    draw.polygon([(x + 18, y + 24), (x + 70, y + 24), (x + 62, y + 2), (x + 26, y + 2)],
                 fill=(90, 160, 220), outline=INK, width=3)
    draw.line([x + 44, y + 2, x + 44, y - 8], fill=INK, width=3)
    # grounded plane, nose to the right
    draw.ellipse([x + 130, y + 62, x + 330, y + 88], fill=LIGHT, outline=INK, width=3)
    draw.polygon([(x + 330, y + 66), (x + 380, y + 74), (x + 330, y + 84)], fill=LIGHT, outline=INK, width=3)
    # tail fin at the rear, swept wings
    draw.polygon([(x + 138, y + 64), (x + 152, y + 38), (x + 164, y + 64)], fill=LIGHT, outline=INK, width=3)
    draw.polygon([(x + 200, y + 64), (x + 238, y + 42), (x + 254, y + 64)], fill=LIGHT, outline=INK, width=3)
    draw.polygon([(x + 200, y + 86), (x + 238, y + 106), (x + 254, y + 86)], fill=LIGHT, outline=INK, width=3)
    for wx in (x + 170, x + 210, x + 250, x + 290):
        draw.ellipse([wx, y + 68, wx + 12, y + 80], fill=BLUE)
    # departures board, wide enough for its text
    draw.rectangle([x + 280, y + 6, x + w - 8, y + 50], fill=INK)
    draw.text((x + 290, y + 10), "CANCELLED", font=font(BOLD, 18), fill=(255, 80, 80))
    draw.text((x + 290, y + 32), "429 FLIGHTS", font=font(BOLD, 13), fill=LIGHT)


def art_ship(draw, x, y, w, h):
    # container ship carrying chips, big $1T figure
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + 84, x + w, y + h], fill=(60, 120, 180))
    for i in range(4):
        yy = y + 92 + i * 8
        draw.arc([x - 10 + i * 26, yy, x + 110 + i * 26, yy + 12], 0, 180, fill=LIGHT, width=3)
    # hull
    draw.polygon([(x + 30, y + 80), (x + 420, y + 80), (x + 390, y + 104), (x + 60, y + 104)],
                 fill=(40, 40, 40), outline=INK, width=3)
    # containers, stacked below the headline figure
    cols = [RED, BLUE, TEAL, GOLD, (40, 120, 60)]
    for row in range(2):
        for c in range(5):
            cx = x + 60 + c * 68
            cy = y + 36 + row * 22
            draw.rectangle([cx, cy, cx + 62, cy + 20], fill=cols[(c + row) % 5], outline=INK, width=2)
    # bridge
    draw.rectangle([x + 380, y + 40, x + 410, y + 80], fill=LIGHT, outline=INK, width=3)
    draw.rectangle([x + 384, y + 46, x + 406, y + 58], fill=BLUE)
    # chip
    draw.rectangle([x + 14, y + 8, x + 52, y + 46], fill=INK)
    for px in (x + 22, x + 30, x + 38):
        draw.line([px, y + 2, px, y + 8], fill=INK, width=2)
        draw.line([px, y + 46, px, y + 52], fill=INK, width=2)
    draw.text((x + 20, y + 16), "AI", font=font(BOLD, 20), fill=GOLD)
    draw.text((x + 60, y + 4), "$1 TRILLION", font=font(BOLD, 28), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.text((512, 18), "THE WORLD IN ONE DAY", font=font(BOLD, 58), fill=INK, anchor="ma")
    d.text((512, 88), "MONDAY, 23 NOVEMBER 2026", font=font(BOLD, 38), fill=RED, anchor="ma")
    d.line([40, 140, 984, 140], fill=INK, width=4)
    d.text((512, 150), "Four stories that defined the day — as reported", font=font(REG, 22), fill=GREY, anchor="ma")
    # panels 2x2
    pw, ph = 462, 330
    panel(d, 40, 190, pw, ph, "DYMER  •  UKRAINE", RED,
          "Boy, 7, pulled alive after 14 hours in rubble",
          "Rescuers freed David from a collapsed apartment block; at least 10 were killed in the drone strike.",
          art_rubble)
    panel(d, 522, 190, pw, ph, "TOKYO  •  MARKETS", BLUE,
          "AI sell-off rattles Asia's markets",
          "Nikkei -5.06%, Korea and Hong Kong down again; gold +2.7% as investors seek safety.",
          art_chart)
    panel(d, 40, 540, pw, ph, "BRUSSELS  •  EUROPE", TEAL,
          "Belgium's airports shut down by strike",
          "Skeyes halted air traffic control 7am-9pm; 429 flights cancelled, 60,000 passengers hit.",
          art_airport)
    panel(d, 522, 540, pw, ph, "SEOUL  •  TRADE", RED,
          "South Korea passes $1 trillion in exports",
          "Monday customs data put 2026 exports at $1.0076 trillion — a first, driven by AI chips.",
          art_ship)
    # also strip
    d.rectangle([40, 886, 984, 972], fill=INK)
    d.text((512, 890), "ALSO TODAY", font=font(BOLD, 18), fill=(255, 200, 60), anchor="ma")
    d.text((512, 912), "Marquez takes eighth MotoGP title at Portimao, level with Agostini  •  Liverpool thrash Man Utd 4-0",
           font=font(REG, 15), fill=LIGHT, anchor="ma")
    d.text((512, 932), "Houthis claim a strike on Saudi Arabia's Rabigh refinery; Saudi strike on Hodeida kills at least 4",
           font=font(REG, 15), fill=LIGHT, anchor="ma")
    d.text((512, 952), "Search resumes at the Cikande candy factory fire; 24 body bags removed, 29 workers still missing",
           font=font(REG, 15), fill=LIGHT, anchor="ma")
    d.text((512, 982), "Stories as reported on 23 November 2026  •  BBC  •  Reuters  •  AFP",
           font=font(REG, 16), fill=GREY, anchor="ma")
    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
