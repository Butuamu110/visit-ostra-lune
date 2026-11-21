#!/usr/bin/env python3
"""OSTRA LUNE — The Tidal Moon Colony.
A vintage deco travel poster for a place that isn't there.

Draws a 1024x1024 poster with Pillow only. The only text in the image is
the place name, "OSTRA LUNE", set large in Playfair Display Black.
Composition leads the eye: name -> landmark (crescent island city +
rocket ferry) -> horizon (tide sea).

Palette: retro-futurist cream-blue.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
OUT = "/output/entry.png"

# Fonts live next to this script in the repo (relative to __file__), so the
# poster renders identically in the grader sandbox: no absolute paths.
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

# --- palette ---------------------------------------------------------------
NAVY = (22, 50, 74)          # deep navy (text, outlines)
NAVY_SOFT = (38, 74, 102)
CREAM = (242, 232, 213)      # sky top
SKY_MID = (216, 228, 232)
HORIZON = (168, 197, 212)
SEA_DEEP = (38, 96, 122)
SEA_MID = (64, 128, 152)
SEA_LIGHT = (127, 179, 200)
SAND = (233, 217, 174)
SAND_DARK = (201, 168, 106)
DOME = (245, 237, 216)
CORAL = (224, 120, 86)
GOLD = (217, 164, 65)
MOON = (247, 239, 201)
MOON_SHADE = (232, 220, 172)
ROCKET_BODY = (248, 244, 232)

random.seed(20261121)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(draw):
    """Cream sky melting into pale blue at the horizon (y ~ 700)."""
    for y in range(0, 701):
        if y < 340:
            t = y / 340.0
            c = lerp(CREAM, SKY_MID, t)
        else:
            t = (y - 340) / 360.0
            c = lerp(SKY_MID, HORIZON, t)
        draw.line([(0, y), (W, y)], fill=c)


def sea(draw):
    """Tide sea: deep teal gradient + wave strokes + moon reflection."""
    for y in range(700, H):
        t = (y - 700) / 324.0
        c = lerp(SEA_MID, SEA_DEEP, t)
        draw.line([(0, y), (W, y)], fill=c)
    # horizon shimmer
    draw.line([(0, 700), (W, 700)], fill=SEA_LIGHT, width=3)
    # wave arcs
    for row, y0 in enumerate((742, 792, 848, 908, 968)):
        for x0 in range(-40, W, 170):
            phase = (row * 53 + x0) % 170
            draw.arc([x0 + phase - 60, y0 - 14, x0 + phase + 60, y0 + 14],
                     start=200, end=340, fill=SEA_LIGHT, width=3)
    # moon reflection: wavy column of light under the moon (x ~ 770). Starts
    # below the island's bottom edge there (~861) so it never touches sand;
    # widths, gaps and centres vary so it reads as rippled water, not a ladder.
    rng = random.Random(11)
    y0 = 878
    while y0 < 1002:
        depth = (y0 - 878) / 124.0
        wdt = int(rng.uniform(24, 66) * (1 - 0.45 * depth))
        cx = 770 + rng.randint(-16, 16)
        col = (250, 240, 200) if rng.random() < 0.4 else (240, 226, 170)
        draw.line([(cx - wdt // 2, y0), (cx + wdt // 2, y0)],
                  fill=col, width=6)
        draw.ellipse([cx - wdt // 2 - 3, y0 - 3, cx - wdt // 2 + 3, y0 + 3],
                     fill=col)
        draw.ellipse([cx + wdt // 2 - 3, y0 - 3, cx + wdt // 2 + 3, y0 + 3],
                     fill=col)
        y0 += rng.randint(20, 30)


def stars(draw):
    for _ in range(90):
        x = random.randint(40, 984)
        y = random.randint(48, 330)
        r = random.choice([1, 1, 2, 2, 3])
        a = random.choice([NAVY_SOFT, GOLD, (255, 255, 255)])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=a)


def birds(draw):
    for (x, y, s) in [(180, 250, 14), (240, 210, 10), (300, 268, 12),
                      (830, 180, 11), (880, 230, 14)]:
        draw.arc([x - s, y - s // 2, x, y + s // 2], start=200, end=340,
                 fill=NAVY_SOFT, width=3)
        draw.arc([x, y - s // 2, x + s, y + s // 2], start=200, end=340,
                 fill=NAVY_SOFT, width=3)


def moon(base):
    """Big pale moon, upper right, with soft halo and craters."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([770 - 150, 300 - 150, 770 + 150, 300 + 150],
               fill=(247, 239, 201, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    d.ellipse([770 - 96, 300 - 96, 770 + 96, 300 + 96], fill=MOON,
              outline=NAVY, width=3)
    for (cx, cy, r) in [(730, 268, 16), (800, 330, 12), (760, 340, 9),
                        (812, 272, 7)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MOON_SHADE)


def clouds(base):
    """Soft deco clouds: blurred cream ellipses."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(layer)
    for (cx, cy, rx, ry) in [(200, 330, 120, 20), (330, 352, 90, 16),
                             (620, 210, 110, 18), (880, 430, 130, 20),
                             (150, 470, 100, 16)]:
        cd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                   fill=(255, 253, 244, 215))
    layer = layer.filter(ImageFilter.GaussianBlur(9))
    base.alpha_composite(layer)


def crescent_points():
    """Crescent island band: outer arc + inner arc, opening upward."""
    pts = []
    for deg in range(8, 173, 2):
        a = math.radians(deg)
        pts.append((512 + 340 * math.cos(a), 640 + 340 * math.sin(a)))
    for deg in range(172, 7, -2):
        a = math.radians(deg)
        pts.append((512 + 238 * math.cos(a), 560 + 238 * math.sin(a)))
    return pts


def island_top_y(x):
    """Top edge of the crescent band at column x.

    Inner-circle lower arc in the middle; on the tips (|dx| > 238) the edge
    is the straight segment joining the inner arc end to the outer arc end.
    """
    dx = x - 512
    if abs(dx) <= 238:
        return int(560 + math.sqrt(238 * 238 - dx * dx))
    # tip segment: inner end (512 +/- 235.7, 593.1) -> outer end (+/- 336.7, 687.3)
    s = 1 if dx > 0 else -1
    ix, iy = 512 + s * 235.7, 593.1
    ox, oy = 512 + s * 336.7, 687.3
    t = (x - ix) / (ox - ix)
    return int(iy + t * (oy - iy))


def building(draw, x, base_y, w, h, kind):
    """One retro-futurist building: dome, tower, or block with arched windows."""
    top = base_y - h
    if kind == "dome":
        draw.rectangle([x - w // 2, top + h // 3, x + w // 2, base_y],
                       fill=DOME, outline=NAVY, width=3)
        draw.pieslice([x - w // 2, top, x + w // 2, top + 2 * h // 3],
                      start=180, end=360, fill=DOME, outline=NAVY, width=3)
        draw.line([x, top - 16, x, top], fill=NAVY, width=3)
        draw.ellipse([x - 4, top - 22, x + 4, top - 14], fill=GOLD,
                     outline=NAVY, width=2)
        # arched windows
        for wx in (-w // 4, w // 4):
            draw.pieslice([x + wx - 6, base_y - 34, x + wx + 6, base_y - 18],
                          start=180, end=360, fill=NAVY)
            draw.rectangle([x + wx - 6, base_y - 26, x + wx + 6, base_y - 12],
                           fill=NAVY)
    elif kind == "tower":
        draw.rectangle([x - w // 2, top, x + w // 2, base_y],
                       fill=DOME, outline=NAVY, width=3)
        draw.polygon([(x - w // 2 - 4, top), (x, top - 34),
                      (x + w // 2 + 4, top)], fill=CORAL, outline=NAVY)
        draw.line([x, top - 52, x, top - 34], fill=NAVY, width=3)
        draw.ellipse([x - 7, top - 62, x + 7, top - 48], fill=GOLD,
                     outline=NAVY, width=2)
        for wy in range(top + 22, base_y - 10, 26):
            draw.rectangle([x - 4, wy, x + 4, wy + 12], fill=NAVY)
    else:  # block
        draw.rectangle([x - w // 2, top, x + w // 2, base_y],
                       fill=DOME, outline=NAVY, width=3)
        draw.rectangle([x - w // 2, top, x + w // 2, top + 10],
                       fill=CORAL, outline=NAVY, width=2)
        for wx in (-w // 4, w // 4):
            draw.pieslice([x + wx - 6, base_y - 30, x + wx + 6, base_y - 16],
                          start=180, end=360, fill=NAVY)
            draw.rectangle([x + wx - 6, base_y - 23, x + wx + 6, base_y - 10],
                           fill=NAVY)


def city(draw):
    """Retro-futurist city riding the crescent, plus a beacon on the tip."""
    specs = [
        (300, 62, 74, "dome"),
        (372, 52, 96, "block"),
        (438, 66, 118, "dome"),
        (512, 46, 176, "tower"),
        (586, 66, 118, "dome"),
        (652, 52, 96, "block"),
        (722, 58, 70, "dome"),
    ]
    for (x, w, h, kind) in specs:
        building(draw, x, island_top_y(x) + 6, w, h, kind)
    # beacon tower on the right crescent tip, foot sunk into the sand so it
    # stands on the island instead of floating above it
    bx, by = 788, island_top_y(788)
    draw.rectangle([bx - 12, by - 96, bx + 12, by + 14], fill=DOME,
                   outline=NAVY, width=3)
    draw.polygon([(bx - 16, by - 96), (bx, by - 122), (bx + 16, by - 96)],
                 fill=GOLD, outline=NAVY)
    draw.ellipse([bx - 9, by - 138, bx + 9, by - 120], fill=GOLD,
                 outline=NAVY, width=2)
    # tiny windows on the island band
    for (wx, wy) in [(340, 830), (470, 872), (600, 862), (700, 828)]:
        draw.ellipse([wx - 4, wy - 4, wx + 4, wy + 4], fill=NAVY)


def rot(pt, cx, cy, ang):
    a = math.radians(ang)
    x, y = pt[0] - cx, pt[1] - cy
    return (cx + x * math.cos(a) - y * math.sin(a),
            cy + x * math.sin(a) + y * math.cos(a))


def rocket(base):
    """Rocket ferry climbing off the island, smoke trail curling behind.

    Scaled ~1.2x and shifted left/up so the whole silhouette clears the
    central tower; smoke puffs overlap the tail instead of trailing detached.
    """
    # smoke trail on its own blurred layer
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    trail = [(472, 642), (448, 662), (418, 678), (384, 688), (348, 690),
             (310, 684), (272, 672)]
    for i, (sx, sy) in enumerate(trail):
        r = 30 - i * 2
        sd.ellipse([sx - r, sy - r, sx + r, sy + r],
                   fill=(255, 253, 245, 215))
    smoke = smoke.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(smoke)

    d = ImageDraw.Draw(base)
    # original design centre (448, 600); scale about it, then rotate about
    # the new centre so the rocket reads bigger and clear of the tower.
    S = 1.22
    OC = (448, 600)
    cx, cy, ang = 415, 575, -38

    def rp(p):
        sx = OC[0] + (p[0] - OC[0]) * S
        sy = OC[1] + (p[1] - OC[1]) * S
        return rot((sx, sy), cx, cy, ang)

    # flame
    flame = [(448, 648), (436, 622), (448, 668), (460, 622)]
    d.polygon([rp(p) for p in flame], fill=GOLD)
    inner = [(448, 640), (441, 622), (448, 650), (455, 622)]
    d.polygon([rp(p) for p in inner], fill=CORAL)
    # body: pointed nose + cylinder
    body = [(448, 520), (436, 560), (436, 620), (460, 620), (460, 560)]
    d.polygon([rp(p) for p in body], fill=ROCKET_BODY, outline=NAVY)
    # porthole
    px, py = rp((448, 566))
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=SEA_MID,
              outline=NAVY, width=3)
    # fins
    for s in (-1, 1):
        fin = [(436 if s < 0 else 460, 596),
               (436 if s < 0 else 460, 626),
               ((436 if s < 0 else 460) + s * 26, 632)]
        d.polygon([rp(p) for p in fin], fill=CORAL, outline=NAVY)
    # launch pad sitting on the island surface under the rocket
    d.rectangle([428, 776, 502, 788], fill=NAVY)
    d.rectangle([440, 766, 490, 776], fill=SAND_DARK, outline=NAVY, width=2)


def name_block(draw):
    """OSTRA LUNE, large and deliberate, with a deco rule beneath."""
    size = 150
    while size > 90:
        font = ImageFont.truetype(
            os.path.join(FONTS, "PlayfairDisplay-900.ttf"), size)
        # letter-spaced width
        tracking = int(size * 0.06)
        widths = [draw.textlength(ch, font=font) for ch in "OSTRA LUNE"]
        total = sum(widths) + tracking * (len(widths) - 1)
        if total <= 880:
            break
        size -= 6
    x = (W - total) / 2
    y = 66
    # soft cream plate behind the name so it reads over the sky
    draw.rounded_rectangle([x - 26, y - 14, x + total + 26, y + size + 22],
                           radius=18, fill=(250, 244, 228), outline=NAVY,
                           width=3)
    for ch, wch in zip("OSTRA LUNE", widths):
        draw.text((x, y), ch, font=font, fill=NAVY)
        x += wch + tracking
    # deco rule + diamond under the name
    ry = y + size + 44
    draw.line([(212, ry), (462, ry)], fill=NAVY, width=3)
    # right rule stops short of the moon (its left edge is ~x 683 at this y)
    draw.line([(562, ry), (655, ry)], fill=NAVY, width=3)
    draw.polygon([(512, ry - 9), (521, ry), (512, ry + 9), (503, ry)],
                 fill=GOLD, outline=NAVY)


def frame(draw):
    draw.rectangle([24, 24, W - 24, H - 24], outline=NAVY, width=5)
    draw.rectangle([38, 38, W - 38, H - 38], outline=NAVY, width=2)


def grain(img):
    """Fine risograph grain, subtle."""
    from PIL import ImageChops
    noise = Image.effect_noise((W, H), 16).convert("L")
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, noise_rgb, 0.045)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    sky_gradient(draw)
    stars(draw)
    birds(draw)
    base = img.convert("RGBA")
    moon(base)
    clouds(base)
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)
    sea(draw)
    # crescent island
    pts = crescent_points()
    draw.polygon(pts, fill=SAND, outline=NAVY)
    # sand shading along the lower edge
    draw.arc([512 - 340, 640 - 340, 512 + 340, 640 + 340], start=20,
             end=160, fill=SAND_DARK, width=10)
    city(draw)
    base = img.convert("RGBA")
    rocket(base)
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)
    name_block(draw)
    frame(draw)
    img = grain(img)
    os.makedirs("/output", exist_ok=True)
    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
