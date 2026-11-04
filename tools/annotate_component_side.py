from PIL import Image, ImageDraw, ImageFont
import sys
src, out = sys.argv[1], sys.argv[2]
from PIL import ImageOps
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
im.thumbnail((1200, 1600))  # box coordinates are on a 1200x1600 preview
W, H = im.size
pad = 560
canvas = Image.new("RGB", (W + pad, H), "white")
canvas.paste(im, (0, 0))
d = ImageDraw.Draw(canvas)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fb = ImageFont.truetype(F, 26)
ft = ImageFont.truetype(F, 22)
fr = ImageFont.truetype(FR, 19)

RED = (220, 30, 30)
BLU = (20, 90, 220)
GRN = (0, 140, 60)
PUR = (140, 40, 170)
ORG = (230, 120, 0)

# (box, label, color)
items = [
    ((50, 950, 120, 1110), "1", PUR),    # F100
    ((205, 1000, 275, 1070), "2", RED),  # PC700
    ((200, 1085, 285, 1135), "3", RED),  # CR700 triac
    ((285, 945, 395, 1085), "4", PUR),   # RY201
    ((405, 1045, 505, 1255), "5", RED),  # RY202
    ((315, 1140, 420, 1350), "6", RED),  # RY200
    ((115, 1140, 240, 1345), "7", RED),  # T700
    ((60, 1180, 125, 1300), "8", RED),   # CN703/CN704
    ((530, 970, 700, 1310), "9", BLU),   # L103 / EMI
    ((560, 1300, 720, 1345), "10", BLU), # CN100 BLACK
    ((690, 1030, 760, 1110), "11", BLU), # CN101 WHITE
    ((180, 590, 360, 940), "12", PUR),   # bulk caps
    ((380, 180, 485, 730), "13", PUR),   # power devices on heatsink
    ((225, 330, 280, 470), "14", PUR),   # CN501
    ((770, 870, 1000, 1060), "15", GRN), # SMPS transformer D1D8A
    ((840, 1100, 970, 1300), "16", GRN), # T101 flyback
    ((935, 680, 1070, 760), "17", ORG),  # PC501-503
    ((1015, 770, 1065, 890), "18", ORG), # CN300
    ((785, 160, 900, 205), "19", PUR),   # CN502
    ((975, 180, 1030, 280), "20", PUR),  # CN503
]
for (x0, y0, x1, y1), lab, col in items:
    d.rectangle((x0, y0, x1, y1), outline=col, width=4)
    tw = d.textlength(lab, font=fb)
    bx, by = x0, max(0, y0 - 32)
    d.rectangle((bx, by, bx + tw + 12, by + 30), fill=col)
    d.text((bx + 6, by + 1), lab, font=fb, fill="white")

# legend
x = W + 18
y = 18
d.text((x, y), "TM31 power board (120 V)", font=fb, fill="black"); y += 36
d.text((x, y), "Component side (rev. after full tracing)", font=fr, fill=(90, 90, 90)); y += 36

legend = [
    (RED, "HEATER", [
        ("2", "PC700  MOC3063 zero-cross opto-triac"),
        ("3", "CR700  heater triac (BTA, insulated tab)"),
        ("5", "RY202  neutral relay, Schrack 12 VDC"),
        ("6", "RY200  live relay, Schrack 12 VDC"),
        ("7", "T700  heater current transformer"),
        ("8", "CN704 / CN703  heater spade outputs"),
    ]),
    (BLU, "MAINS IN / EMI", [
        ("9", "L103 choke, CX102, CY103/104"),
        ("10", "CN100  BLACK (live)"),
        ("11", "CN101  WHITE (neutral)"),
    ]),
    (PUR, "MOTOR DC BUS + DRIVE", [
        ("1", "F100  T6.3 A motor-bus fuse"),
        ("4", "RY201  pre-charge bypass (899-1C)"),
        ("12", "2 x 680 uF 200 V, voltage doubler"),
        ("13", "IGBTs (G04N60) + diodes on heatsink"),
        ("14", "CN501  motor windings (6 fingers)"),
        ("19", "CN502  motor sensor board"),
        ("20", "CN503  MCU flash programming"),
        ("", "uPD78F0034B MCU on solder side"),
    ]),
    (GRN, "LOW-VOLTAGE SUPPLY", [
        ("15", "Flyback transformer T100 (D1D8A)"),
        ("16", "L101 filter choke + F101 1 A"),
    ]),
    (ORG, "ISOLATED LINK", [
        ("17", "PC501-503 opto-couplers"),
        ("18", "CN300  front panel (COLD side)"),
    ]),
]
for col, title, rows in legend:
    d.rectangle((x, y + 4, x + 18, y + 22), fill=col)
    d.text((x + 26, y), title, font=ft, fill=col); y += 32
    for n, txt in rows:
        if n:
            d.text((x + 6, y), n.rjust(2), font=ft, fill=col)
        d.text((x + 44, y + 2), txt, font=fr, fill="black"); y += 26
    y += 14

canvas.save(out, quality=92)
print(out, canvas.size)
