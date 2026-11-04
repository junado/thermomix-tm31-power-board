"""TM31 power board: wired schematic (rev 0.2). Usage: python3 tm31w.py OUTDIR [sheet ...]"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kisch2 import WSheet, box, make_lib, root_sheet, U  # noqa: E402

OUT = sys.argv[1]
ONLY = sys.argv[2:]
PROJ = "TM31_power_board"
L = make_lib()
R, C, CP, D, ZD = L["R"], L["C"], L["CP"], L["D"], L["ZD"]
NPN, PNP, IGBT = L["NPN"], L["PNP"], L["IGBT"]
root_uuid = U()
sheets = []


def new_sheet(title, fname, page, paper="A3"):
    s = WSheet(PROJ, title, fname, page, paper=paper, root_uuid=root_uuid, sheet_uuid=U())
    sheets.append(s)
    return s


def hdr(s, t, x, y):
    s.text(t, x, y, 1.7, bold=True)


def notes(s, text, x, y, size=1.2):
    s.text(text, x, y, size)


# ================================================================== 2. mains & heater
def sheet_mains():
    s = new_sheet("Mains input & heater", "mains_heater.kicad_sch", 2, paper="A4")
    YL, YN = 55.88, 76.2
    hdr(s, "MAINS INPUT & EMI FILTER", 15.24, 27.94)
    hdr(s, "MAINS RELAYS (contacts)", 86.36, 27.94)
    s.text("coils & drivers: sheet 'Safety logic'", 86.36, 31.4, 1.0, italic=True)
    hdr(s, "HEATER", 121.92, 27.94)
    cn100 = s.place(L["SPADE"], "CN100", "BLACK (live)", 17.78, YL,
                    fields=dict(ref=(17.78, YL - 3.6, "bottom"), val=(17.78, YL - 1.6, "bottom")))
    cn101 = s.place(L["SPADE"], "CN101", "WHITE (neutral)", 17.78, YN,
                    fields=dict(ref=(17.78, YN + 1.6, "top"), val=(17.78, YN + 3.6, "top")))
    cx = s.two(C, "CX102", "X2", (27.94, YL + 7.62), "down", fields="left")
    r103 = s.two(R, "R103", "?", (38.1, YL + 2.54), "down", fields="left")
    r104 = s.two(R, "R104", "?", r103.p("2"), "right", fields="above")
    r105 = s.two(R, "R105", "?", (50.8, r103.p("2")[1]), "down")
    ch = s.place(L["CHOKE"], "L103", "EMI choke", 66.04, YL + 10.16)
    s.w(cn100.p("1"), (27.94, YL), (38.1, YL), ch.p("L_IN"))
    s.w(cn101.p("1"), (27.94, YN), (50.8, YN), ch.p("N_IN"))
    s.w((27.94, YL), cx.p("1"))
    s.w(cx.p("2"), (27.94, YN))
    s.w((38.1, YL), r103.p("1"))
    s.w(r104.p("2"), r105.p("1"))
    s.w(r105.p("2"), (50.8, YN))
    # relays
    ry200 = s.place(L["RELAY_1A"], "RY200", "RTH34012WG", 93.98, YL, unit=1, note="live relay",
                    fields=dict(ref=(93.98, YL - 3.2, "bottom"), val=(93.98, YL + 2.6, "top")))
    ry202 = s.place(L["RELAY_1A"], "RY202", "RTH34012WG", 93.98, YN, unit=1, note="neutral relay (JC12-14)",
                    fields=dict(ref=(93.98, YN - 3.2, "bottom"), val=(93.98, YN + 2.6, "top")))
    s.w(ch.p("L_OUT"), (81.28, YL), ry200.p("COM"))
    s.w(ch.p("N_OUT"), (81.28, YN), ry202.p("COM"))
    s.w((81.28, YL), (81.28, 43.18), (78.74, 43.18))
    s.gl((78.74, 43.18), "L_F", 180)
    s.w((81.28, YN), (81.28, 88.9), (78.74, 88.9))
    s.gl((78.74, 88.9), "N_F", 180)
    s.text("to flyback\nsupply", 63.5, 38.0, 1.0, italic=True)
    s.text("to flyback\nsupply", 63.5, 91.4, 1.0, italic=True)
    # heater path
    ct = s.place(L["CT"], "T700", "HARTU 711078-51", 121.92, YL,
                 fields=dict(ref=(121.92, YL - 4.6, "bottom"), val=(121.92, YL - 2.6, "bottom")))
    s.w(ry200.p("NO"), (104.14, YL), ct.p("P1"))
    s.w((104.14, YL), (104.14, 43.18), (106.68, 43.18))
    s.gl((106.68, 43.18), "NODE_Y", 0)
    s.text("to F100 (motor bus)", 106.68, 38.0, 1.0, italic=True)
    s.w(ct.p("S1"), (119.38, 66.04))
    s.gl((119.38, 66.04), "CT_Q", 180)
    s.w(ct.p("S2"), (124.46, 66.04))
    s.gl((124.46, 66.04), "CT_P", 0)
    s.text("heater current\nto 'Analog sensing'", 112.0, 68.3, 0.9, italic=True)
    cn703 = s.place(L["SPADE2"], "CN703", "", 144.78, YL,
                    fields=dict(ref=(144.78, YL - 1.6, "bottom"), val=(144.78, YL + 1.6, "top")))
    cn704 = s.place(L["SPADE2"], "CN704", "", 144.78, YN,
                    fields=dict(ref=(144.78, YN - 1.6, "bottom"), val=(144.78, YN + 1.6, "top")))
    htr = s.two(L["HEATER"], "HTR1", "12.8 ohm", (160.02, YL + 3.81), "down", offboard=True)
    s.w(ct.p("P2"), cn703.p("1"), (160.02, YL), htr.p("1"))
    s.w(htr.p("2"), (160.02, YN), cn704.p("1"))
    s.frame(152.4, 48.26, 175.26, 83.82)
    s.text("BOWL (off-board)", 152.4, 45.2, 1.1, bold=True)
    tr = s.place(L["TRIAC"], "CR700", "BTA24-600BW", 132.08, YN,
                 fields=dict(ref=(132.08, YN - 3.6, "bottom"), val=(126.0, YN + 2.4, "right top")))
    s.text("insulated tab (BTA) only:\nheatsink is at VBUS", 112.0, 82.3, 0.9, italic=True)
    s.w(tr.p("A1"), cn704.p("1"))
    s.w(ry202.p("NO"), (104.14, YN), (114.3, YN), tr.p("A2"))
    s.w((104.14, YN), (104.14, 88.9), (106.68, 88.9))
    s.gl((106.68, 88.9), "NODE_X", 0)
    s.text("to pre-charge & RY201", 106.68, 91.4, 1.0, italic=True)
    # triac firing
    hdr(s, "TRIAC FIRING (MCU pin 51)", 15.24, 101.6)
    g = tr.p("G")
    r715 = s.two(R, "R715", "180", (g[0], g[1] + 2.54), "down", pin="2")
    r714 = s.two(R, "R714", "180", (g[0], r715.p("1")[1] + 2.54), "down", pin="2")
    s.w(g, r715.p("2"))
    s.w(r715.p("1"), r714.p("2"))
    opto = box("OPTOTRIAC", [("1", "A"), ("2", "K")], [("4", "MT4"), ("6", "MT6")], ref="PC", title="zero-cross")
    pc = s.place(opto, "PC700", "MOC3063", 101.6, 112.39)
    s.w(pc.p("MT4"), (114.3, pc.p("MT4")[1]), (114.3, YN))
    s.w(pc.p("MT6"), (g[0], pc.p("MT6")[1]), r714.p("1"))
    r713 = s.two(R, "R713", "?", (83.82, pc.p("A")[1] - 2.54), "up", pin="2", fields="left")
    s.w(pc.p("A"), (83.82, pc.p("A")[1]), r713.p("2"))
    s.pwr(r713.p("1"), "+5V")
    s.w(pc.p("K"), (76.2, pc.p("K")[1]))
    s.gl((76.2, pc.p("K")[1]), "HEAT_CMD", 180)
    s.text("from MCU pin 51 (P74)", 50.8, pc.p("K")[1] + 2.6, 1.0, italic=True)
    notes(s, """NOTES  (confirmed by continuity unless marked;  ? = value not read)
- CN100 = BLACK tab (live), CN101 = WHITE tab (neutral). CY103/CY104 Y-capacitors exist; their far ends were not traced (not drawn).
- RY200 switches live (L_F) to NODE_Y; RY202 switches neutral (N_F) to NODE_X through three parallel jumpers JC12-JC14.
  Both relays only close when the safety logic permits it.
- Heater path: L_F - RY200 - NODE_Y - T700 - CN703 - heater - CN704 - CR700 A1..A2 - NODE_X - RY202 - N_F. No fuse in the heater path.
- CR700 original marking unreadable (date code 409); replaced with BTA24-600BW after the A1 leg cracked in its C-bend (2026-10).
  Re-form the C-bend on replacement legs.  T700 secondary: S1/S2 order assumed.
- The TM31 only heats while a time is set and the blade turns.  120 V bowl: heater 12.8 ohm, NTC ~130 kohm at room temperature.""",
          15.24, 132.08, 1.1)
    return s


# ================================================================== 3. motor DC bus
def sheet_bus():
    s = new_sheet("Motor DC bus (doubler) & pre-charge", "motor_bus.kicad_sch", 3, paper="A4")
    YP = 71.12
    hdr(s, "PRE-CHARGE & BYPASS RELAY", 15.24, 27.94)
    hdr(s, "VOLTAGE DOUBLER (~340 V DC)", 96.52, 27.94)
    # pre-charge line
    s.gl((17.78, YP), "NODE_X", 180)
    s.text("from RY202", 10.16, YP + 2.6, 1.0, italic=True)
    r115 = s.two(R, "R115", "6.8 ohm 5 W", (30.48, YP), "right", fields="above",
                 note="thermal fuse 139 C inside")
    r114 = s.two(R, "R114", "15 ohm 5 W", (45.72, YP), "right", fields="above")
    s.w((17.78, YP), (25.4, YP), r115.p("1"))
    s.w(r115.p("2"), (40.64, YP), r114.p("1"))
    db = box("BRIDGE", [("2", "AC1"), ("3", "AC2")], [("1", "+"), ("4", "-")], ref="DB")
    dbp = s.place(db, "DB100", "SIP bridge", 101.6, YP + 1.27, note="AC pins tied")
    s.w(dbp.p("AC1"), (91.44, dbp.p("AC1")[1]), (91.44, YP), (91.44, dbp.p("AC2")[1]), dbp.p("AC2"))
    s.w(r114.p("2"), (81.28, YP), (91.44, YP))
    ry = s.place(L["RELAY_1C"], "RY201", "899-1C-F-C 12 V", 60.96, 50.8, rot=180, unit=1,
                 fields=dict(ref=(60.96, 44.6, "bottom"), val=(68.58, 56.0, "left top")),
                 note="pre-charge bypass")
    s.w(ry.p("COM"), (81.28, 50.8), (81.28, YP))
    s.w(ry.p("NO"), (25.4, ry.p("NO")[1]), (25.4, YP))
    s.text("coil: sheet 'Safety logic' (MCU pin 49)", 40.64, 62.0, 0.9, italic=True)
    # sense path
    s.w(ry.p("NC"), (50.8, ry.p("NC")[1]), (50.8, 38.1))
    d107 = s.two(D, "D107", "1N4007-type", (50.8, 38.1), "right", fields="above")
    r110 = s.two(R, "R110", "?", (60.96, 38.1), "right", fields="above")
    r111 = s.two(R, "R111", "?", (71.12, 38.1), "right", fields="above")
    s.w(d107.p("K"), r110.p("1"))
    s.w(r110.p("2"), r111.p("1"))
    rx1 = s.two(R, "RX1", "~10k", (83.82, 35.56), "up", note="9.87k measured")
    s.w(r111.p("2"), (83.82, 38.1), (88.9, 38.1))
    s.w((83.82, 38.1), rx1.p("1"))
    s.pwr(rx1.p("2"), "+5V")
    s.gl((88.9, 38.1), "AC_SENSE", 0)
    s.text("to MCU pin 33 (ANI0) via JD1", 88.9, 40.8, 1.0, italic=True)
    # doubler
    YV, YG = 50.8, 91.44
    s.w(dbp.p("+"), (111.76, dbp.p("+")[1]), (111.76, YV))
    s.w(dbp.p("-"), (114.3, dbp.p("-")[1]), (114.3, YG))
    c109 = s.two(CP, "C109", "680uF 200V", (127.0, 57.15), "down")
    c108 = s.two(CP, "C108", "680uF 200V", (127.0, 77.47), "down")
    r118 = s.two(R, "R118", "?", (139.7, 53.34), "down")
    r119 = s.two(R, "R119", "?", (139.7, 63.5), "down")
    r120 = s.two(R, "R120", "?", (139.7, YP + 2.54), "down")
    r121 = s.two(R, "R121", "?", (139.7, 83.82), "down")
    s.w((106.68, YV), (111.76, YV), (127.0, YV), (139.7, YV))
    s.pwr((106.68, YV), "VBUS")
    s.text("VBUS = heatsink potential!\nto motor stage", 84.0, 45.0, 1.0, italic=True)
    s.w((127.0, YV), c109.p("1"))
    s.w(c109.p("2"), (127.0, YP))
    s.w((127.0, YP), c108.p("1"))
    s.w(c108.p("2"), (127.0, YG))
    s.w((139.7, YV), r118.p("1"))
    s.w(r118.p("2"), r119.p("1"))
    s.w(r119.p("2"), (139.7, YP), r120.p("1"))
    s.w(r120.p("2"), r121.p("1"))
    s.w(r121.p("2"), (139.7, YG))
    s.w((114.3, YG), (127.0, YG), (139.7, YG))
    s.pwr((127.0, YG + 2.54), "GND")
    s.w((127.0, YG), (127.0, YG + 2.54))
    s.text("GND = bus negative\n= MCU ground", 116.84, 99.0, 1.0, italic=True)
    f100 = s.two(L["FUSE"], "F100", "T6.3AH 250V", (154.94, YP), "right", pin="2", note="motor fuse")
    s.w((127.0, YP), (139.7, YP), (149.86, YP), f100.p("2"))
    s.lb((133.35, YP), "MID")
    s.w(f100.p("1"), (167.64, YP))
    s.gl((167.64, YP), "NODE_Y", 0)
    s.text("from RY200", 167.64, YP + 2.6, 1.0, italic=True)
    # X cap and bleeders MID -> PRECH
    hdr(s, "BUS X-CAPACITOR & BLEEDERS", 15.24, 98.0)
    s.w((149.86, YP), (149.86, 104.14), (149.86, 114.3))
    cx101 = s.two(C, "CX101", "X2", (99.06, 104.14), "left", fields="above", note="MID-side lead assumed")
    s.w((149.86, 104.14), cx101.p("1"))
    s.w(cx101.p("2"), (40.64, 104.14))
    r100 = s.two(R, "R100", "680k", (127.0, 114.3), "left", fields="below")
    r107 = s.two(R, "R107", "680k", (116.84, 114.3), "left", fields="below")
    r112 = s.two(R, "R112", "680k", (106.68, 114.3), "left", fields="below")
    s.w((149.86, 114.3), r100.p("1"))
    s.w(r100.p("2"), r107.p("1"))
    s.w(r107.p("2"), r112.p("1"))
    s.w(r112.p("2"), (40.64, 114.3))
    s.w((40.64, YP), (40.64, 104.14), (40.64, 114.3))
    s.lb((40.64, 88.9), "PRECH", 0)
    notes(s, """NOTES  (? = value not read)
- 120 V version of a 230 V design: NODE_Y (live after RY200) feeds the capacitor midpoint MID through F100, and NODE_X (neutral after RY202) reaches
  BOTH AC pins of DB100 through R115 + R114. Result: VBUS ~340 V DC, the same bus as a 230 V board's bridge.
- Power-up (3 clicks): RY202 + RY200 close, C108/C109 charge through R115 + R114; RY201 then shorts them (COM to NO).
  At rest, RY201's NC contact routes DB100's AC node to D107 -> R110/R111 -> MCU pin 33, so the MCU can check the pre-charge voltage first.
- F100 open or R115 open: motor dead, heater still works.  Measure from GND (bus -) with a floating meter only.
- APPROXIMATE: pairing of balancing resistors R118-R121; CX101's MID-side lead. Not drawn: Z100 (unmarked, probably a varistor), R214.""",
          15.24, 124.46, 1.1)
    return s


# ================================================================== 4. motor stage
IR2106 = box("IR2106", [("1", "VCC"), None, ("2", "HIN"), None, ("3", "LIN"), None, ("4", "COM")],
             [("8", "VB"), None, ("7", "HO"), None, ("6", "VS"), None, ("5", "LO")], ref="IC")


def ir_driver(s, ref, X, Y, hin_lbl, rhin, lin_lbl, rlin, ho, vs, glo, rlo, dboot, cboot, dtrip, ytrip):
    ic = s.place(IR2106, ref, "IR2106S", X, Y)
    vcc, hin, lin, com = ic.p("VCC"), ic.p("HIN"), ic.p("LIN"), ic.p("COM")
    vb, hop, vsp, lo = ic.p("VB"), ic.p("HO"), ic.p("VS"), ic.p("LO")
    V = (X - 12.7, Y - 15.24)
    s.w(vcc, (X - 12.7, vcc[1]), V)
    s.pwr(V, "VGATE")
    db = s.two(D, dboot, "bootstrap (approx)", (X - 7.62, V[1]), "right", fields="above")
    s.w(V, db.p("A"))
    B = (X + 12.7, V[1])
    s.w(db.p("K"), B, (X + 12.7, vb[1]), vb)
    cb = s.two(CP, cboot, "bootstrap", (X + 15.24, V[1]), "right", fields="above")
    s.w(B, cb.p("1"))
    s.w(cb.p("2"), (X + 25.4, V[1]))
    s.lb((X + 25.4, V[1]), vs)
    s.w(hop, (X + 12.7, hop[1]))
    s.lb((X + 12.7, hop[1]), ho)
    s.w(vsp, (X + 12.7, vsp[1]))
    s.lb((X + 12.7, vsp[1]), vs)
    r = s.two(R, rlo, "470", (X + 10.16, lo[1]), "right", fields="below")
    s.w(lo, r.p("1"))
    s.w(r.p("2"), (X + 20.32, lo[1]))
    s.lb((X + 20.32, lo[1]), glo)
    Hn = (X - 17.78, hin[1])
    rh = s.two(R, rhin, "?", (X - 20.32, hin[1]), "left", pin="2", fields="above")
    s.w(hin, Hn, rh.p("2"))
    s.w(rh.p("1"), (X - 30.48, hin[1]))
    s.gl((X - 30.48, hin[1]), hin_lbl, 180)
    dt = s.two(D, dtrip, "", (X - 17.78, hin[1] - 2.54), "up", fields=dict(
        ref=(X - 19.8, hin[1] - 6.6, "right bottom"), val=(X - 19.8, hin[1] - 6.0, "right top")))
    s.w(Hn, dt.p("A"))
    s.w(dt.p("K"), (X - 17.78, ytrip))
    if rlin:
        rl = s.two(R, rlin, "?", (X - 10.16, lin[1]), "left", pin="2", fields="below")
        s.w(lin, rl.p("2"))
        s.w(rl.p("1"), (X - 20.32, lin[1]))
        s.gl((X - 20.32, lin[1]), lin_lbl, 180)
    else:
        s.w(lin, (X - 10.16, lin[1]))
        s.gl((X - 10.16, lin[1]), lin_lbl, 180)
    s.w(com, (X - 10.16, com[1]), (X - 10.16, com[1] + 2.54))
    s.pwr((X - 10.16, com[1] + 2.54), "GND")
    return (X - 17.78, ytrip)


def disc_driver(s, x0, y0, in_lbl, rb, rb_val, cs, qin, rpu, pu_note, qhi, qlo, rg, roff, doff, rpd, rpd_val,
                glbl, rx11=None):
    """Inverted discrete totem-pole gate driver (MCU high = IGBT off)."""
    q = s.place(NPN, qin, "BC846-type", x0, y0)
    s.w(q.p("E"), (x0 + 2.54, y0 + 7.62))
    s.pwr((x0 + 2.54, y0 + 7.62), "GND")
    rbase = s.two(R, rb, rb_val, (x0 - 7.62, y0), "left", pin="2", fields="above")
    A = (x0 - 17.78, y0)
    s.w((x0 - 20.32, y0), A, rbase.p("1"))
    s.gl((x0 - 20.32, y0), in_lbl, 180)
    c = s.two(C, cs, "speed-up", (x0 - 13.97, y0 + 5.08), "right", fields="below")
    s.w(A, (A[0], y0 + 5.08), c.p("1"))
    s.w(c.p("2"), (x0 - 6.35, y0 + 5.08), (x0 - 6.35, y0))
    s.w(rbase.p("2"), (x0 - 6.35, y0), q.p("B"))
    x1 = x0 + 20.32
    s.w(q.p("C"), (x0 + 2.54, y0 - 5.08), (x0 + 7.62, y0 - 5.08), (x1 - 7.62, y0 - 5.08))
    rp = s.two(R, rpu, "2.2k", (x0 + 7.62, y0 - 7.62), "up", pin="2", fields="left", note=pu_note)
    s.w((x0 + 7.62, y0 - 5.08), rp.p("2"))
    s.pwr(rp.p("1"), "VGATE")
    hi = s.place(NPN, qhi, "BC846-type", x1, y0 - 12.7)
    lo = s.place(PNP, qlo, "BC856-type", x1, y0 + 2.54)
    s.w(hi.p("B"), (x1 - 7.62, hi.p("B")[1]), (x1 - 7.62, y0 - 5.08), (x1 - 7.62, lo.p("B")[1]), lo.p("B"))
    s.w(hi.p("E"), (x1 + 2.54, y0 - 5.08), lo.p("E"))
    s.w(lo.p("C"), (x1 + 2.54, y0 + 10.16))
    s.pwr((x1 + 2.54, y0 + 10.16), "GND")
    top = (x1 + 2.54, y0 - 20.32)
    s.w(hi.p("C"), top)
    if rx11:
        r11 = s.two(R, rx11, "~33", (top[0], top[1] - 2.54), "up", pin="2", fields="left",
                    note="feed to both drivers")
        s.w(top, r11.p("2"))
        s.pwr(r11.p("1"), "VGATE")
    s.lb(top, "VGATE_D")
    x2 = x1 + 7.62
    s.w((x1 + 2.54, y0 - 5.08), (x2, y0 - 5.08))
    rgt = s.two(R, rg, "470", (x2 + 5.08, y0 - 5.08), "right", fields="above")
    s.w((x2, y0 - 5.08), rgt.p("1"))
    s.w((x2, y0 - 5.08), (x2, y0 + 2.54))
    dof = s.two(D, doff, "turn-off", (x2 + 12.7, y0 + 2.54), "left", fields="below")
    s.w((x2, y0 + 2.54), dof.p("K"))
    rof = s.two(R, roff, "47", (x2 + 15.24, y0 + 2.54), "right", pin="2", fields="below")
    s.w(dof.p("A"), rof.p("2"))
    x3 = x2 + 25.4
    s.w(rgt.p("2"), (x3, y0 - 5.08))
    s.w(rof.p("1"), (x3, y0 + 2.54), (x3, y0 - 5.08))
    s.w((x3, y0 - 5.08), (x3 + 5.08, y0 - 5.08), (x3 + 10.16, y0 - 5.08))
    s.lb((x3 + 10.16, y0 - 5.08), glbl)
    rpdp = s.two(R, rpd, rpd_val, (x3 + 5.08, y0 - 2.54), "down")
    s.w((x3 + 5.08, y0 - 5.08), rpdp.p("1"))
    s.w(rpdp.p("2"), (x3 + 5.08, y0 + 7.62), (x3 + 7.62, y0 + 7.62))
    s.gl((x3 + 7.62, y0 + 7.62), "LS_EMIT", 0)


def sheet_motor():
    s = new_sheet("Motor power stage (4-phase SR)", "motor_stage.kicad_sch", 4, paper="A3")
    YV, YM, YE = 50.8, 86.36, 121.92
    hdr(s, "POWER STAGE: 4-PHASE SWITCHED-RELUCTANCE MOTOR, SHARED HIGH-SIDE SWITCHES", 15.24, 27.94)
    s.text("phases (stator, 8.5 ohm each): CN501 1-3 and 1-5 share high side Q501;  2-4 and 2-6 share high side Q502",
           15.24, 32.0, 1.1, italic=True)
    cols = {  # x: (kind, top, bottom, mot, gate label)
        101.6: ("lo", "D500", "Q503", "MOT3", "G503"),
        134.62: ("hi", "Q501", "D504", "MOT1", "HO1"),
        167.64: ("lo", "D508", "Q500", "MOT5", "G500"),
        213.36: ("lo", "D506", "Q504", "MOT4", "G504"),
        246.38: ("hi", "Q502", "D505", "MOT2", "HO2"),
        279.4: ("lo", "D507", "Q505", "MOT6", "G505"),
    }
    ige = lambda c, yc: dict(ref=(c + 1.8, yc - 0.8, "left bottom"), val=(c + 1.8, yc + 0.8, "left top"))
    for c, (kind, top, bot, mot, gl) in cols.items():
        if kind == "hi":
            q = s.place(IGBT, top, "G04N60", c - 2.54, 68.58, fields=ige(c, 68.58))
            s.w((c, YV), q.p("C"))
            s.w(q.p("E"), (c, YM))
            s.w(q.p("G"), (c - 10.16, 68.58))
            s.lb((c - 10.16, 68.58), gl, 180)
            d = s.two(D, bot, "fast diode", (c, 107.95), "up")
            s.w(d.p("K"), (c, YM))
            s.w(d.p("A"), (c, 111.76))
            s.pwr((c, 111.76), "GND")
        else:
            d = s.two(D, top, "fast diode", (c, 72.39), "up")
            s.w((c, YV), d.p("K"))
            s.w(d.p("A"), (c, YM))
            q = s.place(IGBT, bot, "G04N60", c - 2.54, 104.14, fields=ige(c, 104.14))
            s.w((c, YM), q.p("C"))
            s.w(q.p("E"), (c, YE))
            s.w(q.p("G"), (c - 10.16, 104.14))
            s.lb((c - 10.16, 104.14), gl, 180)
        s.lb((c, YM - 5.08), mot, 0 if kind == "lo" else 180)
    xs = sorted(cols)
    s.w(*([(88.9, YV)] + [(x, YV) for x in xs]))
    s.pwr((88.9, YV), "VBUS")
    s.text("VBUS ~340 V DC", 76.2, 44.5, 1.0, italic=True)
    for ref, pin1_at, d, a, b in (("M1", 124.46, "left", 101.6, 134.62), ("M2", 144.78, "right", 134.62, 167.64),
                                  ("M3", 236.22, "left", 213.36, 246.38), ("M4", 256.54, "right", 246.38, 279.4)):
        m = s.two(L["WINDING"], ref, "phase 8.5 ohm", (pin1_at, YM), d, pin="1", offboard=True,
                  fields="above")
        lft, rgt = sorted([m.p("1"), m.p("2")])
        s.w((a, YM), lft)
        s.w(rgt, (b, YM))
    s.frame(107.95, 80.01, 161.29, 92.71)
    s.frame(219.71, 80.01, 273.05, 92.71)
    s.text("stator windings (off-board, via CN501)", 107.95, 94.0, 0.9, italic=True)
    s.text("stator windings (off-board, via CN501)", 219.71, 94.0, 0.9, italic=True)
    los = [x for x in xs if cols[x][0] == "lo"]
    r600 = s.two(R, "R600", "0.27 ohm", (297.18, YE + 2.54), "down")
    r601 = s.two(R, "R601", "0.27 ohm", (309.88, YE + 2.54), "down")
    s.w(*([(x, YE) for x in los] + [(297.18, YE), (309.88, YE), (320.04, YE)]))
    s.gl((320.04, YE), "LS_EMIT", 0)
    s.text("motor current sense\nto 'Analog sensing'", 320.04, YE + 2.6, 1.0, italic=True)
    for rr in (r600, r601):
        s.w((rr.p("1")[0], YE), rr.p("1"))
        s.pwr(rr.p("2"), "GND")
    cn = box("CONN_6", [(str(i), str(i)) if i else None for i in (1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6)], [],
             width=5.08, ref="CN")
    cnp = s.place(cn, "CN501", "to stator", 368.3, 76.2)
    for i in range(1, 7):
        pt = cnp.p(str(i))
        s.w(pt, (pt[0] - 5.08, pt[1]))
        s.lb((pt[0] - 5.08, pt[1]), f"MOT{i}", 180)
    # ---- drivers
    hdr(s, "HIGH/LOW-SIDE DRIVERS (Q501-Q504) & HARDWARE OVERCURRENT CUT-OFF", 15.24, 142.24)
    YT = 154.94
    t1 = ir_driver(s, "IC501", 88.9, 177.8, "P50_HIN1", "R510", "LIN1", None, "HO1", "MOT1", "G503", "RX2",
                   "D514", "C500", "D512", YT)
    t2 = ir_driver(s, "IC502", 180.34, 177.8, "P52_HIN2", "R511", "P53_LIN2", "R572", "HO2", "MOT2", "G504", "RX3",
                   "D517", "C506", "D513", YT)
    r535 = s.two(R, "R535", "?", (t2[0] + 5.08, YT), "right", fields="above")
    s.w((60.96, YT), t1, t2, r535.p("1"))
    s.gl((60.96, YT), "TRIP", 180)
    s.text("from IC610 (overcurrent)", 33.02, YT + 2.6, 1.0, italic=True)
    s.w(r535.p("2"), (r535.p("2")[0] + 2.54, YT))
    s.gl((r535.p("2")[0] + 2.54, YT), "P02_TRIP", 0)
    s.text("MCU pin 45 (INTP2)", r535.p("2")[0] + 2.54, YT - 4.2, 1.0, italic=True)
    s.text("MCU: pin 1 HIN1, 2 LIN1, 3 HIN2, 4 LIN2", 33.02, 205.0, 1.0, italic=True)
    hdr(s, "DISCRETE DRIVERS Q500 / Q505 (INVERTED)", 213.36, 142.24)
    disc_driver(s, 254.0, 177.8, "P55_DRV500", "R562", "30k", "CX1", "Q507", "RX4", "via JA7", "Q512", "Q513",
                "RX5", "RX6", "D511", "RX7", "10k", "G500", rx11="RX11")
    disc_driver(s, 254.0, 226.06, "P54_DRV505", "RX8", "~30k", "CX2", "Q511", "RX9", "via JB5", "Q510", "Q514",
                "RX10", "RX12", "DX2", "R517", "~10k", "G505")
    s.text("MCU pin 6", 220.98, 180.4, 1.0, italic=True)
    s.text("MCU pin 5", 220.98, 228.7, 1.0, italic=True)
    notes(s, """NOTES  (? = value not read)
- IGBTs Q500-Q505: G04N60 (Infineon SGP04N60-type, 600 V). Low-side emitters (LS_EMIT) return to GND through R600 // R601 (0.27 ohm each).
- Freewheel diodes all ~0.475 V in diode mode. IR2106 supply VGATE exists only while the safety logic enables Q205/Q206: a firmware crash or a refused
  permit removes ALL gate drive.  Discrete drivers: MCU pin high = IGBT off; turn-on through 470 ohm, fast turn-off through 47 ohm + diode.
- Hardware overcurrent cut-off: IC610 pulls TRIP low; D512/D513 force both HIN inputs low (high sides off without firmware) and interrupt the MCU (pin 45).
- APPROXIMATE: bootstrap diodes (D514/D517 drawn; D518/D519 also exist); HO gate resistors and Q503/Q504 gate pull-downs not traced;
  the ~33 ohm feed RX11 may be two resistors; DX2 = turn-off diode of Q505 (reference not read).""",
          15.24, 238.76, 1.1)
    return s


# ================================================================== 5. safety logic
def make_hc123():
    def unit(n):
        a, b, clr, q_, nq, cx, rcx = {1: ("1", "2", "3", "13", "4", "14", "15"),
                                      2: ("9", "10", "11", "5", "12", "6", "7")}[n]
        bx = box("X", [(clr, f"~{{{n}CLR}}"), None, (a, f"{n}A"), None, (b, f"{n}B")],
                 [(q_, f"{n}Q"), None, None, None, (nq, f"~{{{n}Q}}")],
                 width=30.48, top=[(cx, f"{n}Cx"), None, (rcx, f"{n}Rx/Cx")])
        return bx.units[0], bx.body
    u1, body = unit(1)
    u2, _ = unit(2)
    from kisch2 import Sym, rect as krect, P as KP
    pw = ([krect(-1.905, 2.54, 1.905, -2.54)],
          [KP("16", "VCC", 0, 5.08, 270, 2.54, "power_in"), KP("8", "GND", 0, -5.08, 90, 2.54, "power_in")])
    s = Sym("74HC123", [u1, u2, pw], show_names=True, show_numbers=True, ref="IC")
    s.body = body
    s.power_unit = 3
    return s


HC123 = make_hc123()


def relay_driver(s, AX, AY, coil_ref, flyback, q, emit_d, diodes, pull, pull_val, en_r):
    """Diode-AND gate (bus at x=AX), NPN relay driver, coil and flyback. diodes: [(ref, label, global?)]."""
    rp = s.two(R, pull, pull_val, (AX, AY), "up", pin="2", fields="left")
    s.pwr(rp.p("1"), "V12RAW")
    pts = [(AX, AY)]
    for i, (ref, lbl, glob) in enumerate(diodes):
        y = AY + 5.08 * (i + 1)
        d = s.two(D, ref, "", (AX, y), "left", fields=dict(ref=(AX - 3.81, y - 1.2, "bottom"), val=(AX - 3.81, y + 1.2, "top")))
        s.w(d.p("K"), (AX - 10.16, y))
        (s.gl if glob else s.lb)((AX - 10.16, y), lbl, 180)
        pts.append((AX, y))
    yb = AY + 25.4
    pts += [(AX, yb), (AX, yb + 10.16)]
    s.w(*pts)
    s.lb((AX, AY + 22.86), "AND1" if len(diodes) == 4 else "AND2")
    qq = s.place(NPN, q, "BC846-type", AX + 10.16, yb)
    s.w((AX, yb), qq.p("B"))
    xc = AX + 12.7
    coil = s.place(L["RELAY_1A"], coil_ref, "12 V coil", xc, AY + 7.62, unit=2)
    T = (xc, AY - 2.54)
    s.w(coil.p("A1"), T, (xc + 7.62, T[1]))
    s.pwr(T, "V12RAW")
    fb = s.two(D, flyback, "flyback", (xc + 7.62, AY + 11.43), "up")
    s.w((xc + 7.62, T[1]), fb.p("K"))
    lo = (xc, AY + 15.24)
    s.w(coil.p("A2"), lo, qq.p("C"))
    s.w(fb.p("A"), (xc + 7.62, lo[1]), lo)
    de = s.two(D, emit_d, "", (xc, yb + 7.62), "down", note="emitter diode")
    s.w(qq.p("E"), de.p("A"))
    s.lb(de.p("A"), "Q_EMIT", 0)
    s.pwr(de.p("K"), "GND")
    re = s.two(R, en_r, "47k", (AX, yb + 10.16), "down", fields="left")
    return re.p("2")


def sheet_safety():
    s = new_sheet("Safety logic (relay permits, watchdog, gate-drive enable)", "safety_logic.kicad_sch", 5, paper="A3")
    hdr(s, "MAINS RELAY PERMITS (diode-AND gates)", 15.24, 27.94)
    s.text("a relay closes only if EVERY input is high; any input low drops the AND node", 15.24, 32.0, 1.0, italic=True)
    e1 = relay_driver(s, 50.8, 53.34, "RY202", "D223", "Q200", "D225",
                      [("D213", "WD1", False), ("D212", "WD2", True), ("D222", "PERMIT1", True),
                       ("D210", "PERMIT2", True)], "R206", "47k", "RX15")
    e2 = relay_driver(s, 116.84, 53.34, "RY200", "D224", "Q204", "D226",
                      [("D215", "WD2", True), ("D221", "PERMIT1", True), ("DX3", "PERMIT2", True)],
                      "RX14", "47k", "RX16")
    s.text("RY202 = NEUTRAL relay", 66.04, 44.5, 1.0, bold=True)
    s.text("RY200 = LIVE relay", 132.08, 44.5, 1.0, bold=True)
    s.text("DX3 = unnumbered", 83.82, 72.0, 0.9, italic=True)
    # VGATE enable
    YE = 111.76
    s.w(e1, (e1[0], YE), (e2[0], YE))
    s.w(e2, (e2[0], YE))
    s.lb((80.0, YE), "EN_M")
    r17 = s.two(R, "RX17", "47k", (e2[0] + 17.78, YE), "right", fields="above")
    s.w((e2[0], YE), r17.p("1"))
    gd = (r17.p("2")[0] + 2.54, YE)
    q205 = s.place(NPN, "Q205", "BC846-type", gd[0] + 7.62, YE)
    s.w(r17.p("2"), gd, q205.p("B"))
    s.w(gd, (gd[0], YE + 7.62), (gd[0] - 2.54, YE + 7.62))
    s.gl((gd[0] - 2.54, YE + 7.62), "GD_EN", 180)
    s.text("MCU pin 16 (P35)", gd[0] - 22.0, YE + 10.2, 1.0, italic=True)
    s.w(q205.p("E"), (q205.p("E")[0], YE + 7.62))
    s.pwr((q205.p("E")[0], YE + 7.62), "GND")
    xq = q205.p("C")[0]
    r213 = s.two(R, "R213", "6.2k", (xq, q205.p("C")[1] - 2.54), "up", fields="left")
    s.w(q205.p("C"), r213.p("1"))
    q206 = s.place(PNP, "Q206", "BC856-type", xq + 15.24, 86.36)
    s.w(r213.p("2"), (xq, 86.36), q206.p("B"))
    nb = (xq + 5.08, 86.36)
    r212 = s.two(R, "R212", "470", (nb[0], 83.82), "up", pin="2", fields="left")
    s.w(nb, r212.p("2"))
    top = (nb[0], 73.66)
    s.w(r212.p("1"), top, (q206.p("E")[0], 73.66), q206.p("E"))
    s.pwr(top, "V12RAW")
    out = (q206.p("C")[0], 99.06)
    s.w(q206.p("C"), out, (out[0] + 5.08, 99.06))
    s.pwr((out[0] + 5.08, 99.06), "VGATE")
    s.text("VGATE (switched gate-drive supply):\nIR2106 VCC via JA2, discrete drivers,\nIC611", out[0] + 8.0, 96.0, 1.0,
           italic=True)
    hdr(s, "GATE-DRIVE SUPPLY ENABLE", 190.5, 111.76)
    # RY201 driver
    hdr(s, "PRE-CHARGE BYPASS RELAY", 236.22, 27.94)
    x0 = 256.54
    q202 = s.place(NPN, "Q202", "BC846-type", x0, 78.74)
    xc = x0 + 2.54
    coil = s.place(L["RELAY_1C"], "RY201", "12 V coil 390 ohm", xc, 60.96, unit=2)
    T = (xc, 50.8)
    s.w(coil.p("A1"), T, (xc + 7.62, 50.8))
    s.pwr(T, "V12RAW")
    fb = s.two(D, "D209", "flyback", (xc + 7.62, 64.77), "up")
    s.w((xc + 7.62, 50.8), fb.p("K"))
    lo = (xc, 68.58)
    s.w(coil.p("A2"), lo, q202.p("C"))
    s.w(fb.p("A"), (xc + 7.62, 68.58), lo)
    s.w(q202.p("E"), (xc, 86.36))
    s.pwr((xc, 86.36), "GND")
    r13 = s.two(R, "RX13", "?", (x0 - 7.62, 78.74), "left", pin="2", fields="above")
    s.w(r13.p("2"), q202.p("B"))
    s.w(r13.p("1"), (x0 - 17.78, 78.74))
    s.gl((x0 - 17.78, 78.74), "RY201_CMD", 180)
    s.text("MCU pin 49 (P72), not safety-gated", x0 - 36.0, 81.4, 1.0, italic=True)
    # ---- watchdog
    hdr(s, "HARDWARE WATCHDOG (IC503 74HC123, dual retriggerable one-shot)", 15.24, 134.62)
    for unit, X, Y, clr_q in ((1, 76.2, 172.72, None), (2, 76.2, 220.98, None)):
        u = s.place(HC123, "IC503", "74HC123", X, Y, unit=unit,
                    fields=dict(ref=(X, Y + 9.2, "top"), val=(X, Y + 11.0, "top")))
        n = str(unit)
        clr = u.p(f"~{{{n}CLR}}")
        s.w(clr, (clr[0] - 2.54, clr[1]))
        s.pwr((clr[0] - 2.54, clr[1]), "+5V")
        a, b = u.p(f"{n}A"), u.p(f"{n}B")
        if unit == 1:
            na = (a[0] - 7.62, a[1])
            rx20 = s.two(R, "RX20", "?", (na[0], na[1] - 2.54), "up", pin="2", fields="left",
                         note="ARM pull-up")
            s.w(a, na, (na[0] - 5.08, a[1]))
            s.w(na, rx20.p("2"))
            s.pwr(rx20.p("1"), "+5V")
            s.gl((na[0] - 5.08, a[1]), "ARM", 180)
            s.text("front panel (PC503) / MCU 14", na[0] - 38.0, a[1] - 3.4, 1.0, italic=True)
        else:
            s.w(a, (a[0] - 2.54, a[1]))
            s.pwr((a[0] - 2.54, a[1]), "GND", toward="left")
        s.w(b, (b[0] - 12.7, b[1]))
        s.gl((b[0] - 12.7, b[1]), "WDCLK", 180)
        s.text("MCU pin 52 pulses", b[0] - 33.0, b[1] + 2.6, 1.0, italic=True)
        qp, nq = u.p(f"{n}Q"), u.p(f"~{{{n}Q}}")
        s.nc(nq)
        s.w(qp, (qp[0] + 7.62, qp[1]))
        if unit == 1:
            s.lb((qp[0] + 7.62, qp[1]), "WD1")
            s.text("timer 1: needs MCU pulses AND front panel (ARM low)", qp[0] + 2.0, qp[1] - 4.0, 0.9, italic=True)
        else:
            s.gl((qp[0] + 7.62, qp[1]), "WD2", 0)
            s.text("read back on MCU pin 13", qp[0] + 7.62, qp[1] + 2.6, 1.0, italic=True)
        cx, rc = u.p(f"{n}Cx"), u.p(f"{n}Rx/Cx")
        yn = cx[1] - 5.08
        s.w(cx, (cx[0], yn), (cx[0] - 5.08, yn))
        s.pwr((cx[0] - 5.08, yn), "GND")
        if unit == 1:
            cap_ = s.two(CP, "C513", "22uF", (rc[0], yn), "left", fields="above")
            s.w(cap_.p("2"), (cx[0], yn))
            res = s.two(R, "R548", "unreadable", (rc[0], yn - 2.54), "up", pin="2")
        else:
            cap_ = s.two(C, "C514", "?", (rc[0] - 2.54, yn), "left", fields="above")
            s.w(cap_.p("2"), (cx[0], yn))
            s.w(rc, (rc[0], yn), cap_.p("1"))
            res = s.two(R, "RX18", "1M (105)", (rc[0], yn - 2.54), "up", pin="2")
        if unit == 1:
            s.w(rc, (rc[0], yn))
        s.w((rc[0], yn), res.p("2"))
        s.pwr(res.p("1"), "+5V")
    pu = s.place(HC123, "IC503", "74HC123", 132.08, 203.2, unit=3)
    s.pwr(pu.p("VCC"), "+5V")
    s.pwr(pu.p("GND"), "GND")
    # ---- IC700 latching comparators
    hdr(s, "LATCHING FAULT COMPARATORS (IC700 TLC277): the only source that can hold the permits high", 160.02, 134.62)
    ox, oy, oyB = 236.22, 172.72, 215.9
    for unit, Y, dout, dlat, perm, rpd, pin in ((1, oy, "D707", "D702", "PERMIT1", "R542", "11"),
                                                 (2, oyB, "D706", "D703", "PERMIT2", "R706", "12")):
        u = s.place(L["DUAL_OPAMP"], "IC700", "TLC277", ox, Y, unit=unit)
        O = (ox + 10.16, Y)
        s.w(u.p("1" if unit == 1 else "7"), O)
        do = s.two(D, dout, "", (ox + 12.7, Y), "right", fields="above", note="permit")
        s.w(O, do.p("A"))
        P1 = (ox + 25.4, Y)
        s.w(do.p("K"), P1, (ox + 30.48, Y))
        s.gl((ox + 30.48, Y), perm, 0)
        s.text(f"MCU pin {pin} (open-drain)", ox + 30.48, Y + 2.6, 1.0, italic=True)
        rp_ = s.two(R, rpd, "47k", (ox + 25.4, Y + 2.54), "down", note="pull-down")
        s.w(P1, rp_.p("1"))
        s.pwr(rp_.p("2"), "GND")
        Pn = u.p("3" if unit == 1 else "5")
        P = (ox - 10.16, Pn[1])
        Q = (ox - 10.16, Y + 7.62)
        dl = s.two(D, dlat, "", (ox - 3.81, Y + 7.62), "right", fields="below", note="latch")
        s.w(Pn, P, Q, dl.p("A"))
        s.w(dl.p("K"), (O[0], Y + 7.62), O)
        if unit == 1:
            r702 = s.two(R, "R702", "47k", (Q[0], Q[1] + 2.54), "down", note="approx")
            s.w(Q, r702.p("1"))
            M = (ox - 15.24, Y - 2.54)
            s.w(u.p("2"), M)
            r21 = s.two(R, "RX21", "39k", (M[0], M[1] - 2.54), "up", pin="2", fields="left")
            s.w(M, r21.p("2"))
            s.w(r21.p("1"), (M[0], M[1] - 12.7), (M[0] - 5.08, M[1] - 12.7))
            s.lb((M[0] - 5.08, M[1] - 12.7), "WD1", 180)
            r22 = s.two(R, "RX22", "150k", (M[0], M[1] + 2.54), "down", fields="left")
            s.w(M, r22.p("1"))
            s.pwr(r22.p("2"), "GND")
            s.text("threshold ~4 V while the watchdog runs", M[0] - 40.0, M[1] - 15.0, 0.9, italic=True)
            trunk_top = (ox - 25.4, r702.p("2")[1])
            s.w(r702.p("2"), trunk_top)
            brk = (ox - 25.4, Y + 25.4)
        else:
            r25 = s.two(R, "RX25", "39k", (Q[0], Q[1] + 2.54), "down")
            s.w(Q, r25.p("1"))
            s.pwr(r25.p("2"), "GND")
            K1 = (ox - 15.24, Pn[1])
            r26 = s.two(R, "RX26", "150k", (ox - 17.78, Pn[1]), "left", fields="below")
            s.w(P, K1, r26.p("1"))
            cx4 = s.two(C, "CX4", "?", (ox - 19.05, Y + 12.7), "left", fields="below")
            s.w(K1, (K1[0], Y + 12.7), cx4.p("1"))
            K2 = (ox - 27.94, Pn[1])
            s.w(r26.p("2"), K2, (ox - 30.48, Pn[1]))
            s.w(cx4.p("2"), (K2[0], Y + 12.7), K2)
            s.lb((ox - 30.48, Pn[1]), "JC3_SIG", 180)
            s.text("JC3 source\nnot traced", ox - 50.0, Pn[1] + 1.5, 0.9, italic=True)
            M = (ox - 10.16, Y - 2.54)
            r23 = s.two(R, "RX23", "~470k (approx)", (ox - 25.4, Y - 2.54), "right", fields="above")
            s.w(r23.p("2"), M, u.p("6"))
            cx3 = s.two(C, "CX3", "?", (M[0], M[1] - 2.54), "up")
            s.w(M, cx3.p("1"))
            s.w(cx3.p("2"), (M[0] + 7.62, cx3.p("2")[1]))
            s.pwr((M[0] + 7.62, cx3.p("2")[1]), "GND")
            s.w(brk, (brk[0], r23.p("1")[1]))
    s.w(trunk_top, brk)
    s.lb((trunk_top[0], trunk_top[1]), "NODE_N", 180)
    r708 = s.two(R, "R708", "1M", (brk[0] - 2.54, brk[1]), "left", fields="below")
    s.w(brk, r708.p("1"))
    d601 = s.two(D, "D601", "?", (r708.p("2")[0] - 2.54, brk[1]), "left", fields="above")
    s.w(r708.p("2"), d601.p("A"))
    kk = (d601.p("K")[0] - 2.54, brk[1])
    s.w(d601.p("K"), kk)
    r24 = s.two(R, "RX24", "1.2k", (kk[0], kk[1] + 2.54), "down", fields="left")
    s.w(kk, r24.p("1"))
    s.pwr(r24.p("2"), "GND")
    s.text("D601 anode: other source\nnot traced", ox - 44.0, brk[1] + 6.0, 0.9, italic=True)
    pu = s.place(L["DUAL_OPAMP"], "IC700", "TLC277", 289.56, 200.66, unit=3)
    s.pwr(pu.p("V+"), "+5V")
    s.pwr(pu.p("V-"), "GND")
    notes(s, """NOTES  (structure confirmed by continuity; MCU port types from the uPD78F0034 datasheet p.11;  ? = value not read)
- MCU pins 11-14 (P30-P33) are N-channel OPEN-DRAIN: they can only pull a line low, or read it.  PERMIT1/2 are pulled DOWN by R542/R706, so only IC700 (through D707/D706)
  can hold them high.  A dead or disconnected detector therefore removes the permit (fail-safe).  The MCU can veto (pull low) and read them.
- VGATE: the 3 x 47 kohm network (RX15, RX16, RX17) feeds Q205 from BOTH AND nodes, so the IGBT drivers are powered only while both mains relays are permitted.
- Watchdog: timer 1 time-out ~0.45 x R548 x 22 uF, timer 2 ~0.45 x 1 Mohm x C514.  Q_EMIT: D225/D226 raise the relay drivers' turn-on threshold; series/parallel not certain.
- IC700: D702/D703 feed each output back to its own + input (latch).  Half A's threshold comes from WD1, so the latch clears when the watchdog restarts.
  APPROXIMATE: the sensed signals (via D601/R708 and the JC3 path) were only partly traced.  Most likely role: heater current while the triac should be off (error 69).""",
          15.24, 240.0, 1.1)
    return s


# ================================================================== 6. analog sensing
def sheet_analog():
    s = new_sheet("Analog sensing (currents, trip, motor sensors)", "analog_sense.kicad_sch", 6, paper="A3")
    OA = L["DUAL_OPAMP"]
    hdr(s, "HEATER CURRENT AMPLIFIER (IC611 A, from T700)", 15.24, 27.94)
    ox, oy = 101.6, 66.04
    a = s.place(OA, "IC611", "TLC277", ox, oy, unit=1)
    YQ, YP = 63.5, 76.2
    s.gl((30.48, YQ), "CT_Q", 180)
    s.gl((30.48, YP), "CT_P", 180)
    s.text("T700 secondary", 15.24, 70.6, 1.0, italic=True)
    d700 = s.two(D, "D700", "clamp", (45.72, 72.39), "up", fields="left")
    d701 = s.two(D, "D701", "clamp", (55.88, 64.77), "down")
    r31 = s.two(R, "RX31", "300", (63.5, YQ), "right", fields="below")
    N = (78.74, YQ)
    s.w((30.48, YQ), (45.72, YQ), (55.88, YQ), r31.p("1"))
    s.w(r31.p("2"), N, a.p("2"))
    s.w(d700.p("K"), (45.72, YQ))
    s.w(d700.p("A"), (45.72, YP))
    s.w((55.88, YQ), d701.p("A"))
    s.w(d701.p("K"), (55.88, YP))
    s.w((30.48, YP), (45.72, YP), (55.88, YP), (88.9, YP), (88.9, a.p("3")[1]), a.p("3"))
    r32 = s.two(R, "RX32", "68k", (88.9, 53.34), "right", fields="above")
    cx5 = s.two(C, "CX5", "?", (90.17, 43.18), "right", fields="above")
    out = (114.3, oy)
    s.w(N, (78.74, 53.34), r32.p("1"))
    s.w((78.74, 53.34), (78.74, 43.18), cx5.p("1"))
    s.w(r32.p("2"), (114.3, 53.34), out)
    s.w(cx5.p("2"), (114.3, 43.18), (114.3, 53.34))
    s.w(a.p("1"), out, (119.38, oy))
    s.lb((119.38, oy), "IC611_OA")
    s.text("output A: destination not traced\n(probably IC700 via D601)", 119.38, oy + 2.4, 1.0, italic=True)
    pu = s.place(OA, "IC611", "TLC277", 160.02, 60.96, unit=3)
    r30 = s.two(R, "RX30", "~780 (in-circuit)", (160.02, pu.p("V+")[1] - 2.54), "up", pin="2", fields="left",
                note="feed not traced")
    s.w(pu.p("V+"), r30.p("2"))
    s.pwr(r30.p("1"), "VGATE")
    s.w(pu.p("V-"), (160.02, 68.58))
    s.pwr((160.02, 68.58), "VNEG", toward="down")
    s.text("runs from VNEG so the outputs\ncan swing below GND", 165.1, 72.0, 1.0, italic=True)
    # motor current
    hdr(s, "MOTOR CURRENT AMPLIFIER (IC611 B, from the shunts)", 15.24, 96.52)
    oy = 116.84
    b = s.place(OA, "IC611", "TLC277", ox, oy, unit=2)
    Lp = (66.04, oy)
    s.gl((30.48, oy), "LS_EMIT", 180)
    s.text("from R600 // R601", 15.24, oy + 2.6, 1.0, italic=True)
    r33 = s.two(R, "RX33", "22k", (73.66, b.p("6")[1]), "right", fields="above")
    r34 = s.two(R, "RX34", "180k (approx)", (73.66, b.p("5")[1]), "right", pin="2", fields="below")
    s.w((30.48, oy), Lp, (66.04, b.p("6")[1]), r33.p("1"))
    s.w(Lp, (66.04, b.p("5")[1]), r34.p("2"))
    s.w(r33.p("2"), b.p("6"))
    s.w(r34.p("1"), b.p("5"))
    r605 = s.two(R, "R605", "51k (5102)", (111.76, oy), "right")
    s.w(b.p("7"), r605.p("1"))
    nd = (124.46, oy)
    c612 = s.two(C, "C612", "?", (124.46, oy + 2.54), "down", fields="left")
    s.w(r605.p("2"), nd, (129.54, oy))
    s.w(nd, c612.p("1"))
    s.pwr(c612.p("2"), "GND")
    s.gl((129.54, oy), "IMOT", 0)
    s.text("MCU pin 29 (ANI4)", 129.54, oy + 2.6, 1.0, italic=True)
    s.text("gain network only partly traced; output B also feeds IC610 (path not traced)", 30.48, 130.0, 1.0,
           italic=True)
    # overcurrent comparator
    hdr(s, "OVERCURRENT COMPARATOR (IC610 LM393)", 15.24, 144.78)
    ca = s.place(OA, "IC610", "LM393", ox, 162.56, unit=1)
    cb = s.place(OA, "IC610", "LM393", ox, 185.42, unit=2)
    r35 = s.two(R, "RX35", "not fitted", (111.76, 185.42), "right", dnp=True, note="empty pads")
    tn = (119.38, 162.56)
    s.w(ca.p("1"), tn, (127.0, 162.56))
    s.w(cb.p("7"), r35.p("1"))
    s.w(r35.p("2"), (119.38, 185.42), tn)
    s.gl((127.0, 162.56), "TRIP", 0)
    s.text("to D512/D513 (motor stage) via JC11\nand MCU pin 45 via R535", 127.0, 165.2, 1.0, italic=True)
    s.text("inputs of both halves\nnot traced", 66.04, 170.0, 1.0, italic=True)
    pc = s.place(OA, "IC610", "LM393", 160.02, 185.42, unit=3)
    s.pwr(pc.p("V+"), "+5V")
    s.pwr(pc.p("V-"), "GND")
    # CN502
    hdr(s, "MOTOR SENSOR BOARD (CN502)", 200.66, 27.94)
    pins = []
    for i in range(1, 6):
        pins.append((str(i), str(i)))
        if i < 5:
            pins += [None, None]
    cn = box("CONN_5R", [], pins, width=5.08, ref="CN")
    cnp = s.place(cn, "CN502", "to sensor board in motor", 233.68, 76.2,
                  fields=dict(ref=(233.68, 59.0, "bottom"), val=(231.0, 94.5, "right top")))
    p1, p2, p3, p4, p5 = (cnp.p(str(i)) for i in range(1, 6))
    n1 = (p1[0] + 7.62, p1[1])
    r36 = s.two(R, "RX36", "~1k (975 in-circuit)", (n1[0] + 5.08, p1[1]), "right")
    s.w(p1, n1, r36.p("1"))
    s.w(r36.p("2"), (r36.p("2")[0] + 5.08, p1[1]))
    s.gl((r36.p("2")[0] + 5.08, p1[1]), "NTC_ADC", 0)
    s.text("MCU pin 31 (ANI2)", r36.p("2")[0] + 5.08, p1[1] + 2.6, 1.0, italic=True)
    xr = 215.9
    rth = s.two(L["NTC"], "RTH1", "10k NTC", (xr, p1[1] - 2.54), "down", offboard=True, fields="left")
    s.w(n1, (n1[0], p1[1] - 10.16), (xr, p1[1] - 10.16), rth.p("1"))
    s.pwr(rth.p("2"), "GND")
    s.frame(203.2, p1[1] - 6.35, 223.52, p1[1] + 12.7)
    s.text("in the motor\n(off-board)", 203.2, p1[1] + 14.0, 0.9, italic=True)
    for pp, ref, lbl, mcu in ((p2, "RX37", "POS_A", "44 (INTP1)"), (p3, "RX38", "POS_B", "43 (INTP0)")):
        rr = s.two(R, ref, "20k", (pp[0] + 12.7, pp[1]), "right")
        s.w(pp, rr.p("1"))
        s.w(rr.p("2"), (rr.p("2")[0] + 5.08, pp[1]))
        s.gl((rr.p("2")[0] + 5.08, pp[1]), lbl, 0)
        s.text(f"rotor position -> MCU pin {mcu}", rr.p("2")[0] + 5.08, pp[1] + 2.6, 1.0, italic=True)
    s.w(p4, (p4[0] + 7.62, p4[1]))
    s.lb((p4[0] + 7.62, p4[1]), "VSENS")
    s.text("sensor supply", p4[0] + 17.0, p4[1] - 0.6, 1.0, italic=True)
    s.w(p5, (p5[0] + 5.08, p5[1]))
    s.pwr((p5[0] + 5.08, p5[1]), "GND")
    # sensor supply regulator
    hdr(s, "SENSOR SUPPLY (zener follower)", 200.66, 124.46)
    q = s.place(NPN, "Q508", "BC846-type", 248.92, 152.4)
    e = q.p("E")
    s.w(e, (e[0], e[1] + 2.54), (e[0] + 5.08, e[1] + 2.54))
    s.lb((e[0] + 5.08, e[1] + 2.54), "VSENS")
    cnode = (q.p("C")[0], q.p("C")[1] - 5.08)
    s.w(q.p("C"), cnode)
    r512 = s.two(R, "R512", "?", (cnode[0], cnode[1] - 2.54), "up", pin="2", fields="left", note="source assumed")
    s.w(cnode, r512.p("2"))
    s.pwr(r512.p("1"), "V12RAW")
    c512 = s.two(CP, "C512", "?", (cnode[0] + 10.16, cnode[1] + 2.54), "down")
    s.w(cnode, (cnode[0] + 10.16, cnode[1]), c512.p("1"))
    s.pwr(c512.p("2"), "GND")
    bn = (q.p("B")[0] - 5.08, q.p("B")[1])
    zd = s.two(ZD, "ZD500", "zener (V not read)", (bn[0], bn[1] + 2.54), "down", pin="K", fields="left")
    s.w(q.p("B"), bn, zd.p("K"))
    s.pwr(zd.p("A"), "GND")
    s.text("Q508 base bias not traced", 223.52, 172.0, 1.0, italic=True)
    notes(s, """NOTES  (approximate where marked; ? = value not read)
- IC611 TLC277 is powered between pin 8 (~0.78 kohm in-circuit to VGATE; exact feed not traced) and the negative rail VNEG (pin 4, C230).
- Half A converts the T700 secondary current to a voltage (300 ohm in, 68 kohm // C feedback, D700/D701 clamp). Where CT_P is referenced and where output A goes were not traced.
- Half B amplifies the shunt voltage (LS_EMIT) for the MCU (pin 29).  IC610 output A is the hardware overcurrent trip; output B goes to unpopulated pads (second trip, not fitted).
- CN502: pin 1 motor NTC (~12.5 kohm at room temperature, i.e. a 10 kohm NTC); pins 2/3 rotor-position sensors; pin 4 sensor supply; pin 5 GND.""",
          15.24, 238.76, 1.1)
    return s


# ================================================================== 7. MCU & links
MCU_NAMES = {1: "P50/A8", 2: "P51/A9", 3: "P52/A10", 4: "P53/A11", 5: "P54/A12", 6: "P55/A13", 7: "P56/A14",
             8: "P57/A15", 9: "VSS0", 10: "VDD0", 11: "P30", 12: "P31", 13: "P32", 14: "P33", 15: "P34/SI31",
             16: "P35/SO31", 17: "P36/SCK31", 18: "P20/SI30", 19: "P21/SO30", 20: "P22/SCK30", 21: "P23/RxD0",
             22: "P24/TxD0", 23: "P25/ASCK0", 24: "VDD1", 25: "AVSS", 26: "P17/ANI7", 27: "P16/ANI6",
             28: "P15/ANI5", 29: "P14/ANI4", 30: "P13/ANI3", 31: "P12/ANI2", 32: "P11/ANI1", 33: "P10/ANI0",
             34: "AVREF", 35: "AVDD", 36: "~{RESET}", 37: "XT2", 38: "XT1", 39: "VPP", 40: "X2", 41: "X1",
             42: "VSS1", 43: "P00/INTP0", 44: "P01/INTP1", 45: "P02/INTP2", 46: "P03/INTP3", 47: "P70/TO0",
             48: "P71/TI01", 49: "P72/TO50", 50: "P73/TO51", 51: "P74/PCL", 52: "P75/BUZ", 53: "P64/~{RD}",
             54: "P65/~{WR}", 55: "P66/~{WAIT}", 56: "P67/ASTB"}
for _i in range(8):
    MCU_NAMES[57 + _i] = f"P4{_i}/AD{_i}"
MCU_SYM = box("UPD78F0034", [(str(i), MCU_NAMES[i]) for i in range(1, 33)],
              [(str(i), MCU_NAMES[i]) for i in range(33, 65)], ref="IC", width=30.48)
MCU_PINS = {  # pin: (net, role)
    1: ("P50_HIN1", "HIN1 -> IC501"), 2: ("LIN1", "LIN1 -> IC501"), 3: ("P52_HIN2", "HIN2 -> IC502"),
    4: ("P53_LIN2", "LIN2 -> IC502"), 5: ("P54_DRV505", "Q505 driver (inv.)"), 6: ("P55_DRV500", "Q500 driver (inv.)"),
    9: ("GND", ""), 10: ("+5V", ""), 11: ("PERMIT1", "permit 1 (open-drain)"), 12: ("PERMIT2", "permit 2 (open-drain)"),
    13: ("WD2", "watchdog 2 read-back"), 14: ("ARM", "watchdog arm / panel"), 16: ("GD_EN", "gate-drive enable"),
    18: ("PROG_SI", ""), 19: ("PROG_SO", ""), 20: ("PROG_SCK", ""), 21: ("RXD", "UART from panel"),
    22: ("TXD", "UART to panel"), 24: ("+5V", ""), 25: ("GND", ""), 29: ("IMOT", "motor current"),
    31: ("NTC_ADC", "motor NTC"), 33: ("AC_SENSE", "pre-charge sense"), 34: ("+5V", ""), 35: ("+5V", ""),
    36: ("RESET", ""), 38: ("+5V", ""), 39: ("VPP", ""), 42: ("GND", ""), 43: ("POS_B", "rotor position B"),
    44: ("POS_A", "rotor position A"), 45: ("P02_TRIP", "overcurrent interrupt"), 49: ("RY201_CMD", "RY201 bypass"),
    51: ("HEAT_CMD", "heater triac (PC700)"), 52: ("WDCLK", "watchdog pulses")}
LOCAL = {"PROG_SI", "PROG_SO", "PROG_SCK", "RESET", "VPP", "RXD", "TXD"}


def sheet_mcu():
    s = new_sheet("MCU, programming header & front-panel link", "mcu_links.kicad_sch", 7, paper="A3")
    hdr(s, "MICROCONTROLLER  NEC/Renesas uPD78F0034B (78K0, 64-pin QFP)", 15.24, 27.94)
    m = s.place(MCU_SYM, "IC1", "uPD78F0034B (GC 64-QFP)", 160.02, 88.9, note="board reference not read")
    for pin, (net, role) in MCU_PINS.items():
        pt = m.p(str(pin))
        left = pin <= 32
        end = (pt[0] - 5.08, pt[1]) if left else (pt[0] + 5.08, pt[1])
        s.w(pt, end)
        if net in ("GND", "+5V"):
            s.pwr(end, net, toward="left" if left else "right")
            continue
        ang = 180 if left else 0
        if net in LOCAL:
            if not left:
                end2 = (end[0] + 5.08, end[1])
                s.w(end, end2)
                end = end2
            s.lb(end, net, ang)
        else:
            s.gl(end, net, ang)
        if role:
            w = len(net) * 1.3 + 3.0
            tx = end[0] - w - 1.5 if left else end[0] + w + 1.5
            s.text(role, tx, pt[1], 0.9, italic=True, justify="right" if left else "left")
    s.text("untraced pins left open; crystal/resonator (X1/X2) and reset circuit not traced", 15.24, 32.0, 1.0,
           italic=True)
    # programming header
    hdr(s, "FLASH PROGRAMMING HEADER CN503", 271.78, 50.8)
    cpins = []
    for i in range(1, 9):
        cpins.append((str(i), str(i)))
        if i < 8:
            cpins.append(None)
    cn = box("CONN_8", cpins, [], width=5.08, ref="CN")
    c = s.place(cn, "CN503", "2x4 header, not fitted", 309.88, 80.01)
    for pin, net in ((1, "GND"), (2, "RESET"), (3, "PROG_SO"), (4, "+5V"), (5, "PROG_SI"), (6, "VPP"),
                     (7, "PROG_SCK")):
        pt = c.p(str(pin))
        end = (pt[0] - 5.08, pt[1])
        s.w(pt, end)
        if net in ("GND", "+5V"):
            s.pwr(end, net, toward="left")
        else:
            s.lb(end, net, 180)
    s.nc(c.p("8"))
    s.text("3-wire CSI30 flash mode;\nnot connected in the machine", 271.78, 110.0, 1.0, italic=True)
    # front panel link
    hdr(s, "FRONT-PANEL LINK (opto-isolated UART)", 15.24, 152.4)
    s.text("COLD (isolated) side", 30.48, 157.5, 1.1, bold=True)
    s.text("HOT side (GND = bus negative)", 121.92, 157.5, 1.1, bold=True)
    s.graphics.append(([(91.44, 154.94), (91.44, 226.06)], "dash", 0.3))
    pins = []
    for i in range(1, 6):
        pins.append((str(i), str(i)))
        if i < 5:
            pins += [None, None]
    cn300 = s.place(box("CONN_5R", [], pins, width=5.08, ref="CN"), "CN300", "to front panel (blue cable)",
                    25.4, 195.58)
    p1, p2, p3, p4, p5 = (cn300.p(str(i)) for i in range(1, 6))
    s.w(p1, (35.56, p1[1]))
    s.pwr((35.56, p1[1]), "GND_COLD")
    s.w(p3, (35.56, p3[1]))
    s.pwr((35.56, p3[1]), "VCOLD")
    s.text("1 GND_COLD  2 data from panel  3 VCOLD  4 data to panel  5 panel enable", 15.24, 230.0, 1.0, italic=True)
    r43 = s.two(R, "RX43", "470", (45.72, p2[1]), "right")
    s.w(p2, r43.p("1"))
    q = s.place(NPN, "Q506", "BC846 (1B)", 60.96, p2[1], note="approx")
    B = (55.88, p2[1])
    s.w(r43.p("2"), B)
    r44 = s.two(R, "RX44", "47k", (55.88, p2[1] + 2.54), "down", fields="left")
    s.w(B, r44.p("1"))
    s.pwr(r44.p("2"), "GND_COLD")
    s.w(q.p("E"), (63.5, q.p("E")[1] + 2.54))
    s.pwr((63.5, q.p("E")[1] + 2.54), "GND_COLD")
    COM = (78.74, 175.26)
    s.w(q.p("C"), (63.5, 175.26), COM)
    OPTO = box("OPTO", [("1", "A"), ("2", "K")], [("4", "C"), ("3", "E")], ref="PC")
    pc2 = s.place(OPTO, "PC502", "LTV-816 (panel -> MCU)", 91.44, 166.37)
    s.w(pc2.p("K"), (78.74, pc2.p("K")[1]), COM)
    r41 = s.two(R, "RX41", "1.5k", (78.74, 160.02), "left", pin="2", fields="above")
    s.w(pc2.p("A"), (81.28, pc2.p("A")[1]), (81.28, 160.02), r41.p("2"))
    s.w(r41.p("1"), (68.58, 160.02))
    s.pwr((68.58, 160.02), "VCOLD")
    rx = (106.68, pc2.p("C")[1])
    s.w(pc2.p("C"), rx, (111.76, rx[1]))
    s.lb((111.76, rx[1]), "RXD")
    s.text("MCU pin 21", 111.76, rx[1] + 2.4, 1.0, italic=True)
    r42 = s.two(R, "RX42", "?", (106.68, rx[1] - 2.54), "up", pin="2", fields="left", note="pull-up")
    s.w(rx, r42.p("2"))
    s.pwr(r42.p("1"), "+5V")
    s.w(pc2.p("E"), (101.6, pc2.p("E")[1]), (101.6, pc2.p("E")[1] + 2.54))
    s.pwr((101.6, pc2.p("E")[1] + 2.54), "GND")
    pc1 = s.place(OPTO, "PC501", "LTV-816 (MCU -> panel)", 91.44, 185.42, rot=180,
                  fields=dict(ref=(91.44, 179.6, "bottom"), val=(91.44, 191.2, "top")))
    s.w(pc1.p("E"), (78.74, pc1.p("E")[1]), COM)
    s.w(pc1.p("C"), (81.28, pc1.p("C")[1]), (81.28, p4[1]), p4)
    r40 = s.two(R, "RX40", "?", (101.6, pc1.p("A")[1]), "right", pin="2", fields="below")
    s.w(pc1.p("A"), r40.p("2"))
    s.w(r40.p("1"), (111.76, pc1.p("A")[1]))
    s.pwr((111.76, pc1.p("A")[1]), "+5V")
    tx = (104.14, pc1.p("K")[1])
    s.w(pc1.p("K"), tx, (104.14, 179.07), (114.3, 179.07))
    s.lb((114.3, 179.07), "TXD")
    s.text("MCU pin 22", 114.3, 181.5, 1.0, italic=True)
    pc3 = s.place(OPTO, "PC503", "LTV-816 (panel enable)", 91.44, 210.82, note="LED polarity assumed")
    s.w(p5, (76.2, p5[1]), (76.2, pc3.p("A")[1]), pc3.p("A"))
    s.w(pc3.p("K"), (78.74, pc3.p("K")[1]), (78.74, pc3.p("K")[1] + 3.81))
    s.pwr((78.74, pc3.p("K")[1] + 3.81), "GND_COLD")
    s.w(pc3.p("C"), (109.22, pc3.p("C")[1]))
    s.gl((109.22, pc3.p("C")[1]), "ARM", 0)
    s.text("watchdog arm (IC503 1A) and MCU pin 14", 109.22, pc3.p("C")[1] - 3.4, 1.0, italic=True)
    s.w(pc3.p("E"), (101.6, pc3.p("E")[1]), (101.6, pc3.p("E")[1] + 2.54))
    s.pwr((101.6, pc3.p("E")[1] + 2.54), "GND")
    notes(s, """NOTES
- MCU pin numbers per the datasheet QFP drawing (p.6), marking D78F0034BCC (archived datasheet in datasheets/archive/).
- UART0: PC502 carries panel -> MCU RxD0 (pin 21); PC501 carries MCU TxD0 (pin 22) -> panel.  PC503 (LED driven by the panel on pins 5/1) pulls ARM low = arms watchdog timer 1.
- APPROXIMATE on the cold side: Q506's exact role, LED polarities of PC501/PC503, resistor values RX40-RX42; R540 not drawn.
- Never connect a mains-earthed adapter to the hot side. To sniff the link, use the COLD side of CN300 only (see docs/15-future-work.md).""",
          150.0, 205.74, 1.1)
    return s


# ================================================================== 8. power supply
def sheet_psu():
    s = new_sheet("Low-voltage power supply (flyback)", "power_supply.kicad_sch", 8, paper="A3")
    hdr(s, "INPUT RECTIFIER & FILTER (fed before the relays)", 15.24, 27.94)
    YT, YM, YB = 50.8, 66.04, 81.28
    s.gl((20.32, YM), "L_F", 180)
    f101 = s.two(L["FUSE"], "F101", "T1AH 250V", (30.48, YM), "right")
    s.w((20.32, YM), f101.p("1"))
    l1, l2 = 60.96, 76.2
    d101 = s.two(D, "D101", "", (l1, YM - 3.81), "up", fields="left")
    d100 = s.two(D, "D100", "", (l1, YB - 3.81), "up", fields="left")
    d103 = s.two(D, "D103", "", (l2, YM - 3.81), "up")
    d102 = s.two(D, "D102", "", (l2, YB - 3.81), "up")
    s.w(f101.p("2"), (l1, YM))
    for d in (d101, d103):
        s.w(d.p("K"), (d.p("K")[0], YT))
    for d in (d101, d103):
        s.w((d.p("A")[0], YM), d.p("A"))
    for d in (d100, d102):
        s.w(d.p("K"), (d.p("K")[0], YM))
        s.w(d.p("A"), (d.p("A")[0], YB))
    z = s.two(L["VAR"], "Z101", "varistor (not fitted)", (64.77, YM), "right", dnp=True, fields="below")
    s.w((l1, YM), z.p("1"))
    s.w(z.p("2"), (l2, YM), (86.36, YM))
    s.gl((86.36, YM), "N_F", 0)
    lf = s.two(L["L"], "L101", "filter choke", (83.82, YT), "right")
    hv = (99.06, YT)
    s.w((l1, YT), (l2, YT), lf.p("1"))
    s.w(lf.p("2"), hv)
    c110 = s.two(CP, "C110", "22uF 400V", (hv[0], YM - 3.81), "down")
    s.w(hv, c110.p("1"))
    s.w(c110.p("2"), (hv[0], YB))
    s.w((l1, YB), (l2, YB), (88.9, YB), (hv[0], YB))
    s.pwr((88.9, YB), "HVDC_N")
    s.text("HVDC_N = primary ground (NOT the logic GND)", 40.64, 90.0, 1.0, italic=True)
    # flyback
    hdr(s, "FLYBACK CONVERTER", 116.84, 27.94)
    N3 = [None, None, None]
    tl = [("1", "PRI+")] + N3 + [("2", "PRI-")] + N3 * 2 + [None, ("3", "AUX+")] + N3 + [("4", "AUX-")]
    tr = [("5", "12V")] + N3 + [("6", "5V")] + N3 + [("7", "NEG")] + N3 + [("8", "HOT_COM")] + N3 + [None, ("9", "COLD")] \
        + N3 + [("10", "COLD_COM")]
    t100 = s.place(box("T100", tl, tr, ref="T", title="windings: functional"), "T100", "D1D8A flyback", 152.4,
                   92.71)
    pp, pm = t100.p("PRI+"), t100.p("PRI-")
    s.w(hv, (121.92, YT), (134.62, YT), (134.62, pp[1]), pp)
    zd = s.two(ZD, "ZD101", "clamp zener", (121.92, YT + 2.54), "down", fields="left")
    s.w((121.92, YT), zd.p("A"))
    DR = (129.54, pm[1] + 5.08)
    d104 = s.two(D, "D104", "clamp", (121.92, DR[1] - 2.54), "up", fields="left")
    s.w(zd.p("K"), d104.p("K"))
    s.w(pm, (129.54, pm[1]), DR)
    s.w(d104.p("A"), (121.92, DR[1]), DR)
    ic = s.place(box("MIP2E3D", [("D", "DRAIN")], [("S", "SOURCE"), ("V", "VDD"), ("F", "FB")], ref="IC",
                     title="pinout not traced"), "IC100", "Panasonic MIP2E3D", 147.32, 147.32)
    s.w(DR, (129.54, ic.p("DRAIN")[1]), ic.p("DRAIN"))
    src = ic.p("SOURCE")
    s.w(src, (src[0] + 5.08, src[1]))
    s.pwr((src[0] + 5.08, src[1]), "HVDC_N", toward="right")
    s.w(ic.p("VDD"), (src[0] + 5.08, ic.p("VDD")[1]))
    s.lb((src[0] + 5.08, ic.p("VDD")[1]), "IC100_VDD")
    ax, am = t100.p("AUX+"), t100.p("AUX-")
    dx5 = s.two(D, "DX5", "aux rectifier", (134.62, ax[1] + 2.54), "down", fields="left")
    s.w(ax, (134.62, ax[1]), dx5.p("A"))
    s.w(dx5.p("K"), (134.62, dx5.p("K")[1] + 2.54))
    s.lb((134.62, dx5.p("K")[1] + 2.54), "IC100_VDD", 180)
    s.w(am, (137.16, am[1]), (137.16, am[1] + 2.54))
    s.pwr((137.16, am[1] + 2.54), "HVDC_N")
    # feedback
    fbo = box("OPTO_FB", [("2", "K"), ("1", "A")], [("3", "E"), ("4", "C")], ref="PC")
    pc = s.place(fbo, "PC100", "feedback opto", 190.5, ic.p("FB")[1] + 1.27, rot=180,
                 fields=dict(ref=(190.5, ic.p("FB")[1] - 5.0, "bottom"), val=(190.5, ic.p("FB")[1] + 6.4, "top")))
    s.w(ic.p("FB"), pc.p("C"))
    pe = pc.p("E")
    s.w(pe, (pe[0] - 2.54, pe[1]), (pe[0] - 2.54, pe[1] + 2.54))
    s.pwr((pe[0] - 2.54, pe[1] + 2.54), "HVDC_N")
    pa, pk = pc.p("A"), pc.p("K")
    r50 = s.two(R, "RX50", "?", (pa[0] + 7.62, pa[1] - 2.54), "up", pin="2")
    s.w(pa, (pa[0] + 7.62, pa[1]), r50.p("2"))
    s.pwr(r50.p("1"), "+5V")
    tlb = box("TL431", [("R", "REF")], [], top=[("K", "K")], bottom=[("A", "A")], ref="IC")
    tlp = s.place(tlb, "IC200", "TL431", 220.98, pk[1] + 12.7, fields=dict(
        ref=(227.3, pk[1] + 11.6, "left bottom"), val=(227.3, pk[1] + 13.0, "left top")))
    s.w(pk, (220.98, pk[1]), tlp.p("K"))
    s.pwr(tlp.p("A"), "GND")
    rn = (tlp.p("REF")[0] - 5.08, tlp.p("REF")[1])
    s.w(tlp.p("REF"), rn)
    r52 = s.two(R, "RX52", "?", (rn[0], rn[1] + 2.54), "down", fields="left")
    s.w(rn, r52.p("1"))
    s.pwr(r52.p("2"), "GND")
    r51 = s.two(R, "RX51", "?", (rn[0] - 2.54, rn[1]), "left", pin="2", fields="above")
    s.w(rn, r51.p("2"))
    s.w(r51.p("1"), (r51.p("1")[0] - 2.54, rn[1]))
    s.pwr((r51.p("1")[0] - 2.54, rn[1]), "+5V")
    s.text("regulates the hot-side +5V", 196.0, pk[1] + 22.5, 1.0, italic=True)
    # secondary rails
    hdr(s, "SECONDARY RAILS", 175.26, 27.94)
    w12, w5, wn, hc, wc, cc = (t100.p(k) for k in ("12V", "5V", "NEG", "HOT_COM", "COLD", "COLD_COM"))
    x0 = w12[0]

    def rail(pin, dref, cref, cval, rail_name, cx, reverse=False, gnd="GND"):
        d = s.two(D, dref, "", (pin[0] + 12.7, pin[1]), "left", fields="above") if reverse else \
            s.two(D, dref, "", (pin[0] + 5.08, pin[1]), "right", fields="above")
        if reverse:
            s.w(pin, d.p("K"))
            s.w(d.p("A"), (cx, pin[1]))
        else:
            s.w(pin, d.p("A"))
            s.w(d.p("K"), (cx, pin[1]))
        node = (cx, pin[1])
        s.pwr(node, rail_name)
        if reverse:
            cp = s.two(CP, cref, cval, (cx, pin[1] + 2.54), "down", pin="2")
            s.w(node, cp.p("2"))
            s.pwr(cp.p("1"), gnd)
        else:
            cp = s.two(CP, cref, cval, (cx, pin[1] + 2.54), "down")
            s.w(node, cp.p("1"))
            s.pwr(cp.p("2"), gnd)
        return node

    rail(w12, "D201", "C200", "? (relays, VGATE)", "V12RAW", x0 + 60.96)
    rail(w5, "D220", "C220", "? (logic)", "+5V", x0 + 48.26)
    rail(wn, "D230", "C230", "? (IC611)", "VNEG", x0 + 35.56, reverse=True)
    s.w(hc, (hc[0] + 5.08, hc[1]))
    s.pwr((hc[0] + 5.08, hc[1]), "GND")
    s.text("GND = hot logic ground = motor bus negative", x0 + 10.0, hc[1] - 0.6, 0.9, italic=True)
    nc_ = rail(wc, "D214", "C210", "?", "VCOLD", x0 + 25.4, gnd="GND_COLD")
    r211 = s.two(R, "R211", "?", (nc_[0] + 12.7, nc_[1] + 2.54), "down")
    s.w(nc_, (nc_[0] + 12.7, nc_[1]), r211.p("1"))
    s.pwr(r211.p("2"), "GND_COLD")
    s.w(cc, (cc[0] + 5.08, cc[1]))
    s.pwr((cc[0] + 5.08, cc[1]), "GND_COLD")
    s.text("isolated front-panel supply (CN300)", nc_[0] + 12.0, nc_[1] - 0.6, 0.9, italic=True)
    notes(s, """NOTES  (structure confirmed; transformer pin-out and several values NOT traced; ? = value not read)
- Fed from mains BEFORE the relays (it must power the MCU before RY200/RY202 close). Exact tap (before/after L103) not confirmed; drawn after L103.
- F101 T1 A; Z101 varistor position empty on this board; IC100 Panasonic MIP2E3D (forum reports MIP2E1D on 230 V boards); T100 marked D1D8A.
- Feedback: PC100 + IC200 TL431 regulate the hot-side +5V.  Clamp ZD101/D104, the aux winding and the IC100 pin-out are drawn functionally (DX5 = aux rectifier).
- Hot-side outputs are referenced to GND (= motor bus negative = MCU ground).  The cold output (VCOLD / GND_COLD) is the only isolated rail.""",
          15.24, 238.76, 1.1)
    return s


SHEETS = {"mains": sheet_mains, "bus": sheet_bus, "motor": sheet_motor, "safety": sheet_safety,
          "analog": sheet_analog, "mcu": sheet_mcu, "psu": sheet_psu}


LEGEND = """KEY NETS
Power symbols (rails): GND = hot logic ground = motor bus negative (NOT neutral, NOT earth);
  +5V logic;  V12RAW relay coils / gate-drive source;  VGATE switched gate-drive supply;  VNEG negative rail (IC611);
  VBUS ~340 V DC (= heatsink);  HVDC / HVDC_N flyback primary;  VCOLD / GND_COLD isolated front-panel supply.
Global labels (signals between sheets):
  L_F / N_F ........ live / neutral after the EMI choke L103
  NODE_Y / NODE_X .. live after RY200 / neutral after RY202
  CT_P / CT_Q ...... T700 secondary (heater current)
  LS_EMIT .......... low-side IGBT emitters (top of the shunts)
  PERMIT1/2, WD2 ... relay permits (MCU 11/12), watchdog 2 (MCU 13)
  ARM / WDCLK ...... watchdog arm (panel + MCU 14) / pulses (MCU 52)
  TRIP ............. overcurrent trip (IC610 -> D512/D513, R535 -> MCU 45)
  other labels ..... MCU pin signals, named after the port or function"""
ROOT_NOTES = [("""THERMOMIX TM31-4C (120 V) POWER BOARD  NPVTM31LTA-3  -  REVERSE-ENGINEERED SCHEMATIC  rev 0.2 (2026-11)

HOW TO READ THIS PROJECT
- Each sheet is drawn as a real circuit: parts are wired together; supply rails use power symbols; only signals that leave a sheet use
  global labels (flag-shaped). A few busy nodes inside a sheet use local net labels (plain text on a wire); same name = same net.
- Relays are split into two units: contacts (A) where they switch power, coil (B) next to its driver on 'Safety logic'.
  The dual op-amps are split into halves A/B and a supply unit C; the watchdog 74HC123 into timers A/B and supply C.
- References are the board's silkscreen references.  RXn / CXn / DXn = part present on the board whose reference was not read.
- '?' = value not read.  'approx' / APPROXIMATE = inferred from photos or partial tracing, not confirmed by continuity.
- Everything except the CN300 'COLD' corner is at mains potential.  Off-board items (bowl heater, motor windings, motor NTC) are drawn
  in dashed frames and excluded from the BOM.
- The connections are identical to rev 0.1 (verified by comparing the exported netlists node by node).

ARCHITECTURE IN ONE PARAGRAPH
Mains -> EMI filter -> two relays (RY200 live, RY202 neutral) -> heater (through a triac and current transformer T700) and the motor DC bus
(a voltage doubler giving ~340 V DC, pre-charged through R115/R114 and then bypassed by RY201).  A 78K0 MCU on this board drives a 4-phase
switched-reluctance motor (6 IGBTs, shared high-side switches) and talks to the front panel over an opto-isolated UART (CN300).
Hardware safety: both mains relays and the IGBT gate-drive supply need (a) two open-drain MCU permits that only IC700's fault comparators can hold
high, (b) a running 74HC123 watchdog fed by MCU pulses, and (c) for RY202, the front panel's enable through PC503.  A comparator (IC610) cuts the
high-side IGBTs in hardware on motor overcurrent.

KNOWN FAILURES / NOTES FROM THIS BOARD
- No heat, no error: CR700 triac A1 leg fatigued and cracked at its C-bend (fixed 2026-10, BTA24-600BW, re-form the C-bend).  Remember the TM31 only
  heats while a TIME is set and the blade is turning.
- Shorted triac (230 V forum reports) -> continuous heating, error 69.   F100 open / R115 open -> no motor.""", 15.24, 96.52, 1.4),
              (LEGEND, 15.24, 200.0, 1.4)]


def write():
    os.makedirs(OUT, exist_ok=True)
    for name, fn in SHEETS.items():
        if ONLY and name not in ONLY:
            continue
        fn()
    total = 0
    for sh in sheets:
        sh.check()
        with open(os.path.join(OUT, sh.fname), "w", encoding="utf-8") as f:
            f.write(sh.emit())
        total += len({p.ref for p in sh.parts if not p.ref.startswith("#")})
    root_notes = ROOT_NOTES if "ROOT_NOTES" in globals() else []
    with open(os.path.join(OUT, f"{PROJ}.kicad_sch"), "w", encoding="utf-8") as f:
        f.write(root_sheet(PROJ, "TM31 power board - overview", root_uuid, sheets, root_notes))
    pro = '''{
  "board": {"design_settings": {}},
  "meta": {"filename": "%s.kicad_pro", "version": 1},
  "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
  "sheets": [%s],
  "text_variables": {}
}''' % (PROJ, ", ".join([f'["{root_uuid}", ""]'] + [f'["{sh.sheet_uuid}", "{sh.title}"]' for sh in sheets]))
    with open(os.path.join(OUT, f"{PROJ}.kicad_pro"), "w") as f:
        f.write(pro)
    print("written", len(sheets) + 1, "sheets;", total, "parts")


if __name__ == "__main__":
    write()
