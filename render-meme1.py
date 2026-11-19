#!/usr/bin/env python3
"""Render meme #1 untuk gta6-meme-x-01 (akun 5): kartu 'YOUR 13 YEARS IN WAITING'
gaya Spotify Wrapped. Teks tajam via PIL (bukan AI image) supaya terbaca di 480px.
Output: meme1.png (1080x1080). Logo hantu dari press kit resmi make.fun.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1080, 1080
ASSETS = os.path.expanduser('~/workspace/makefun/meme-x-assets')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meme1.png')

BG_TOP = (27, 16, 48)
BG_BOT = (13, 8, 24)
MAGENTA = (214, 51, 132)
MAGENTA_DARK = (178, 32, 108)
WHITE = (255, 255, 255)
LABEL = (158, 146, 172)
DIVIDER = (46, 36, 62)
SUB = (196, 188, 210)


def font(name, size):
    paths = [
        f'/usr/share/fonts/truetype/noto/NotoSans-{name}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans-{name}.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


# --- background: vertical gradient + soft magenta glows ---
img = Image.new('RGB', (W, H), BG_TOP)
px = img.load()
for y in range(H):
    t = y / H
    r = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
    g = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
    b = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
    for x in range(W):
        px[x, y] = (r, g, b)
glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-220, -220, 380, 380], fill=(214, 51, 132, 46))
gd.ellipse([760, 780, 1360, 1380], fill=(214, 51, 132, 36))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
d = ImageDraw.Draw(img)

MX = 64  # margin x
CW = W - 2 * MX  # content width

# --- header: ghost + make.fun ---
ghost = Image.open(os.path.join(ASSETS, 'mark-1024.png')).convert('RGBA')
ghost = ghost.resize((118, 118), Image.LANCZOS)
img.paste(ghost, (MX, 50), ghost)
d.text((MX + 138, 62), 'make.fun', font=font('Bold', 46), fill=WHITE)
d.text((MX + 138, 122), 'GTA VI  •  LAUNCH WEEK', font=font('Regular', 27), fill=LABEL)

# --- title ---
d.text((MX, 205), 'YOUR 13 YEARS', font=font('Black', 92), fill=WHITE)
d.text((MX, 300), 'IN WAITING', font=font('Black', 92), fill=MAGENTA)
d.text((MX, 408), 'GTA VI  •  LEONIDA  •  19 NOV 2026', font=font('Bold', 27), fill=SUB)

# --- stats ---
stats = [
    ('MINUTES WAITED', '6,837,480'),
    ('TOP SONG', 'Trailer theme on repeat'),
    ('DELAYS SURVIVED', '2'),
    ('PATIENCE LEFT', '0%'),
    ('SICK DAYS FILED', '2  ·  same excuse'),
]
y = 455
for label, value in stats:
    d.text((MX, y), label, font=font('Bold', 25), fill=LABEL)
    d.text((MX, y + 28), value, font=font('Bold', 44), fill=WHITE)
    y += 94
    if label != stats[-1][0]:
        d.line([(MX, y - 4), (W - MX, y - 4)], fill=DIVIDER, width=2)

# --- punchline bar ---
bar_y0, bar_y1 = 940, 1044
d.rounded_rectangle([(MX, bar_y0), (W - MX, bar_y1)], radius=22, fill=MAGENTA)
d.text((W // 2, bar_y0 + 14), 'WHILE YOU WAITED, MY AGENT EARNED $312.50',
       font=font('Bold', 33), fill=WHITE, anchor='ma')
d.text((W // 2, bar_y0 + 56), 'ON make.fun  —  REAL MONEY, REAL BOUNTIES.',
       font=font('Bold', 30), fill=WHITE, anchor='ma')

img.save(OUT, 'PNG')
print('saved', OUT, img.size, os.path.getsize(OUT), 'bytes')
