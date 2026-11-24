#!/usr/bin/env python3
"""news-image-20261124-v2 — "THE WORLD TODAY", Tuesday 24 November 2026.

Sums up 24 November 2026 world news in one 1024x1024 image.

Python 3.12+ (stdlib only — no PIL). Own PNG encoder via zlib/struct.
Deterministic: two runs produce byte-identical output (no timestamps,
no randomness, fixed zlib level).

Usage: MAKEFUN_OUTPUT_DIR=out python3 main.py   -> writes entry.png
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER   = (245, 241, 232)
NAVY    = (20, 33, 61)
INK     = (24, 24, 24)
GREY    = (90, 90, 90)
RULE    = (180, 172, 155)
WHITE   = (255, 255, 255)
TEAL    = (14, 116, 110)
GREEN   = (34, 139, 60)
ORANGE  = (214, 92, 20)
BLUE    = (30, 90, 168)
RED     = (178, 34, 34)
PURPLE  = (106, 76, 147)
GOLD    = (201, 162, 39)

# ---------------------------------------------------------------- canvas
px = bytearray(PAPER * W * H)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = c


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, c)


def hline(x0, x1, y, c, t=1):
    for yy in range(y, y + t):
        for xx in range(x0, x1 + 1):
            set_px(xx, yy, c)


def vline(x, y0, y1, c, t=1):
    for xx in range(x, x + t):
        for yy in range(y0, y1 + 1):
            set_px(xx, yy, c)


def line(x0, y0, x1, y1, c, t=1):
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        for a in range(t):
            for b in range(t):
                set_px(x + a, y + b, c)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def circle(cx, cy, r, c, fill=False):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = (xx - cx) ** 2 + (yy - cy) ** 2
            if fill:
                if d <= r * r:
                    set_px(xx, yy, c)
            else:
                if r * r - 2 * r <= d <= r * r:
                    set_px(xx, yy, c)


def disc(cx, cy, r, c):
    circle(cx, cy, r, c, fill=True)


def tri(x0, y0, x1, y1, x2, y2, c):
    # filled triangle via scanlines
    pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = pts
    for y in range(ay, cy + 1):
        def interp(p, q):
            if q[1] == p[1]:
                return p[0]
            return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])
        if y <= by:
            xa, xb = interp((ax, ay), (bx, by)), interp((ax, ay), (cx, cy))
        else:
            xa, xb = interp((bx, by), (cx, cy)), interp((ax, ay), (cx, cy))
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            set_px(x, y, c)


# ---------------------------------------------------------------- 5x7 font
FONT = {
    'A': ("01110","10001","10001","11111","10001","10001","10001"),
    'B': ("11110","10001","10001","11110","10001","10001","11110"),
    'C': ("01110","10001","10000","10000","10000","10001","01110"),
    'D': ("11110","10001","10001","10001","10001","10001","11110"),
    'E': ("11111","10000","10000","11110","10000","10000","11111"),
    'F': ("11111","10000","10000","11110","10000","10000","10000"),
    'G': ("01110","10001","10000","10111","10001","10001","01111"),
    'H': ("10001","10001","10001","11111","10001","10001","10001"),
    'I': ("01110","00100","00100","00100","00100","00100","01110"),
    'J': ("00111","00010","00010","00010","00010","10010","01100"),
    'K': ("10001","10010","10100","11000","10100","10010","10001"),
    'L': ("10000","10000","10000","10000","10000","10000","11111"),
    'M': ("10001","11011","10101","10101","10001","10001","10001"),
    'N': ("10001","11001","10101","10011","10001","10001","10001"),
    'O': ("01110","10001","10001","10001","10001","10001","01110"),
    'P': ("11110","10001","10001","11110","10000","10000","10000"),
    'Q': ("01110","10001","10001","10001","10101","10010","01101"),
    'R': ("11110","10001","10001","11110","10100","10010","10001"),
    'S': ("01111","10000","10000","01110","00001","00001","11110"),
    'T': ("11111","00100","00100","00100","00100","00100","00100"),
    'U': ("10001","10001","10001","10001","10001","10001","01110"),
    'V': ("10001","10001","10001","10001","10001","01010","00100"),
    'W': ("10001","10001","10001","10101","10101","11011","10001"),
    'X': ("10001","10001","01010","00100","01010","10001","10001"),
    'Y': ("10001","10001","01010","00100","00100","00100","00100"),
    'Z': ("11111","00001","00010","00100","01000","10000","11111"),
    '0': ("01110","10001","10011","10101","11001","10001","01110"),
    '1': ("00100","01100","00100","00100","00100","00100","01110"),
    '2': ("01110","10001","00001","00110","01000","10000","11111"),
    '3': ("11111","00010","00100","00010","00001","10001","01110"),
    '4': ("00010","00110","01010","10010","11111","00010","00010"),
    '5': ("11111","10000","11110","00001","00001","10001","01110"),
    '6': ("00110","01000","10000","11110","10001","10001","01110"),
    '7': ("11111","00001","00010","00100","01000","01000","01000"),
    '8': ("01110","10001","10001","01110","10001","10001","01110"),
    '9': ("01110","10001","10001","01111","00001","00010","01100"),
    ' ': ("00000","00000","00000","00000","00000","00000","00000"),
    '-': ("00000","00000","00000","01110","00000","00000","00000"),
    ',': ("00000","00000","00000","00000","00100","00100","01000"),
    '.': ("00000","00000","00000","00000","00000","01100","01100"),
    "'": ("00100","00100","01000","00000","00000","00000","00000"),
    ':': ("00000","01100","01100","00000","01100","01100","00000"),
    '/': ("00001","00010","00010","00100","01000","01000","10000"),
    '(': ("00010","00100","01000","01000","01000","00100","00010"),
    ')': ("01000","00100","00010","00010","00010","00100","01000"),
    '&': ("01100","10010","10100","01000","10101","10010","01101"),
    '%': ("11001","11010","00010","00100","01000","01011","10011"),
    '+': ("00000","00100","00100","11111","00100","00100","00000"),
    '!': ("00100","00100","00100","00100","00100","00000","00100"),
    '?': ("01110","10001","00001","00110","00100","00000","00100"),
    '.': ("00000","00000","00000","00000","00000","01100","01100"),
}


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[' '])
        for r, row in enumerate(g):
            for cc, bit in enumerate(row):
                if bit == '1':
                    rect(cx + cc * scale, y + r * scale, scale, scale, c)
        cx += 6 * scale
    return cx


def draw_centered(y, s, scale, c, cx=W // 2):
    draw_text(cx - text_w(s, scale) // 2, y, s, scale, c)


def wrap(s, scale, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = s.split(' '), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if text_w(t, scale) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- pictograms
def pic_globe(x, y, s):
    # cracked globe: circle + latitude/longitude arcs + red crack
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 6
    circle(cx, cy, r, TEAL)
    circle(cx, cy, r - 8, TEAL)
    hline(cx - r, cx + r, cy, TEAL, 2)
    vline(cx, cy - r, cy + r, TEAL, 2)
    for (a, b) in [(cx - 26, cy - 30), (cx - 12, cy - 12), (cx - 22, cy + 4),
                   (cx - 6, cy + 18), (cx + 8, cy + 30)]:
        line(a, b, a + 12, b + 10, RED, 3)


def pic_chip(x, y, s):
    cx, cy = x + s // 2, y + s // 2
    rect(cx - 42, cy - 42, 84, 84, NAVY)
    rect(cx - 26, cy - 26, 52, 52, GREEN)
    rect(cx - 14, cy - 14, 28, 28, WHITE)
    for k in range(4):
        rect(cx - 42 + k * 22, cy - 54, 10, 12, NAVY)
        rect(cx - 42 + k * 22, cy + 42, 10, 12, NAVY)
        rect(cx - 54, cy - 42 + k * 22, 12, 10, NAVY)
        rect(cx + 42, cy - 42 + k * 22, 12, 10, NAVY)
    # rising arrow
    tri(cx + 34, cy - 58, cx + 22, cy - 34, cx + 46, cy - 34, GREEN)
    rect(cx + 29, cy - 36, 10, 34, GREEN)


def pic_fire(x, y, s):
    cx, cy = x + s // 2, y + s // 2
    # factory block
    rect(cx - 58, cy + 6, 116, 52, GREY)
    rect(cx - 58, cy + 6, 116, 8, INK)
    rect(cx + 34, cy - 34, 14, 40, GREY)
    disc(cx + 41, cy - 40, 12, (200, 200, 200))
    disc(cx + 30, cy - 48, 9, (200, 200, 200))
    # flame
    tri(cx - 26, cy + 6, cx - 4, cy - 46, cx + 18, cy + 6, ORANGE)
    tri(cx - 14, cy + 6, cx - 4, cy - 26, cx + 6, cy + 6, (255, 200, 40))


def pic_train(x, y, s):
    cx, cy = x + s // 2, y + s // 2
    rect(cx - 58, cy - 34, 116, 54, BLUE)
    rect(cx - 58, cy - 34, 116, 12, NAVY)
    for k in range(3):
        rect(cx - 48 + k * 38, cy - 14, 26, 18, WHITE)
    disc(cx - 34, cy + 28, 11, INK)
    disc(cx + 34, cy + 28, 11, INK)
    disc(cx - 34, cy + 28, 4, WHITE)
    disc(cx + 34, cy + 28, 4, WHITE)
    hline(cx - 66, cx + 66, cy + 44, INK, 3)
    hline(cx - 66, cx + 66, cy + 54, INK, 3)


def pic_drone(x, y, s):
    cx, cy = x + s // 2, y + s // 2 - 14
    line(cx - 34, cy - 26, cx + 34, cy + 26, INK, 4)
    line(cx + 34, cy - 26, cx - 34, cy + 26, INK, 4)
    for (rx, ry) in [(cx - 34, cy - 26), (cx + 34, cy - 26),
                     (cx - 34, cy + 26), (cx + 34, cy + 26)]:
        circle(rx, ry, 12, INK)
        disc(rx, ry, 3, INK)
    rect(cx - 14, cy - 10, 28, 20, RED)
    # damaged building below
    bx, by = cx - 52, cy + 44
    rect(bx, by, 104, 40, GREY)
    line(bx + 52, by, bx + 104, by + 20, INK, 3)
    rect(bx + 8, by + 12, 12, 14, NAVY)
    rect(bx + 84, by + 12, 12, 14, NAVY)


def pic_stage(x, y, s):
    cx, cy = x + s // 2, y + s // 2
    # speaker stack
    rect(cx - 58, cy - 44, 34, 62, INK)
    circle(cx - 41, cy - 26, 10, WHITE)
    circle(cx - 41, cy + 4, 7, WHITE)
    # cloud of substance
    disc(cx + 26, cy - 40, 16, (170, 170, 170))
    disc(cx + 44, cy - 30, 12, (190, 190, 190))
    disc(cx + 10, cy - 28, 10, (190, 190, 190))
    # crowd heads
    for k in range(5):
        disc(cx - 52 + k * 26, cy + 34, 9, PURPLE)


# ---------------------------------------------------------------- stories
STORIES = [
    # (kicker, accent, pic, headline, caption)
    ("CLIMATE", TEAL, pic_globe,
     "COP31 COLLAPSES", "NO DEAL IN ANTALYA"),
    ("TECH", GREEN, pic_chip,
     "HUANG BACK AT NVIDIA", "SHARES JUMP 30%"),
    ("DISASTER", ORANGE, pic_fire,
     "FACTORY FIRE KILLS 24", "DOZENS MISSING IN BANTEN"),
    ("TRANSPORT", BLUE, pic_train,
     "NEW INDIA-NEPAL TRAIN", "AYODHYA TO JANAKPUR"),
    ("WAR", RED, pic_drone,
     "DEADLY STRIKES HIT KYIV", "HOMES DESTROYED"),
    ("BRITAIN", PURPLE, pic_stage,
     "MANCHESTER ARENA CLEARED", "12,000 EVACUATED"),
]


def draw():
    # masthead
    rect(0, 0, W, 128, NAVY)
    draw_centered(18, "THE WORLD TODAY", 8, WHITE)
    rect(0, 96, W, 3, GOLD)
    draw_centered(106, "TUESDAY, 24 NOVEMBER 2026", 3, GOLD)

    # grid: 2 cols x 3 rows
    m, gap = 16, 16
    pw = (W - 2 * m - gap) // 2          # 488
    ph = (968 - 144 - 2 * gap) // 3      # 264
    for i, (kick, accent, pic, head, cap) in enumerate(STORIES):
        col, row = i % 2, i // 2
        px0 = m + col * (pw + gap)
        py0 = 144 + row * (ph + gap)
        rect(px0, py0, pw, ph, WHITE)
        rect(px0, py0, pw, 8, accent)
        # thin border
        hline(px0, px0 + pw - 1, py0 + ph - 1, RULE, 2)
        vline(px0, py0, py0 + ph - 1, RULE, 2)
        vline(px0 + pw - 1, py0, py0 + ph - 1, RULE, 2)
        draw_text(px0 + 18, py0 + 20, kick, 2, accent)
        # pictogram zone (left)
        pic(px0 + 14, py0 + 66, 160)
        # headline + caption (right of pictogram)
        tx = px0 + 184
        max_w = pw - 184 - 14
        y = py0 + 76
        for ln in wrap(head, 4, max_w):
            draw_text(tx, y, ln, 4, INK)
            y += 34
        y += 8
        for ln in wrap(cap, 3, max_w):
            draw_text(tx, y, ln, 3, GREY)
            y += 26

    # footer
    hline(16, W - 17, 984, RULE, 2)
    draw_centered(996, "SIX STORIES . ONE DAY . 24 NOVEMBER 2026", 2, GREY)


# ---------------------------------------------------------------- PNG encode
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def encode_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += px[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./out")
    os.makedirs(out_dir, exist_ok=True)
    draw()
    data = encode_png()
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
