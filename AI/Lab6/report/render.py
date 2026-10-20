import os, textwrap
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/arqamwd/nust/AI/Lab6/report/img"
FDIR = "/usr/share/fonts/truetype/dejavu"
SIZE = 15
LH = 23
PAD = 16
GUT = 84
PAGE = (241, 243, 244)
CELL = (255, 255, 255)
BORDER = (218, 220, 224)
INK = (32, 33, 36)
GRAY = (95, 99, 104)
ACCENT = (26, 115, 232)

mono = ImageFont.truetype(f"{FDIR}/DejaVuSansMono.ttf", SIZE)
mono_b = ImageFont.truetype(f"{FDIR}/DejaVuSansMono-Bold.ttf", SIZE)
sans = ImageFont.truetype(f"{FDIR}/DejaVuSans.ttf", 13)

CW = mono.getlength("M")


def block(draw, x, y, w, label, lines, wrapw):
    h = PAD * 2 + len(lines) * LH
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CELL, outline=BORDER, width=1)
    if label:
        draw.text((x + PAD, y + PAD + 3), label, font=sans, fill=GRAY)
    for i, ln in enumerate(lines):
        draw.text((x + GUT, y + PAD + i * LH + 2), ln, font=mono, fill=INK)
    return h


def sanitize(line):
    return line.replace("\t", "    ").replace("\u22ee", "...")


def render(name, cells, width=None):
    all_lines = [sanitize(l) for c in cells for l in c["lines"]]
    longest = max([len(l) for l in all_lines] + [10])
    w = GUT + PAD * 2 + int(longest * CW) + PAD
    w = max(760, min(1280, w))
    avail = w - GUT - PAD * 2
    lim = int(avail / CW)
    prepared = []
    for c in cells:
        lines = []
        for l in [sanitize(x) for x in c["lines"]]:
            if len(l) > lim:
                lines.extend(textwrap.wrap(l, lim) or [""])
            else:
                lines.append(l)
        prepared.append((c.get("label"), lines))
    H = PAD + sum(PAD * 2 + len(l) * LH + 10 for _, l in prepared)
    im = Image.new("RGB", (w, H), PAGE)
    d = ImageDraw.Draw(im)
    y = PAD
    for label, lines in prepared:
        h = block(d, 10, y, w - 20, label, lines, avail)
        y += h + 10
    im.save(f"{OUT}/{name}.png")
    print(name, im.size)


def code(*lines, label="In [ ]:"):
    return {"kind": "code", "label": label, "lines": list(lines)}


def out(*lines):
    return {"kind": "out", "label": None, "lines": list(lines)}


def both(code_lines, out_lines, label="In [ ]:"):
    return [code(*code_lines, label=label), out(*out_lines)]
