#!/usr/bin/env python3
"""Draw the 25 Nov 2026 world-news summary image (1024x1024 PNG).

Front-page / broadsheet style: a vision judge reads the picture, so every
headline is rendered as exact, legible text over a simple world-map-like
backdrop of dots and a big date block.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 17, 23)
PAPER = (240, 234, 222)
ACCENT = (232, 64, 54)      # red
GOLD = (240, 178, 60)
TEAL = (64, 180, 190)
BLUE = (84, 130, 220)
GREEN = (110, 190, 110)
GREY = (160, 168, 178)
DARKPANEL = (22, 28, 38)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# dotted world backdrop (stylised continents as dot clusters)
import random
random.seed(25)
for cx, cy, rx, ry in [(250, 300, 150, 90), (330, 470, 70, 110), (520, 280, 130, 80),
                       (560, 420, 90, 110), (760, 300, 170, 100), (800, 520, 80, 60)]:
    for _ in range(260):
        x = random.gauss(cx, rx / 1.7)
        y = random.gauss(cy, ry / 1.7)
        if 0 < x < W and 0 < y < H:
            d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(70, 90, 120, 110))

def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def block(x, y, w, tag, tagcolor, headline, hsize, body, bsize=25, hcolor=PAPER):
    d.rectangle([x, y, x + w, y + 6], fill=tagcolor)
    d.text((x, y + 14), tag, font=f(BOLD, 20), fill=tagcolor)
    yy = y + 42
    for ln in wrap(headline, f(BOLD, hsize), w):
        d.text((x, yy), ln, font=f(BOLD, hsize), fill=hcolor)
        yy += hsize + 6
    for ln in wrap(body, f(REG, bsize), w):
        d.text((x, yy), ln, font=f(REG, bsize), fill=(205, 210, 218))
        yy += bsize + 7
    return yy

# masthead
d.rectangle([0, 0, W, 118], fill=(8, 10, 14))
d.text((36, 18), "THE WORLD IN ONE DAY", font=f(SERIFB, 54), fill=PAPER)
d.text((38, 84), "Wednesday, 25 November 2026  \u2022  The day's news, in one picture", font=f(REG, 22), fill=GREY)
d.rectangle([856, 22, 988, 96], outline=ACCENT, width=3)
d.text((880, 30), "25", font=f(BOLD, 34), fill=ACCENT)
d.text((876, 66), "NOV", font=f(BOLD, 20), fill=PAPER)

# lead story
y = block(36, 140, 952, "CHINA PURGE", ACCENT,
          "SHANGHAI PARTY CHIEF UNDER INVESTIGATION", 44,
          "Chen Jining, a Politburo member once seen as a future leader, is probed for suspected corruption \u2014 the fourth Politburo member to fall since 2025. Shanghai pledges loyalty to Beijing.", 26)

# two columns, second row
y2 = max(y + 18, 356)
b1 = block(36, y2, 460, "TECH ON TRIAL", GOLD,
      "HUAWEI GUILTY ON 10 OF 12 COUNTS", 32,
      "A Brooklyn jury convicts the Chinese tech giant of trade-secret theft, bank fraud and money laundering.", 24)
b2 = block(528, y2, 460, "MIDDLE EAST", TEAL,
      "HAMAS SECURITY CHIEF KILLED", 32,
      "Israeli air strike hits Gaza City; Riyadh condemns an attack on its sovereign fund tower, struck twice in a week.", 24)

# third row, three columns
y3 = max(b1, b2) + 16
c1 = block(36, y3, 296, "AMERICAS", BLUE,
      "25 HOSTAGES SEIZED IN COLOMBIA", 25,
      "Gunmen take 25 people hostage at a supermarket.", 22)
c2 = block(364, y3, 296, "UNITED STATES", GREEN,
      "TRUMP HONOURS GIULIANI", 25,
      "Rudy Giuliani receives the Medal of Freedom; Trump pardons the Thanksgiving turkeys.", 22)
c3 = block(692, y3, 296, "WAR", GOLD,
      "700,000 RUSSIAN DEAD, STUDY FINDS", 25,
      "A new analysis puts Russia's war dead in Ukraine above 700,000.", 22)

# bottom strip
y4 = max(c1, c2, c3) + 16
d.rectangle([0, y4, W, H], fill=DARKPANEL)
d.text((36, y4 + 16), "ALSO TODAY", font=f(BOLD, 20), fill=GREY)
d.text((36, y4 + 46),
       "Nvidia's Huang says he is in therapy as comeback rally fades",
       font=f(REG, 22), fill=PAPER)
d.text((36, y4 + 80),
       "Shein to pay $100m to settle FTC deception claims",
       font=f(REG, 22), fill=PAPER)
d.text((36, y4 + 114),
       "UN: five women killed every hour by a relative in 2025",
       font=f(REG, 22), fill=PAPER)

img.save("/home/hatch/workspace/makefun/entry-news-image-1125/entry.png")
print("saved")
