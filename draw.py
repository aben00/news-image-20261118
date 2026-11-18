#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: "THE WORLD TODAY", a newspaper
front page summing up Wednesday 18 November 2026 in 32 verified stories.

Layout (1024x1024, Pillow + DejaVu only):
  * masthead with the date set large, so the day is unmistakable
  * 3 lead tiles with flat illustrations, one-line headlines, two-line decks
  * 3 more illustrated tiles in a second row
  * "THE DAY IN BRIEF": 26 further headlines in two columns, one per line,
    each led by a coloured field dot, so the breadth of the day reads at
    a glance without any story needing a second line

Run:  python3 draw.py            (writes entry.png next to this script)
Deterministic: no timestamps, no randomness, fixed font metrics, so two
runs of the program write byte-identical PNGs.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (18, 34, 62)
AMBER = (232, 163, 23)
PAPER = (248, 246, 241)
INK = (22, 26, 32)
GREY = (88, 94, 102)
CARD = (255, 255, 255)
EDGE = (212, 210, 204)


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, font, max_w):
    """Greedy word wrap; returns the lines that fit inside max_w pixels."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def fit_line(d, text, font, max_w):
    """Shorten text with an ellipsis until it fits max_w pixels."""
    if d.textlength(text, font=font) <= max_w:
        return text
    while text and d.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def centred(d, cx, y, text, font, fill):
    d.text((cx - d.textlength(text, font=font) / 2, y), text, font=font, fill=fill)


def starburst(d, cx, cy, r, fill):
    """Twelve-ray flash with a bright core."""
    for k in range(12):
        ang = math.radians(k * 30)
        reach = r if k % 2 == 0 else r * 0.55
        d.line([(cx + 9 * math.cos(ang), cy + 9 * math.sin(ang)),
                (cx + reach * math.cos(ang), cy + reach * math.sin(ang))],
               fill=fill, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 205, 70))


def quadcopter(d, cx, cy, s, body=(54, 62, 72)):
    """A small quadcopter drone, side view."""
    d.ellipse([cx - s, cy - s * 0.42, cx + s, cy + s * 0.42], fill=body)
    d.ellipse([cx - s * 0.32, cy - s * 0.18, cx + s * 0.32, cy + s * 0.18],
              fill=(28, 32, 38))
    for side in (-1, 1):
        d.line([(cx + side * s * 0.9, cy - s * 0.28),
                (cx + side * s * 1.65, cy - s * 0.52)],
               fill=(96, 102, 110), width=3)
        d.ellipse([cx + side * s * 1.65 - 10, cy - s * 0.62,
                   cx + side * s * 1.65 + 10, cy - s * 0.46],
                  fill=(146, 154, 162))


# ---------------------------------------------------------------- masthead
def masthead(d):
    d.rectangle([0, 0, W, 128], fill=NAVY)
    d.rectangle([0, 128, W, 132], fill=AMBER)
    centred(d, W // 2, 12, "W E D N E S D A Y   ·   1 8   N O V E M B E R   2 0 2 6",
            fnt(BOLD, 24), AMBER)
    centred(d, W // 2, 44, "THE WORLD TODAY", fnt(BOLD, 56), (255, 255, 255))
    centred(d, W // 2, 106, "32 stories that defined the day",
            fnt(REG, 18), (198, 206, 220))


# ------------------------------------------------------------- tile art
# Every art function draws inside (x, y, w, h) with positions relative to
# h, so the same art works at the lead row's height and the second row's.
def art_gulf(d, x, y, w, h):
    """Night over the Gulf: radar dish, drones, one intercepted mid-air."""
    d.rectangle([x, y, x + w, y + h], fill=(15, 27, 47))
    for sx, sy in ((24, 14), (86, 30), (150, 10), (210, 24), (272, 12), (120, 40)):
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 56, y + 8, x + w - 20, y + 44], fill=(246, 202, 92))
    sea = y + int(h * 0.72)
    d.rectangle([x, sea, x + w, y + h], fill=(36, 72, 104))
    d.line([(x + 12, sea + 14), (x + 96, sea + 14)], fill=(255, 255, 255), width=3)
    d.line([(x + w - 116, sea + 26), (x + w - 24, sea + 26)],
           fill=(255, 255, 255), width=3)
    base = y + int(h * 0.60)
    d.rectangle([x + 16, base, x + 96, sea], fill=(88, 99, 110))
    d.arc([x + 30, y + int(h * 0.26), x + 92, base + 6], start=195, end=345,
          fill=(202, 208, 214), width=6)
    d.line([(x + 61, y + int(h * 0.44)), (x + 116, y + int(h * 0.24))],
           fill=AMBER, width=3)
    quadcopter(d, x + int(w * 0.55), y + int(h * 0.36), 22)
    starburst(d, x + int(w * 0.80), y + int(h * 0.26), 24, (236, 132, 42))
    quadcopter(d, x + int(w * 0.42), y + int(h * 0.56), 17)
    for bx, bw, bh in ((w - 96, 30, 26), (w - 60, 24, 38), (w - 30, 18, 20)):
        d.rectangle([x + bx, sea - bh, x + bx + bw, sea], fill=(68, 82, 98))
        for wy in range(sea - bh + 4, sea - 4, 12):
            for wx in range(x + bx + 5, x + bx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 222, 122))


def art_nvidia(d, x, y, w, h):
    """A green chip on a circuit board under a rising red chart line."""
    d.rectangle([x, y, x + w, y + h], fill=(212, 230, 212))
    for ty in (0.16, 0.28, 0.84, 0.94):
        yy = y + int(h * ty)
        d.line([(x + 8, yy), (x + w - 8, yy)], fill=(138, 178, 138), width=3)
    for tx in (0.09, 0.21, 0.79, 0.91):
        xx = x + int(w * tx)
        d.line([(xx, y + 8), (xx, y + h - 8)], fill=(138, 178, 138), width=3)
    for fx, fy in ((0.09, 0.16), (0.21, 0.28), (0.79, 0.84), (0.91, 0.94),
                   (0.09, 0.94), (0.91, 0.16)):
        cx, cy = x + int(w * fx), y + int(h * fy)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(88, 138, 88))
    cs = int(h * 0.58)
    cx0, cy0 = x + w // 2 - cs // 2, y + int(h * 0.16)
    for i in range(4):
        for px in (cx0 - 12, cx0 + cs + 6):
            d.rectangle([px, cy0 + 10 + i * (cs // 4), px + 6,
                         cy0 + 22 + i * (cs // 4)], fill=(178, 184, 190))
        for py in (cy0 - 12, cy0 + cs + 6):
            d.rectangle([cx0 + 10 + i * (cs // 4), py,
                         cx0 + 22 + i * (cs // 4), py + 6], fill=(178, 184, 190))
    d.rectangle([cx0, cy0, cx0 + cs, cy0 + cs], fill=(28, 32, 38))
    d.rectangle([cx0 + 9, cy0 + 9, cx0 + cs - 9, cy0 + cs - 9], fill=(32, 138, 32))
    d.rectangle([cx0 + 18, cy0 + 18, cx0 + cs - 18, cy0 + cs - 18],
                fill=(44, 158, 44))
    centred(d, x + w // 2, cy0 + cs // 2 - 9, "$115.8B", fnt(BOLD, 15),
            (255, 255, 255))
    pts = [(x + 22, y + h - 8), (x + 82, y + h - 22), (x + 138, y + h - 18),
           (x + 198, y + h - 38), (x + 260, y + h - 56), (x + 296, y + h - 64)]
    d.line(pts, fill=(178, 34, 34), width=5, joint="curve")
    d.polygon([(x + 296, y + h - 64), (x + 278, y + h - 68), (x + 288, y + h - 48)],
              fill=(178, 34, 34))


def art_quad(d, x, y, w, h):
    """Four flags — US, India, Japan, Australia — behind a round table."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 235, 244))
    d.ellipse([x + int(w * 0.17), y + int(h * 0.66), x + int(w * 0.83),
               y + int(h * 0.94)], fill=(146, 104, 66))
    d.rectangle([x + w // 2 - 12, y + int(h * 0.86), x + w // 2 + 12, y + h - 4],
                fill=(122, 84, 52))
    d.ellipse([x + int(w * 0.17), y + int(h * 0.60), x + int(w * 0.83),
               y + int(h * 0.86)], fill=(176, 130, 84))
    top, bot = y + int(h * 0.14), y + int(h * 0.52)
    for label, fx in zip(("US", "IN", "JP", "AU"),
                         (0.10, 0.32, 0.54, 0.76)):
        px = x + int(w * fx)
        d.line([(px + 20, top), (px + 20, y + int(h * 0.68))],
               fill=(80, 70, 60), width=4)
        if label == "US":
            for row in range(6):
                col = (178, 34, 34) if row % 2 == 0 else (255, 255, 255)
                d.rectangle([px, top + row * 7, px + 40, top + 7 + row * 7], fill=col)
            d.rectangle([px, top, px + 17, top + 18], fill=(30, 50, 110))
        elif label == "IN":
            d.rectangle([px, top, px + 40, top + 14], fill=(255, 153, 51))
            d.rectangle([px, top + 14, px + 40, top + 28], fill=(255, 255, 255))
            d.rectangle([px, top + 28, px + 40, top + 42], fill=(19, 136, 8))
            d.ellipse([px + 14, top + 18, px + 26, top + 30],
                      outline=(0, 56, 147), width=2)
        elif label == "JP":
            d.rectangle([px, top, px + 40, top + 42], fill=(255, 255, 255))
            d.ellipse([px + 13, top + 10, px + 27, top + 24], fill=(188, 0, 45))
        else:
            d.rectangle([px, top, px + 40, top + 42], fill=(0, 40, 104))
            d.line([(px, top), (px + 40, top + 42)], fill=(255, 255, 255), width=3)
            d.line([(px + 40, top), (px, top + 42)], fill=(255, 255, 255), width=3)
    for fx in (0.13, 0.36, 0.59, 0.82):
        cx0 = x + int(w * fx)
        d.rectangle([cx0, y + int(h * 0.82), cx0 + 40, y + int(h * 0.90)],
                    fill=(94, 80, 66))


def art_bridge(d, x, y, w, h):
    """A river bridge at dusk: two towers, a broken span, smoke rising."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 204))
    d.ellipse([x + w - 62, y + 8, x + w - 26, y + 44], fill=(246, 200, 92))
    river = y + int(h * 0.70)
    d.rectangle([x, river, x + w, y + h], fill=(92, 128, 158))
    for wy in (river + 12, river + 24):
        d.line([(x + 16, wy), (x + 120, wy)], fill=(255, 255, 255), width=3)
        d.line([(x + w - 130, wy + 4), (x + w - 20, wy + 4)],
               fill=(255, 255, 255), width=3)
    deck = y + int(h * 0.52)
    d.rectangle([x + 10, deck, x + w - 10, deck + 8], fill=(74, 82, 92))
    d.rectangle([x + w // 2 - 26, deck, x + w // 2 + 26, river],
                fill=(232, 222, 204))
    for tx in (x + int(w * 0.16), x + int(w * 0.78)):
        d.rectangle([tx, y + int(h * 0.12), tx + 14, deck], fill=(96, 104, 114))
        d.rectangle([tx - 6, y + int(h * 0.08), tx + 20, y + int(h * 0.14)],
                    fill=(74, 82, 92))
        d.line([(tx + 7, y + int(h * 0.14)), (x + w // 2, deck)],
               fill=(150, 158, 166), width=3)
    starburst(d, x + w // 2, y + int(h * 0.32), 24, (236, 132, 42))
    for fx, fy, sr in ((0.40, 0.14, 12), (0.52, 0.08, 15), (0.62, 0.15, 11)):
        sx, sy = x + int(w * fx), y + int(h * fy)
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 126, 132))
    d.polygon([(x + 30, river + 12), (x + 86, river + 12), (x + 72, river + 24),
               (x + 44, river + 24)], fill=(52, 60, 70))


def art_latvia(d, x, y, w, h):
    """Latvia's flag over parliament benches, with a ticked ballot box."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    fx0, fx1 = x + 22, x + w - 22
    d.rectangle([fx0, y + int(h * 0.08), fx1, y + int(h * 0.30)], fill=(158, 27, 50))
    d.rectangle([fx0, y + int(h * 0.30), fx1, y + int(h * 0.38)],
                fill=(255, 255, 255))
    d.rectangle([fx0, y + int(h * 0.38), fx1, y + int(h * 0.60)], fill=(158, 27, 50))
    d.line([(fx0, y + int(h * 0.08)), (fx0, y + int(h * 0.60))],
           fill=(80, 70, 60), width=4)
    for row, fy in enumerate((0.66, 0.78, 0.90)):
        ry = y + int(h * fy)
        for i in range(7):
            sx = x + 28 + i * 40
            col = (30, 122, 52) if (i + row) % 3 else (178, 34, 34)
            d.ellipse([sx, ry, sx + 22, ry + 10], fill=col)
    bx0, by0 = x + w - 98, y + int(h * 0.68)
    d.rectangle([bx0, by0, bx0 + 72, by0 + int(h * 0.30)], fill=(74, 85, 96))
    d.rectangle([bx0 - 6, by0 - 10, bx0 + 78, by0], fill=(52, 60, 70))
    d.rectangle([bx0 + 24, by0 - 15, bx0 + 48, by0 - 7], fill=(24, 28, 34))
    d.line([(bx0 + 18, by0 + 14), (bx0 + 32, by0 + 24), (bx0 + 56, by0 + 2)],
           fill=(46, 180, 90), width=6)


def art_cyclone(d, x, y, w, h):
    """A spiral cyclone over the Bay of Bengal, rain slanting down."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 219, 233))
    sea = y + int(h * 0.68)
    d.rectangle([x, sea, x + w, y + h], fill=(96, 140, 168))
    cx, cy = x + w // 2, y + int(h * 0.46)
    for ring, (r1, col) in enumerate(((int(h * 0.12), (255, 255, 255)),
                                      (int(h * 0.27), (220, 232, 240)),
                                      (int(h * 0.42), (190, 210, 224)))):
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              start=ring * 100, end=ring * 100 + 300, fill=col, width=14)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(38, 74, 106))
    d.polygon([(x, y + h), (x, sea + 8), (x + 88, sea), (x + 118, sea + 22),
               (x + 68, y + h)], fill=(120, 150, 110))
    for rx, ry in ((38, 22), (88, 12), (258, 18), (288, 34), (208, 10), (128, 34)):
        d.line([(x + rx, y + ry), (x + rx - 8, y + ry + 16)],
               fill=(120, 150, 180), width=3)
    tx, ty = x + w - 64, sea + 16
    d.polygon([(tx, ty), (tx + 44, ty), (tx + 22, ty - 30)], fill=AMBER)
    d.rectangle([tx + 20, ty - 23, tx + 24, ty - 9], fill=(24, 28, 34))
    d.ellipse([tx + 20, ty - 7, tx + 24, ty - 3], fill=(24, 28, 34))


# ------------------------------------------------------------- the stories
# Six illustrated tiles: (kicker, headline, deck, accent colour, art fn).
# Headlines are one line; decks wrap to at most two lines.
LEAD = [
    ("MIDDLE EAST · GULF", "DRONES OVER GULF",
     "Kuwait shoots down hostile drones; Bahrain sounds the all-clear.",
     (178, 34, 34), art_gulf),
    ("USA · BUSINESS", "NVIDIA +103%",
     "Revenue $115.8bn, up 103%, first report since Huang exit.",
     (34, 139, 34), art_nvidia),
    ("ASIA · DIPLOMACY", "QUAD IN MANILA",
     "First Quad leaders' summit since 2024 opens in Manila.",
     (0, 90, 140), art_quad),
]
SECOND = [
    ("EUROPE · WAR", "KYIV BRIDGES HIT",
     "Ukraine damages the Crimean bridge as Russia strikes bridges in Kyiv.",
     (146, 40, 40), art_bridge),
    ("EUROPE · POLITICS", "LATVIA'S NEW GOVT",
     "Kulbergs' cabinet approved 57–34 before Independence Day.",
     (158, 27, 50), art_latvia),
    ("ASIA · WEATHER", "AKVAN STRENGTHENS",
     "Bay of Bengal storm set to turn severe by Thursday.",
     (28, 110, 88), art_cyclone),
]

# The day in brief: (headline, field-dot colour). One line each, two columns.
BRIEF = [
    ("Dow plunges 848 points; S&P lowest since July", (34, 139, 34)),
    ("Judge gives Trump until 22 Jan in $10bn BBC suit", (110, 70, 160)),
    ("Asif Merchant jailed 27.5 years over Trump plot", (90, 90, 100)),
    ("Iran weighed dirty-bomb attack on US officials", (178, 34, 34)),
    ("US presses ICAO over Taiwan flight curbs", (0, 90, 140)),
    ("Beijing mobilises China-based voters for polls", (200, 60, 60)),
    ("Modi's Indo-Pacific vision at East Asia Summit", (220, 120, 20)),
    ("India re-elected to ITU Council for 2027–2030", (220, 120, 20)),
    ("Amazon plans $7bn green investment in India", (0, 130, 130)),
    ("Japan proposes Asian energy agency, oil storage", (180, 140, 20)),
    ("Deutsche Bank ignored warnings on risky clients", (90, 90, 100)),
    ("Investors slash tech, pile into gold — BofA poll", (34, 139, 34)),
    ("Salesforce leads S&P fallers amid tech jitters", (34, 139, 34)),
    ("Costco gains as shoppers stock up after outage", (150, 90, 40)),
    ("St Kitts ends citizenship scheme after EU threat", (0, 150, 150)),
    ("Canberra sanctions Israeli settlement expansion", (0, 60, 140)),
    ("Singapore non-oil exports jump 79.8% in October", (200, 40, 40)),
    ("Malaysia investments up 20.7% to RM350.4bn", (200, 170, 0)),
    ("Microsoft traces global outage to hidden July bug", (70, 110, 170)),
    ("WFP: one hot meal every two days in Gaza camps", (140, 140, 60)),
    ("UN: 372 civilians killed in Ukraine in October", (0, 90, 140)),
    ("UN confirms 2,230+ civilian deaths in Sudan", (150, 90, 40)),
    ("Jordan beat Australia 2–0 in final game of 2026", (230, 110, 20)),
    ("Celtic edge Dundee 2–1 after extra time in cup", (230, 110, 20)),
    ("Malaysia rout Guam 10–0 as Fazryel hits treble", (230, 110, 20)),
    ("Early voting opens in Victoria's state election", (110, 70, 160)),
]


# ------------------------------------------------------------- composition
def draw_tile(d, x, y, w, h, kicker, headline, deck, accent, art, art_h,
              head_size=25, deck_size=16):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                        outline=EDGE, width=2)
    art(d, x + 2, y + 2, w - 4, art_h)
    ty = y + art_h + 12
    d.text((x + 16, ty), kicker, font=fnt(BOLD, 15), fill=accent)
    # Shrink the headline until it fits on one line; never truncate it.
    size = head_size
    while size > 18 and d.textlength(headline, font=fnt(BOLD, size)) > w - 32:
        size -= 1
    head = fit_line(d, headline, fnt(BOLD, size), w - 32)
    d.text((x + 16, ty + 20), head, font=fnt(BOLD, size), fill=INK)
    sub = wrap_text(d, deck, fnt(REG, deck_size), w - 32)
    sy = ty + 20 + size + 9
    for line in sub[:2]:
        d.text((x + 16, sy), line, font=fnt(REG, deck_size), fill=GREY)
        sy += deck_size + 6


def draw_brief(d, x, y, col_w, items, row_h=23):
    """One column of one-line headlines, each led by a field dot."""
    for i, (headline, colour) in enumerate(items):
        ry = y + i * row_h
        d.ellipse([x, ry + 4, x + 10, ry + 14], fill=colour)
        text = fit_line(d, headline, fnt(BOLD, 16), col_w - 20)
        d.text((x + 18, ry), text, font=fnt(BOLD, 16), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)

    margin, gap = 12, 12
    cols = 3
    tw = (W - 2 * margin - (cols - 1) * gap) // cols

    # Lead row: three big illustrated tiles.
    lead_y, lead_h = 142, 240
    for i, (kicker, headline, deck, accent, art) in enumerate(LEAD):
        tx = margin + i * (tw + gap)
        draw_tile(d, tx, lead_y, tw, lead_h, kicker, headline, deck, accent,
                  art, art_h=116, head_size=25, deck_size=16)

    # Second row: three smaller illustrated tiles.
    row2_y, row2_h = 392, 240
    for i, (kicker, headline, deck, accent, art) in enumerate(SECOND):
        tx = margin + i * (tw + gap)
        draw_tile(d, tx, row2_y, tw, row2_h, kicker, headline, deck, accent,
                  art, art_h=104, head_size=22, deck_size=15)

    # The day in brief: 26 more stories, two columns of thirteen.
    d.rectangle([0, 642, W, 668], fill=NAVY)
    centred(d, W // 2, 648, "THE DAY IN BRIEF  ·  26 MORE STORIES",
            fnt(BOLD, 17), (255, 255, 255))
    half = (len(BRIEF) + 1) // 2
    col_w = (W - 2 * 12 - 12) // 2
    draw_brief(d, 12, 676, col_w, BRIEF[:half])
    draw_brief(d, 12 + col_w + 12, 676, col_w, BRIEF[half:])

    centred(d, W // 2, 996,
            "Sources: Reuters · AP · Al Jazeera · Nvidia · US DOJ · UN · Bernama · ABC",
            fnt(REG, 15), GREY)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
