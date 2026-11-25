#!/usr/bin/env python3
"""Draw the 25 Nov 2026 world-news summary image (1024x1024 PNG).

A front-page layout: masthead with the date, one lead story, two
mid-size stories, three short stories and an "also today" strip.
Every story is drawn by a small helper that returns where it ends,
so blocks are stacked with fixed gaps and can never overlap.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
INK = (14, 18, 26)          # page background
PAPER = (238, 232, 220)     # headline colour
BODY = (203, 208, 216)      # body text colour
MUTED = (150, 158, 168)     # captions
RED = (226, 60, 48)
AMBER = (235, 170, 55)
TEAL = (70, 175, 185)
SKY = (95, 135, 215)
LEAF = (105, 185, 105)
STRIP = (24, 30, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img, "RGBA")

# faint dotted texture, like a stylised map, behind the stories
import random
random.seed(25)
for cx, cy, rx, ry in [(230, 320, 140, 80), (700, 260, 160, 90),
                       (480, 520, 120, 90), (820, 560, 90, 70)]:
    for _ in range(240):
        x = random.gauss(cx, rx / 1.8)
        y = random.gauss(cy, ry / 1.8)
        if 0 < x < W and 0 < y < H:
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(70, 88, 118, 100))


def wrap(text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def story(x, y, w, kicker, colour, headline, head_size, body, body_size=23):
    """Draw one story block; return the y just below it."""
    d.line([x, y, x + w, y], fill=colour, width=5)
    d.text((x, y + 12), kicker, font=font(BOLD, 19), fill=colour)
    yy = y + 40
    hf = font(BOLD, head_size)
    for ln in wrap(headline, hf, w):
        d.text((x, yy), ln, font=hf, fill=PAPER)
        yy += head_size + 7
    bf = font(PLAIN, body_size)
    for ln in wrap(body, bf, w):
        d.text((x, yy), ln, font=bf, fill=BODY)
        yy += body_size + 6
    return yy


# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 116], fill=(7, 9, 13))
d.text((34, 16), "THE WORLD IN ONE DAY", font=font(SERIF, 52), fill=PAPER)
d.text((36, 82), "Wednesday, 25 November 2026  •  The day's news, in one picture",
       font=font(PLAIN, 21), fill=MUTED)
d.rectangle([858, 20, 990, 96], outline=RED, width=3)
d.text((882, 28), "25", font=font(BOLD, 34), fill=RED)
d.text((874, 64), "NOV", font=font(BOLD, 19), fill=PAPER)

# ---- lead story -----------------------------------------------------------
y = story(34, 138, 956, "CHINA", RED,
          "BEIJING PROBES TOP SHANGHAI OFFICIAL", 42,
          "China opens an investigation into Politburo member and Shanghai "
          "party chief Chen Jining, the most senior figure targeted in years.",
          25)

# ---- middle row: two stories ---------------------------------------------
mid_y = y + 26
left_end = story(34, mid_y, 462, "TECH", AMBER,
                 "HUAWEI CONVICTED OF STEALING SECRETS", 30,
                 "A US jury finds the Chinese tech giant guilty of stealing "
                 "trade secrets, in a verdict set to deepen the tech standoff.",
                 23)
right_end = story(528, mid_y, 462, "UNITED STATES", TEAL,
                  "HUANG'S COMEBACK RALLY FADES", 30,
                  "Nvidia shares slide a day after Jensen Huang's return as "
                  "CEO; he tells staff he made 'some terrible mistakes'.",
                  23)

# ---- lower row: three short stories ---------------------------------------
low_y = max(left_end, right_end) + 26
a = story(34, low_y, 300, "MIDDLE EAST", SKY,
          "RIYADH TOWER HIT AGAIN", 23,
          "Saudi Arabia condemns a 'terrorist attack' after its sovereign "
          "wealth fund skyscraper is struck twice in a week.", 21)
b = story(362, low_y, 300, "GAZA", LEAF,
          "HAMAS SECURITY CHIEF KILLED", 23,
          "An Israeli air strike on Gaza City kills a senior Hamas security "
          "official, officials say.", 21)
c = story(690, low_y, 300, "EUROPE", AMBER,
          "NATO EYES SPACE THREAT", 23,
          "Allies respond to reports that Russia may launch a nuclear-armed "
          "satellite.", 21)

# ---- also today strip ------------------------------------------------------
strip_y = max(a, b, c) + 26
d.rectangle([0, strip_y, W, H], fill=STRIP)
d.text((34, strip_y + 14), "ALSO TODAY", font=font(BOLD, 19), fill=MUTED)
also = [
    "Trump awards Rudy Giuliani the Medal of Freedom",
    "Gunmen take 25 hostage at a supermarket in Colombia",
    "Shein to pay $100m to settle FTC deception claims",
    "Democrats turn their sights to 2028 after midterm triumph",
]
yy = strip_y + 44
for line in also:
    d.text((34, yy), line, font=font(PLAIN, 21), fill=PAPER)
    yy += 32

img.save("/home/hatch/workspace/makefun/entry-news-image-1125/entry.png")
print("saved entry.png")
