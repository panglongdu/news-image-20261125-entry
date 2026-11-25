#!/usr/bin/env python3
"""Render the 25 Nov 2026 world-news front page as a 1024x1024 PNG.

Layout, top to bottom: a dark masthead carrying the title and date,
one lead article, two medium articles side by side, three short
articles in a row, and a footer strip listing four more items.
Each article is drawn by `article()`, which returns the y coordinate
just below it, so sections stack with a fixed gap and never collide.
"""
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BG = (13, 17, 25)
FG = (240, 234, 222)
SUB = (200, 205, 214)
DIM = (148, 156, 166)
FOOT = (22, 28, 38)
C_CHINA = (228, 58, 46)
C_TECH = (236, 172, 54)
C_US = (72, 176, 186)
C_ME = (96, 136, 216)
C_GAZA = (106, 186, 106)

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MARGIN = 40
GAP = 20

canvas = Image.new("RGB", (SIZE, SIZE), BG)
pen = ImageDraw.Draw(canvas, "RGBA")


def load(size, path=SANS_PATH):
    return ImageFont.truetype(path, size)


def flow(text, fnt, maxw):
    """Greedy wrap of `text` in font `fnt` to lines no wider than `maxw`."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pen.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def article(x, y, w, tag, accent, headline, head_px, deck, deck_px=23):
    """Draw one article block; return the y just below the block."""
    pen.line([x, y, x + w, y], fill=accent, width=5)
    pen.text((x, y + 12), tag, font=load(19, SANS_B_PATH), fill=accent)
    yy = y + 42
    hf = load(head_px, SANS_B_PATH)
    for ln in flow(headline, hf, w):
        pen.text((x, yy), ln, font=hf, fill=FG)
        yy += head_px + 7
    df = load(deck_px)
    for ln in flow(deck, df, w):
        pen.text((x, yy), ln, font=df, fill=SUB)
        yy += deck_px + 6
    return yy


# ---- masthead -------------------------------------------------------------
pen.rectangle([0, 0, SIZE, 118], fill=(6, 8, 12))
pen.text((MARGIN, 18), "THE WORLD IN ONE DAY",
         font=load(54, SERIF_PATH), fill=FG)
pen.text((MARGIN + 2, 84),
         "Wednesday, 25 November 2026  |  The day's news, in one picture",
         font=load(21), fill=DIM)
pen.rectangle([852, 22, 986, 96], outline=C_CHINA, width=3)
pen.text((878, 30), "25", font=load(34, SANS_B_PATH), fill=C_CHINA)
pen.text((870, 66), "NOV", font=load(19, SANS_B_PATH), fill=FG)
pen.line([0, 118, SIZE, 118], fill=C_CHINA, width=2)

# ---- lead article -----------------------------------------------------------
y = article(MARGIN, 140, SIZE - 2 * MARGIN, "CHINA", C_CHINA,
            "BEIJING PROBES TOP SHANGHAI OFFICIAL", 42,
            "China opens an investigation into Politburo member and Shanghai "
            "party chief Chen Jining — the most senior figure targeted in "
            "years.",
            25)

# ---- two medium articles ----------------------------------------------------
row_y = y + GAP
left_bottom = article(MARGIN, row_y, 456, "TECH", C_TECH,
                      "HUAWEI CONVICTED OF STEALING SECRETS", 30,
                      "A US jury finds the Chinese tech giant guilty of "
                      "stealing trade secrets, a verdict set to deepen the "
                      "tech standoff.", 23)
right_bottom = article(528, row_y, 456, "UNITED STATES", C_US,
                       "HUANG'S COMEBACK RALLY FADES", 30,
                       "Nvidia shares slide a day after Jensen Huang's "
                       "return as CEO; he tells staff he made 'some terrible "
                       "mistakes'.", 23)

# ---- three short articles ---------------------------------------------------
trio_y = max(left_bottom, right_bottom) + GAP
a_end = article(MARGIN, trio_y, 296, "MIDDLE EAST", C_ME,
                "RIYADH TOWER HIT AGAIN", 23,
                "Saudi Arabia condemns a 'terrorist attack' after its "
                "sovereign wealth fund skyscraper is struck twice in a "
                "week.", 21)
b_end = article(364, trio_y, 296, "GAZA", C_GAZA,
                "HAMAS SECURITY CHIEF KILLED", 23,
                "An Israeli air strike on Gaza City kills a senior Hamas "
                "security official, officials say.", 21)
c_end = article(688, trio_y, 296, "EUROPE", C_TECH,
                "NATO EYES SPACE THREAT", 23,
                "Allies respond to reports that Russia may launch a "
                "nuclear-armed satellite.", 21)

# ---- footer strip -----------------------------------------------------------
foot_y = max(a_end, b_end, c_end) + GAP
pen.rectangle([0, foot_y, SIZE, SIZE], fill=FOOT)
pen.text((MARGIN, foot_y + 14), "ALSO TODAY", font=load(19, SANS_B_PATH),
         fill=DIM)
extras = [
    "Trump awards Rudy Giuliani the Medal of Freedom",
    "Gunmen take 25 hostage at a supermarket in Colombia",
    "Shein to pay $100m to settle FTC deception claims",
    "Democrats turn their sights to 2028 after midterm triumph",
]
yy = foot_y + 40
for item in extras:
    pen.text((MARGIN, yy), item, font=load(21), fill=FG)
    yy += 28

canvas.save("/home/hatch/workspace/makefun/entry-news-image-1125/entry.png")
print("saved entry.png")
