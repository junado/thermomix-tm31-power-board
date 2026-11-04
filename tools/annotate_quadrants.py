"""Annotate the solder-side quadrant photos (box coordinates are on a 1200x1600 preview).
Usage: python3 annotate_quadrants.py ../photos/04-solder-side ../images/annotated"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC, OUT = sys.argv[1], sys.argv[2]
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
RED, ORG, BLU, GRN, PUR, TEA = (225, 30, 30), (235, 130, 0), (25, 95, 230), (0, 140, 60), (150, 40, 180), (0, 140, 150)


def annotate(src, out, title, sub, items, legend):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1200, 1600))
    W, H = im.size
    pad = 640
    c = Image.new("RGB", (W + pad, H), "white")
    c.paste(im, (0, 0))
    d = ImageDraw.Draw(c)
    fb, ft, fr = ImageFont.truetype(F, 24), ImageFont.truetype(F, 21), ImageFont.truetype(FR, 18)
    for (x0, y0, x1, y1), lab, col in items:
        d.rectangle((x0, y0, x1, y1), outline=col, width=4)
        tw = d.textlength(lab, font=fb)
        by = y0 - 30 if y0 > 32 else y1 + 2
        d.rectangle((x0, by, x0 + tw + 10, by + 28), fill=col)
        d.text((x0 + 5, by + 1), lab, font=fb, fill="white")
    x, y = W + 18, 16
    d.text((x, y), title, font=fb, fill="black"); y += 34
    for line in sub:
        d.text((x, y), line, font=fr, fill=(90, 90, 90)); y += 24
    y += 10
    for col, head, rows in legend:
        d.rectangle((x, y + 4, x + 18, y + 22), fill=col)
        d.text((x + 26, y), head, font=ft, fill=col); y += 32
        for n, txt in rows:
            d.text((x + 4, y), n.rjust(2), font=ft, fill=col)
            d.text((x + 42, y + 2), txt, font=fr, fill="black"); y += 26
        y += 12
    c.save(out, quality=90)
    print(out, c.size)


SUB = ["Solder side (mirror image of the", "component side). Boxes are approximate", "areas, not exact pads."]

annotate(f"{SRC}/quadrant-A-cold-side-and-supply.jpg", f"{OUT}/solder-side-quadrant-A-cold-side-and-supply.jpg",
         "Quadrant A: front-panel link & supply", SUB,
         [((95, 235, 385, 690), "1", TEA), ((100, 285, 335, 345), "2", TEA), ((120, 360, 178, 535), "3", TEA),
          ((330, 600, 645, 850), "4", GRN), ((730, 640, 805, 675), "5", GRN), ((345, 895, 435, 1000), "6", GRN),
          ((150, 1040, 420, 1370), "7", GRN), ((388, 1118, 512, 1200), "8", GRN), ((528, 1328, 612, 1402), "9", GRN),
          ((640, 1040, 890, 1385), "10", BLU), ((815, 835, 1105, 1135), "11", BLU), ((505, 105, 775, 325), "12", PUR)],
         [(TEA, "ISOLATED (COLD) SIDE", [("1", "cold zone (black outline)"), ("2", "PC503 / PC501 / PC502 optos"),
                                          ("3", "CN300 front panel (5 pins)")]),
          (GRN, "LOW-VOLTAGE SUPPLY", [("4", "T100 flyback (D1D8A)"), ("5", "PC100 feedback opto"),
                                       ("6", "IC100 MIP2E3D area"), ("7", "bridge D100-D103, C110"),
                                       ("8", "L101 filter choke"), ("9", "F101 T1A fuse")]),
          (BLU, "MAINS INPUT", [("10", "CN100 + CX102 + R103-R105"), ("11", "L103 common-mode choke")]),
          (PUR, "ANALOG", [("12", "IC610 / IC611 / IC700 (SOIC-8)")])])

annotate(f"{SRC}/quadrant-B-mcu.jpg", f"{OUT}/solder-side-quadrant-B-mcu.jpg",
         "Quadrant B: MCU & logic", SUB,
         [((530, 230, 905, 690), "1", RED), ((555, 92, 785, 150), "2", BLU), ((268, 135, 352, 305), "3", BLU),
          ((272, 1028, 462, 1152), "4", RED), ((168, 1428, 442, 1600), "5", TEA), ((688, 1238, 1002, 1478), "6", PUR),
          ((830, 88, 950, 140), "7", BLU)],
         [(RED, "LOGIC", [("1", "IC1 uPD78F0034B (78K0, 64-QFP)"), ("4", "IC503 74HC(T)123 watchdog")]),
          (BLU, "CONNECTORS", [("2", "CN502 motor sensor board"), ("3", "CN503 flash programming 2x4"),
                               ("7", "ZD500 / Q508 sensor supply")]),
          (TEA, "LINK", [("5", "PC503 / PC501 / PC502 optos")]),
          (PUR, "ANALOG", [("6", "IC610 LM393, IC611 + IC700 TLC277")])])

annotate(f"{SRC}/quadrant-C-motor-drive.jpg", f"{OUT}/solder-side-quadrant-C-motor-drive.jpg",
         "Quadrant C: motor drive", SUB,
         [((292, 188, 388, 298), "1", RED), ((292, 488, 392, 592), "2", RED), ((478, 420, 582, 1135), "3", RED),
          ((838, 605, 1022, 1012), "4", BLU), ((560, 860, 762, 1112), "5", RED), ((150, 300, 262, 412), "6", ORG),
          ((605, 1178, 702, 1332), "7", GRN), ((735, 1178, 1012, 1362), "8", GRN), ((468, 1338, 602, 1552), "9", ORG)],
         [(RED, "POWER STAGE", [("1", "IC501 IR2106S (Q501/Q503)"), ("2", "IC502 IR2106S (Q502/Q504)"),
                                ("3", "IGBT / diode legs (heatsink)"), ("5", "freewheel diodes D500-D508")]),
          (BLU, "CONNECTOR", [("4", "CN501 to stator (6 fingers)")]),
          (ORG, "PROTECTION", [("6", "D512 / D513 trip diodes"), ("9", "R600 / R601 0.27 ohm shunts")]),
          (GRN, "DC BUS", [("7", "DB100 bridge (doubler)"), ("8", "C109 + balancing R118-R121")])])
