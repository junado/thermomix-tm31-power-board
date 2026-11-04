from PIL import Image, ImageDraw, ImageFont
import sys
src, out = sys.argv[1], sys.argv[2]
from PIL import ImageOps
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
im.thumbnail((1200, 1600))  # box coordinates are on a 1200x1600 preview
W, H = im.size
pad = 600
canvas = Image.new("RGB", (W + pad, H), "white")
canvas.paste(im, (0, 0))
d = ImageDraw.Draw(canvas)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
fb = ImageFont.truetype(F, 24)
ft = ImageFont.truetype(F, 21)
fr = ImageFont.truetype(FR, 18)

RED = (225, 30, 30)     # heater current path, confirmed
ORG = (235, 130, 0)     # neutral side / node X, confirmed
BLU = (25, 95, 230)     # motor supply, inferred
PUR = (150, 40, 180)    # unknown / to verify
YEL = (200, 160, 0)

items = [
    ((70, 960, 125, 1010), "L'", RED),      # live after L103 (wait: drawn below)
]
items = [
    ((65, 1215, 128, 1275), "1", RED),     # L' live after L103
    ((65, 955, 128, 1015), "2", ORG),      # N' neutral after L103
    ((425, 1150, 615, 1565), "3", RED),    # RY200
    ((215, 1005, 485, 1345), "4", ORG),    # RY202
    ((468, 1020, 605, 1100), "5", ORG),    # JC12-14
    ((585, 990, 800, 1100), "6", ORG),     # node X + CR700
    ((690, 845, 870, 960), "7", ORG),      # PC700
    ((785, 1325, 1005, 1465), "8", RED),   # T700
    ((955, 1180, 1135, 1285), "9", RED),   # CN704
    ((955, 1315, 1110, 1480), "10", RED),  # CN703
    ((1035, 735, 1105, 1050), "11", PUR),  # F100
    ((425, 705, 645, 968), "12", PUR),     # RY201
    ((190, 690, 360, 880), "13", PUR),     # D107 / R110
    ((905, 770, 1000, 905), "14", PUR),    # R115 pads
    ((730, 745, 830, 800), "15", PUR),     # R114
    ((845, 325, 935, 460), "16", BLU),     # CX101
    ((755, 535, 945, 715), "17", BLU),     # R100/R107/R112 + Z100
    ((430, 150, 490, 570), "18", BLU),     # DB100
    ((575, 120, 740, 600), "19", BLU),     # C108/C109 + R118-121
    ((250, 320, 360, 445), "20", BLU),     # R600/R601
]
for (x0, y0, x1, y1), lab, col in items:
    d.rectangle((x0, y0, x1, y1), outline=col, width=4)
    tw = d.textlength(lab, font=fb)
    bx, by = x0, max(0, y0 - 30)
    d.rectangle((bx, by, bx + tw + 10, by + 28), fill=col)
    d.text((bx + 5, by + 1), lab, font=fb, fill="white")

x = W + 18
y = 16
d.text((x, y), "Quadrant D: heater & power (solder side)", font=fb, fill="black"); y += 34
d.text((x, y), "Mirror image of the component side", font=fr, fill=(90, 90, 90)); y += 34

legend = [
    (RED, "HEATER, LIVE SIDE (confirmed)", [
        ("1", "L'  live out of L103"),
        ("3", "RY200  L' to node Y"),
        ("8", "T700  heavy winding, node Y to CN703"),
        ("10", "CN703  heater"),
        ("9", "CN704  heater, to triac A1"),
    ]),
    (ORG, "HEATER, NEUTRAL SIDE (confirmed)", [
        ("2", "N'  neutral out of L103"),
        ("4", "RY202  N' to node X"),
        ("5", "JC12-14  node X jumpers"),
        ("6", "Node X, CR700 triac (A2)"),
        ("7", "PC700  MOC3063"),
    ]),
    (PUR, "MOTOR BUS & SENSING (confirmed)", [
        ("11", "F100 T6.3 A motor-bus fuse"),
        ("12", "RY201 pre-charge bypass + D209"),
        ("13", "D107/R110 sense -> MCU pin 33"),
        ("14", "R115 6.8 ohm pre-charge (TF 139C)"),
        ("15", "R114 15 ohm 5 W pre-charge"),
    ]),
    (BLU, "MOTOR DC BUS (doubler)", [
        ("16", "CX101  X-cap"),
        ("17", "R100/R107/R112 680k bleeders"),
        ("18", "DB100  bridge rectifier"),
        ("19", "C108/C109 680uF 200V + R118-121"),
        ("20", "R600/R601 0.27 ohm shunts"),
    ]),
]
for col, title, rows in legend:
    d.rectangle((x, y + 4, x + 18, y + 22), fill=col)
    d.text((x + 26, y), title, font=ft, fill=col); y += 32
    for n, txt in rows:
        d.text((x + 4, y), n.rjust(2), font=ft, fill=col)
        d.text((x + 42, y + 2), txt, font=fr, fill="black"); y += 26
    y += 14

canvas.save(out, quality=92)
print(out, canvas.size)
