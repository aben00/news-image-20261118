#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: one infographic summing up
Wednesday 18 November 2026.

Renders a 1024x1024 PNG: a newspaper front page, "THE WORLD TODAY", with
six flat-illustration story tiles, each with a small drawn picture, a
headline and a one-line label, so the day reads from the image alone.

Run:  python3 draw.py            (writes entry.png next to this script)
Uses only Pillow and the DejaVu fonts present on this machine.
"""
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (19, 35, 63)
AMBER = (232, 163, 23)
PAPER = (247, 245, 240)
INK = (24, 28, 34)
GREY = (90, 96, 104)
CARD = (255, 255, 255)
BORDER = (214, 212, 206)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def center_text(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def burst(d, x, y, r, fill):
    """A starburst (explosion / interception flash) centred at (x, y)."""
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        r1 = r if ang % 60 == 0 else r * 0.6
        d.line([(x + 8 * math.cos(a), y + 8 * math.sin(a)),
                (x + r1 * math.cos(a), y + r1 * math.sin(a))],
               fill=fill, width=4)
    d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=(255, 200, 60))


def drone(d, x, y, s, body=(52, 60, 70)):
    """A small quadcopter drone seen from the side."""
    d.ellipse([x - s, y - s * 0.45, x + s, y + s * 0.45], fill=body)
    d.ellipse([x - s * 0.35, y - s * 0.2, x + s * 0.35, y + s * 0.2], fill=(30, 34, 40))
    for sx in (-1, 1):
        d.line([(x + sx * s, y - s * 0.3), (x + sx * s * 1.7, y - s * 0.55)],
               fill=(90, 96, 104), width=3)
        d.ellipse([x + sx * s * 1.7 - 10, y - s * 0.62, x + sx * s * 1.7 + 10,
                   y - s * 0.48], fill=(140, 148, 156))


# ---------------------------------------------------------------- header
def draw_header(d):
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=AMBER)
    center_text(d, W // 2, 16, "W E D N E S D A Y   1 8   N O V E M B E R   2 0 2 6",
                font(BOLD, 25), AMBER)
    center_text(d, W // 2, 50, "THE WORLD TODAY", font(BOLD, 64), (255, 255, 255))
    center_text(d, W // 2, 120, "Six stories that defined the day",
                font(REG, 22), (196, 205, 220))


# ---------------------------------------------------------------- tile art
def art_gulf(d, x, y, w, h):
    """Night over the Gulf: drones intercepted, radar dish, sea below."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 48))
    for sx, sy in ((26, 18), (80, 40), (250, 16), (296, 46), (180, 12), (130, 30)):
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    d.ellipse([x + w - 58, y + 10, x + w - 22, y + 46], fill=(245, 200, 90))
    # sea
    d.rectangle([x, y + 132, x + w, y + h], fill=(38, 74, 106))
    d.line([(x + 14, y + 152), (x + 90, y + 152)], fill=(255, 255, 255), width=3)
    d.line([(x + w - 120, y + 166), (x + w - 30, y + 166)], fill=(255, 255, 255), width=3)
    # radar dish on a rooftop at the left
    d.rectangle([x + 18, y + 118, x + 96, y + 132], fill=(90, 101, 112))
    d.polygon([(x + 30, y + 118), (x + 84, y + 118), (x + 96, y + 92),
               (x + 42, y + 92)], fill=(120, 132, 146))
    d.arc([x + 30, y + 58, x + 96, y + 118], start=200, end=340,
          fill=(200, 206, 212), width=6)
    d.line([(x + 63, y + 88), (x + 118, y + 52)], fill=(232, 163, 23), width=3)
    # two drones, one bursting as it is intercepted
    drone(d, x + 190, y + 62, 26)
    burst(d, x + 262, y + 44, 26, (235, 130, 40))
    drone(d, x + 150, y + 104, 20)
    # a small coastal skyline at the right
    for bx, bw, bh in ((w - 92, 30, 34), (w - 56, 24, 48), (w - 26, 18, 28)):
        d.rectangle([x + bx, y + 132 - bh, x + bx + bw, y + 132], fill=(70, 84, 100))
        for wy in range(y + 136 - bh, y + 126, 12):
            for wx in range(x + bx + 5, x + bx + bw - 5, 10):
                d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 220, 120))


def art_nvidia(d, x, y, w, h):
    """A green computer chip on a circuit board, with a rising chart."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 214))
    # circuit traces
    for ty in (34, 62, 150, 168):
        d.line([(x + 10, y + ty), (x + w - 10, y + ty)], fill=(140, 180, 140), width=3)
    for tx in (30, 70, 250, 290):
        d.line([(x + tx, y + 10), (x + tx, y + h - 10)], fill=(140, 180, 140), width=3)
    for cx, cy in ((30, 34), (70, 62), (250, 150), (290, 168), (30, 168), (290, 34)):
        d.ellipse([x + cx - 6, y + cy - 6, x + cx + 6, y + cy + 6], fill=(90, 140, 90))
    # the chip: dark square, green core, pins on all sides
    cx0, cy0, cs = x + w // 2 - 62, y + 44, 124
    for i in range(5):
        for px in (cx0 - 14, cx0 + cs + 8):
            d.rectangle([px, cy0 + 12 + i * 22, px + 6, cy0 + 26 + i * 22],
                        fill=(180, 186, 192))
        for py in (cy0 - 14, cy0 + cs + 8):
            d.rectangle([cx0 + 12 + i * 22, py, cx0 + 26 + i * 22, py + 6],
                        fill=(180, 186, 192))
    d.rectangle([cx0, cy0, cx0 + cs, cy0 + cs], fill=(30, 34, 40))
    d.rectangle([cx0 + 14, cy0 + 14, cx0 + cs - 14, cy0 + cs - 14], fill=(34, 139, 34))
    d.rectangle([cx0 + 30, cy0 + 30, cx0 + cs - 30, cy0 + cs - 30], fill=(46, 160, 46))
    center_text(d, x + w // 2, cy0 + 52, "$115.8B", font(BOLD, 26), (255, 255, 255))
    # rising arrow chart at the bottom
    pts = [(x + 24, y + 168), (x + 84, y + 150), (x + 140, y + 156),
           (x + 200, y + 128), (x + 262, y + 104), (x + 296, y + 92)]
    d.line(pts, fill=(178, 34, 34), width=5, joint="curve")
    d.polygon([(x + 296, y + 92), (x + 278, y + 88), (x + 288, y + 108)],
              fill=(178, 34, 34))


def art_quad(d, x, y, w, h):
    """Four flags — USA, India, Japan, Australia — over a round table."""
    d.rectangle([x, y, x + w, y + h], fill=(227, 236, 245))
    # table
    d.ellipse([x + 58, y + 122, x + w - 58, y + 170], fill=(146, 104, 66))
    d.rectangle([x + w // 2 - 12, y + 160, x + w // 2 + 12, y + h - 8], fill=(122, 84, 52))
    d.ellipse([x + 58, y + 116, x + w - 58, y + 160], fill=(176, 130, 84))
    # four flag poles: USA, India, Japan, Australia
    flag_defs = [
        ("US", [(178, 34, 34), (255, 255, 255)]),
        ("IN", [(255, 153, 51), (19, 136, 8)]),
        ("JP", [(255, 255, 255), (188, 0, 45)]),
        ("AU", [(0, 40, 104), (255, 255, 255)]),
    ]
    fx = [x + 34, x + 106, x + 178, x + 250]
    for (label, bands), fx0 in zip(flag_defs, fx):
        d.line([(fx0 + 20, y + 26), (fx0 + 20, y + 118)], fill=(80, 70, 60), width=4)
        d.rectangle([fx0, y + 26, fx0 + 40, y + 46], fill=bands[0])
        d.rectangle([fx0, y + 46, fx0 + 40, y + 66], fill=bands[1])
        if label == "US":
            for sy in (30, 40, 50, 60):
                d.rectangle([fx0, y + sy, fx0 + 40, y + sy + 4], fill=(178, 34, 34))
            d.rectangle([fx0, y + 26, fx0 + 17, y + 44], fill=(30, 50, 110))
        if label == "IN":
            d.rectangle([fx0, y + 46, fx0 + 40, y + 66], fill=(255, 255, 255))
            d.ellipse([fx0 + 14, y + 50, fx0 + 26, y + 62], outline=(0, 56, 147), width=2)
        if label == "JP":
            d.rectangle([fx0, y + 26, fx0 + 40, y + 66], fill=(255, 255, 255))
            d.ellipse([fx0 + 13, y + 36, fx0 + 27, y + 50], fill=(188, 0, 45))
        if label == "AU":
            d.rectangle([fx0, y + 26, fx0 + 40, y + 66], fill=(0, 40, 104))
            d.line([(fx0, y + 26), (fx0 + 40, y + 66)], fill=(255, 255, 255), width=3)
            d.line([(fx0 + 40, y + 26), (fx0, y + 66)], fill=(255, 255, 255), width=3)
    # four chairs around the table
    for cx0 in (x + 44, x + 118, x + 192, x + 266):
        d.rectangle([cx0, y + 132, cx0 + 40, y + 142], fill=(94, 80, 66))
        d.rectangle([cx0 + 3, y + 142, cx0 + 8, y + 168], fill=(58, 48, 40))
        d.rectangle([cx0 + 32, y + 142, cx0 + 37, y + 168], fill=(58, 48, 40))


def art_latvia(d, x, y, w, h):
    """Latvia's flag over a parliament chamber; a ballot box with a tick."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    # the Latvian flag: dark red, white, dark red
    d.rectangle([x + 24, y + 22, x + w - 24, y + 62], fill=(158, 27, 50))
    d.rectangle([x + 24, y + 62, x + w - 24, y + 82], fill=(255, 255, 255))
    d.rectangle([x + 24, y + 82, x + w - 24, y + 122], fill=(158, 27, 50))
    d.line([(x + 24, y + 22), (x + 24, y + 122)], fill=(80, 70, 60), width=4)
    # parliament benches: rows of seats
    for row, ry in enumerate((132, 150, 168)):
        for i in range(7):
            sx = x + 30 + i * 40
            col = (30, 122, 52) if (i + row) % 3 else (178, 34, 34)
            d.ellipse([sx, ry, sx + 22, ry + 12], fill=col)
    # ballot box with a green tick
    bx0, by0 = x + w - 96, y + 128
    d.rectangle([bx0, by0, bx0 + 72, by0 + 44], fill=(74, 85, 96))
    d.rectangle([bx0 - 6, by0 - 10, bx0 + 78, by0], fill=(52, 60, 70))
    d.rectangle([bx0 + 24, by0 - 14, bx0 + 48, by0 - 6], fill=(24, 28, 34))
    d.line([(bx0 + 18, by0 + 24), (bx0 + 32, by0 + 36), (bx0 + 56, by0 + 10)],
           fill=(46, 180, 90), width=6)


def art_merchant(d, x, y, w, h):
    """A courthouse with columns, a gavel, and prison bars."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    # courthouse: pediment, columns, steps
    bx = x + 18
    d.polygon([(bx, y + 62), (bx + 118, y + 22), (bx + 236, y + 62)], fill=(140, 148, 156))
    d.ellipse([bx + 106, y + 36, bx + 130, y + 60], fill=(232, 163, 23))
    d.rectangle([bx, y + 62, bx + 236, y + 72], fill=(120, 128, 136))
    for cx0 in range(4):
        cx = bx + 14 + cx0 * 56
        d.rectangle([cx, y + 72, cx + 20, y + 128], fill=(200, 206, 212))
        d.rectangle([cx - 4, y + 66, cx + 24, y + 74], fill=(180, 186, 192))
        d.rectangle([cx - 4, y + 128, cx + 24, y + 136], fill=(180, 186, 192))
    d.rectangle([bx, y + 136, bx + 236, y + 146], fill=(120, 128, 136))
    d.rectangle([bx - 8, y + 146, bx + 236 + 8, y + 154], fill=(100, 108, 116))
    # gavel resting on the steps, clear of the stamp
    gx, gy = bx + 168, y + 148
    d.rectangle([gx, gy - 6, gx + 52, gy + 6], fill=(122, 84, 52))
    d.line([(gx + 26, gy + 6), (gx + 38, gy + 24)], fill=(94, 66, 40), width=6)
    # prison bars at the right
    for i in range(4):
        bx2 = x + w - 84 + i * 18
        d.rectangle([bx2, y + 96, bx2 + 8, y + 172], fill=(52, 60, 70))
    d.rectangle([x + w - 90, y + 90, x + w - 12, y + 98], fill=(52, 60, 70))
    d.rectangle([x + w - 90, y + 168, x + w - 12, y + 176], fill=(52, 60, 70))
    # "27.5 YEARS" stamp
    d.rectangle([x + 22, y + 158, x + 138, y + 176], outline=(178, 34, 34), width=3)
    center_text(d, x + 80, y + 161, "27.5 YEARS", font(BOLD, 13), (178, 34, 34))


def art_cyclone(d, x, y, w, h):
    """A spiral cyclone over the Bay of Bengal, rain slanting down."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 219, 233))
    # sea
    d.rectangle([x, y + 120, x + w, y + h], fill=(96, 140, 168))
    # spiral arms of the cyclone
    cx, cy = x + w // 2, y + 78
    for ring, (r0, r1, col) in enumerate(((8, 44, (255, 255, 255)),
                                          (44, 74, (220, 232, 240)),
                                          (74, 100, (190, 210, 224)))):
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1],
              start=ring * 100, end=ring * 100 + 300, fill=col, width=16)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(38, 74, 106))
    # a small coastline at the bottom left
    d.polygon([(x, y + h), (x, y + 140), (x + 90, y + 132), (x + 120, y + 158),
               (x + 70, y + h)], fill=(120, 150, 110))
    # slanting rain
    for rx, ry in ((40, 30), (90, 16), (260, 26), (290, 44), (210, 14), (130, 44)):
        d.line([(x + rx, y + ry), (x + rx - 8, y + ry + 18)],
               fill=(120, 150, 180), width=3)
    # warning triangle on the sea
    tx, ty = x + w - 66, y + 132
    d.polygon([(tx, ty), (tx + 44, ty), (tx + 22, ty - 34)], fill=(232, 163, 23))
    d.rectangle([tx + 20, ty - 26, tx + 24, ty - 10], fill=(24, 28, 34))
    d.ellipse([tx + 20, ty - 8, tx + 24, ty - 4], fill=(24, 28, 34))


# ---------------------------------------------------------------- tiles
STORIES = [
    ("MIDDLE EAST · GULF", "DRONES OVER KUWAIT",
     "Kuwait intercepts hostile drones overnight; Bahrain sounds the all-clear.",
     (178, 34, 34), art_gulf),
    ("USA · BUSINESS", "NVIDIA DOUBLES SALES",
     "Revenue $115.8bn, up 103%, in its first report since Huang was ousted.",
     (34, 139, 34), art_nvidia),
    ("ASIA · DIPLOMACY", "QUAD MEETS IN MANILA",
     "First Quad leaders' summit since 2024; joint patrols and a business forum.",
     (0, 90, 140), art_quad),
    ("EUROPE · POLITICS", "LATVIA'S NEW GOVERNMENT",
     "Parliament approves Kulbergs' cabinet 57-34 ahead of Independence Day.",
     (158, 27, 50), art_latvia),
    ("USA · JUSTICE", "27 YEARS FOR TRUMP PLOT",
     "A judge sentences Iranian operative Asif Merchant to 330 months in prison.",
     (90, 110, 130), art_merchant),
    ("ASIA · WEATHER", "CYCLONE AKVAN STRENGTHENS",
     "The Bay of Bengal storm is likely to become a severe cyclone by Thursday.",
     (30, 122, 52), art_cyclone),
]


def draw_tile(d, x, y, w, h, kicker, headline, sub, accent, art):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=BORDER, width=2)
    art_h = 180
    art(d, x + 2, y + 2, w - 4, art_h)
    ty = y + art_h + 14
    d.text((x + 18, ty), kicker, font=font(BOLD, 17), fill=accent)
    hl = wrap(d, headline, font(BOLD, 30), w - 36)
    hy = ty + 26
    for line in hl:
        d.text((x + 18, hy), line, font=font(BOLD, 30), fill=INK)
        hy += 36
    sl = wrap(d, sub, font(REG, 20), w - 36)
    sy = hy + 6
    for line in sl[:3]:
        d.text((x + 18, sy), line, font=font(REG, 20), fill=GREY)
        sy += 26


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    margin, gap = 12, 12
    cols, rows = 3, 2
    tw = (W - 2 * margin - (cols - 1) * gap) // cols
    th = (984 - 164 - (rows - 1) * gap) // rows
    for i, (kicker, headline, sub, accent, art) in enumerate(STORIES):
        cx = i % cols
        cy = i // cols
        tx = margin + cx * (tw + gap)
        ty = 164 + cy * (th + gap)
        draw_tile(d, tx, ty, tw, th, kicker, headline, sub, accent, art)
    center_text(d, W // 2, 992, "Sources: Reuters, Al Jazeera, Nvidia, US DOJ, LSM  ·  Wednesday 18 November 2026",
                font(REG, 17), GREY)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
