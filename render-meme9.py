#!/usr/bin/env python3
"""Render meme #9 untuk gta6-meme-x-01 (akun 1, pengganti #5 Fair Lantern):
Eviction Notice dari Leonida Housing Authority. Format dokumen resmi Leonida
(tagihan itemisasi + stempel PAID BY AI AGENT) mengikuti pola pemenang top 10
live 20 Nov 2026 07:37 WIB (kwitansi Steam, overdue notice perpustakaan, dll).
Teks tajam via PIL (bukan AI image) supaya terbaca di 480px.
Output: meme9.png (1080x1080). Logo hantu dari press kit resmi make.fun.
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1080, 1080
ASSETS = os.path.expanduser('~/workspace/makefun/meme-x-assets')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meme9.png')

PAPER = (247, 241, 220)
INK = (30, 25, 20)
RED = (192, 0, 0)
MAROON = (120, 20, 20)
MAGENTA = (214, 51, 132)
MUTED = (110, 100, 85)
PURPLE = (46, 26, 71)
WHITE = (255, 255, 255)


def serif(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSerif-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
    return ImageFont.truetype(p, size)


def mono(name, size):
    p = f'/usr/share/fonts/truetype/dejavu/DejaVuSansMono-{name}.ttf' if name else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    return ImageFont.truetype(p, size)


def sans(name, size):
    paths = [
        f'/usr/share/fonts/truetype/noto/NotoSans-{name}.ttf',
        f'/usr/share/fonts/truetype/dejavu/DejaVuSans-{name}.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new('RGB', (W, H), PURPLE)
d = ImageDraw.Draw(img)

# --- paper ---
d.rectangle([(36, 36), (1044, 1044)], fill=PAPER, outline=MAROON, width=4)
d.rectangle([(48, 48), (1032, 1032)], outline=MAROON, width=1)

MX = 78
RX = W - MX  # right edge of content

# --- header: ghost emblem + authority name ---
ghost = Image.open(os.path.join(ASSETS, 'mark-1024.png')).convert('RGBA')
ghost = ghost.resize((92, 92), Image.LANCZOS)
img.paste(ghost, (MX, 66), ghost)
d.text((MX + 112, 70), 'LEONIDA HOUSING AUTHORITY', font=serif('Bold', 38), fill=INK)
d.text((MX + 112, 124), 'VICE CITY BRANCH  •  EST. 2013', font=mono('', 22), fill=MUTED)

d.line([(MX, 182), (RX, 182)], fill=MAGENTA, width=3)

# --- title ---
d.text((W // 2, 198), 'EVICTION NOTICE', font=serif('Bold', 66), fill=RED, anchor='ma')
d.text((W // 2, 282), 'NOTICE NO. 000013  •  19 NOV 2026', font=mono('', 24), fill=INK, anchor='ma')
d.line([(MX, 326), (RX, 326)], fill=INK, width=2)

# --- tenant fields ---
d.text((MX, 344), 'TENANT:  ONE VERY PATIENT GAMER', font=mono('Bold', 27), fill=INK)
d.text((MX, 382), 'PROPERTY:  ONE COUCH, VICE CITY', font=mono('', 26), fill=INK)
d.text((MX, 420), 'OCCUPIED SINCE 17 SEP 2013  •  NEVER VACATED', font=mono('', 26), fill=INK)
d.text((MX, 462), 'DAYS ON THE COUCH:  4,811', font=mono('Bold', 32), fill=RED)

d.line([(MX, 516), (RX, 516)], fill=INK, width=2)

# --- itemized arrears with dotted leaders ---
items = [
    ('COUCH RENT \u2014 4,811 DAYS \u00d7 $1.00', '$4,811.00'),
    ('LATE FEE — DELAY No.1 + No.2 (WAIVED)', '$0.00'),
    ('NOISE COMPLAINTS — TRAILER 2, 87 VIEWS', '$0.00'),
    ('UNAUTHORIZED OCCUPANTS — JASON & LUCIA', '$0.00'),
    ('MISSING PROPERTY — 214 GB FAMILY PHOTOS', '$0.00'),
    ('PATIENCE DEPOSIT — FORFEITED', '$0.00'),
    ('REPLACEMENT COST — GTA VI', '$79.99'),
]
f_item = mono('', 24)
y = 534
for label, amt in items:
    lw = d.textlength(label, font=f_item)
    aw = d.textlength(amt, font=f_item)
    d.text((MX, y), label, font=f_item, fill=INK)
    d.text((RX, y), amt, font=f_item, fill=INK, anchor='ra')
    # dotted leader between label and amount
    dot_x0 = MX + lw + 14
    dot_x1 = RX - aw - 14
    dot_w = d.textlength('.', font=f_item)
    n = max(0, int((dot_x1 - dot_x0) / dot_w))
    d.text((dot_x0, y), '.' * n, font=f_item, fill=MUTED)
    y += 33

d.line([(MX, 778), (RX, 778)], fill=INK, width=2)

# --- total ---
d.text((MX, 792), 'TOTAL ARREARS DUE', font=serif('Bold', 34), fill=INK)
d.text((RX, 786), '$4,890.99', font=serif('Bold', 44), fill=RED, anchor='ra')
d.text((W // 2, 848), 'THE RENT COSTS MORE THAN THE GAME.', font=sans('Italic', 26), fill=RED, anchor='ma')

# --- PAID stamp (rotated layer) ---
stamp = Image.new('RGBA', (480, 88), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rectangle([(4, 4), (476, 84)], outline=RED, width=4)
sd.text((240, 10), 'PAID IN FULL', font=mono('Bold', 42), fill=RED, anchor='ma')
sd.text((240, 58), 'BY MY AI AGENT ON MAKE.FUN', font=mono('Bold', 19), fill=RED, anchor='ma')
stamp = stamp.rotate(4, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (W // 2 - stamp.width // 2, 872), stamp)

# --- footer ---
d.text((W // 2, 1002), "You can't evict someone who never left.", font=sans('Italic', 20), fill=MUTED, anchor='ma')

img.save(OUT, 'PNG')
print('saved', OUT, img.size, os.path.getsize(OUT), 'bytes')
