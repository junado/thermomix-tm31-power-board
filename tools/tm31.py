import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kisch import Sheet, box, make_lib, root_sheet, U

OUT = sys.argv[1]
PROJ = "TM31_power_board"
L = make_lib()

# ---------------- box symbols
B = {}
B["CONN_1"] = box("CONN_1", [("1", "1")], [], width=5.08, ref="CN")
B["CONN_5"] = box("CONN_5", [(str(i), str(i)) for i in range(1, 6)], [], width=5.08, ref="CN")
B["CONN_6"] = box("CONN_6", [(str(i), str(i)) for i in range(1, 7)], [], width=5.08, ref="CN")
B["CONN_8"] = box("CONN_8", [(str(i), str(i)) for i in range(1, 9)], [], width=5.08, ref="CN")
B["RELAY_1A"] = box("RELAY_1A", [("A1", "COIL+"), ("A2", "COIL-")], [("11", "COM"), ("14", "NO")], ref="RY")
B["RELAY_1C"] = box("RELAY_1C", [("A1", "COIL+"), ("A2", "COIL-")],
                    [("11", "COM"), ("14", "NO"), ("12", "NC")], ref="RY")
B["CT"] = box("CT", [("1", "P1"), ("2", "P2")], [("3", "S1"), ("4", "S2")], ref="T", title="current transf.")
B["CHOKE"] = box("CHOKE", [("1", "L_IN"), ("3", "N_IN")], [("2", "L_OUT"), ("4", "N_OUT")], ref="L",
                 title="common-mode")
B["TRIAC"] = box("TRIAC", [("3", "G")], [("2", "A2"), ("1", "A1")], ref="CR")
B["OPTOTRIAC"] = box("OPTOTRIAC", [("1", "A"), ("2", "K")], [("6", "MT6"), ("4", "MT4")], ref="PC",
                     title="zero-cross")
B["OPTO"] = box("OPTO", [("1", "A"), ("2", "K")], [("4", "C"), ("3", "E")], ref="PC")
B["BRIDGE"] = box("BRIDGE", [("2", "AC1"), ("3", "AC2")], [("1", "+"), ("4", "-")], ref="DB")
B["IR2106"] = box("IR2106", [("1", "VCC"), ("2", "HIN"), ("3", "LIN"), ("4", "COM")],
                  [("8", "VB"), ("7", "HO"), ("6", "VS"), ("5", "LO")], ref="IC")
B["DUAL_OPAMP"] = box("DUAL_OPAMP", [("3", "+IN_A"), ("2", "-IN_A"), ("5", "+IN_B"), ("6", "-IN_B")],
                      [("1", "OUT_A"), ("7", "OUT_B"), ("8", "V+"), ("4", "V-")], ref="IC")
B["74HC123"] = box("74HC123",
                   [("1", "1A"), ("2", "1B"), ("3", "~{1CLR}"), ("15", "1Rx/Cx"), ("14", "1Cx"), None,
                    ("9", "2A"), ("10", "2B"), ("11", "~{2CLR}"), ("7", "2Rx/Cx"), ("6", "2Cx")],
                   [("13", "1Q"), ("4", "~{1Q}"), None, ("5", "2Q"), ("12", "~{2Q}"), None, None, None,
                    ("16", "VCC"), None, ("8", "GND")], ref="IC")
mcu_names = {1: "P50/A8", 2: "P51/A9", 3: "P52/A10", 4: "P53/A11", 5: "P54/A12", 6: "P55/A13", 7: "P56/A14",
             8: "P57/A15", 9: "VSS0", 10: "VDD0", 11: "P30", 12: "P31", 13: "P32", 14: "P33", 15: "P34/SI31",
             16: "P35/SO31", 17: "P36/SCK31", 18: "P20/SI30", 19: "P21/SO30", 20: "P22/SCK30", 21: "P23/RxD0",
             22: "P24/TxD0", 23: "P25/ASCK0", 24: "VDD1", 25: "AVSS", 26: "P17/ANI7", 27: "P16/ANI6",
             28: "P15/ANI5", 29: "P14/ANI4", 30: "P13/ANI3", 31: "P12/ANI2", 32: "P11/ANI1", 33: "P10/ANI0",
             34: "AVREF", 35: "AVDD", 36: "~{RESET}", 37: "XT2", 38: "XT1", 39: "VPP", 40: "X2", 41: "X1",
             42: "VSS1", 43: "P00/INTP0", 44: "P01/INTP1", 45: "P02/INTP2", 46: "P03/INTP3", 47: "P70/TO0",
             48: "P71/TI01", 49: "P72/TO50", 50: "P73/TO51", 51: "P74/PCL", 52: "P75/BUZ", 53: "P64/~{RD}",
             54: "P65/~{WR}", 55: "P66/~{WAIT}", 56: "P67/ASTB"}
for i in range(8):
    mcu_names[57 + i] = f"P4{i}/AD{i}"
B["UPD78F0034"] = box("UPD78F0034", [(str(i), mcu_names[i]) for i in range(1, 33)],
                      [(str(i), mcu_names[i]) for i in range(33, 65)], ref="IC", width=30.48)
B["MIP2E3D"] = box("MIP2E3D", [("D", "DRAIN")], [("S", "SOURCE"), ("V", "VDD"), ("F", "FB")], ref="IC",
                   title="pinout not traced")
B["TL431"] = box("TL431", [("R", "REF")], [("K", "K"), ("A", "A")], ref="IC")
B["T100"] = box("T100", [("1", "PRI+"), ("2", "PRI-"), None, ("3", "AUX+"), ("4", "AUX-")],
                [("5", "12V"), ("6", "5V"), ("7", "NEG"), ("8", "HOT_COM"), None, ("9", "COLD"),
                 ("10", "COLD_COM")], ref="T", title="windings: functional")

R, C, CP, D, ZD = L["R"], L["C"], L["CP"], L["D"], L["ZD"]
NPN, PNP, IGBT, FUSE, IND, VAR, HTR = L["NPN"], L["PNP"], L["IGBT"], L["FUSE"], L["L"], L["VAR"], L["HEATER"]

root_uuid = U()
sheets = []


def new_sheet(title, fname, page, paper="A3"):
    s = Sheet(PROJ, title, fname, page, paper=paper, root_uuid=root_uuid, sheet_uuid=U())
    sheets.append(s)
    return s


def notes(s, text, x=15.24, y=15.24):
    s.note(text, x, y, 1.27)
    n = text.count("\n") + 1
    s.y_start = round((y + n * 2.2 + 8) / 2.54) * 2.54


def r2(s, ref, val, a, b, sym=None, **kw):
    s.add(sym or R, ref, val, {"1": a, "2": b}, **kw)


def dio(s, ref, val, a, k, sym=None, **kw):
    s.add(sym or D, ref, val, {"A": a, "K": k}, **kw)


def cap(s, ref, val, a, b, **kw):
    s.add(C, ref, val, {"1": a, "2": b}, **kw)


def ecap(s, ref, val, pos, neg, **kw):
    s.add(CP, ref, val, {"1": pos, "2": neg}, **kw)


def bjt(s, ref, typ, val, b, c, e, **kw):
    s.add(NPN if typ == "NPN" else PNP, ref, val, {"B": b, "C": c, "E": e}, **kw)


# =============================================================== 2. mains & heater
s = new_sheet("Mains input & heater", "mains_heater.kicad_sch", 2)
notes(s, """MAINS INPUT AND HEATER  (confirmed by continuity unless marked)
- CN100 = BLACK tab (live), CN101 = WHITE tab (neutral). L103 common-mode choke. CX102 across the input, bleeders R103-R105 (values not read).
- RY200 switches live (L_F) to NODE_Y. RY202 switches neutral (N_F) to NODE_X through the three parallel jumpers JC12-JC14.
  Both relays can only close when the safety logic permits it (sheet 'Safety logic').
- Heater path: L_F - RY200 - NODE_Y - T700 heavy winding - CN703 - bowl heater - CN704 - triac A1..A2 - NODE_X - RY202 - N_F.  No fuse in the heater path on this board.
- CR700 must be an ISOLATED-TAB triac (BTA): it is riveted to a heatsink that sits at VBUS (~340 V DC). Original marking unreadable (date code 409);
  replaced with BTA24-600BW after the A1 leg cracked at its bend (2026-10). Re-create the C-bend strain relief on replacement legs.
- PC700 MOC3063 zero-cross opto-triac: LED fed from +5V via R713, cathode switched by MCU pin 51 (P74).  Gate drive: MT6 - R714 - R715 (2 x 180 ohm) - G.
- 120 V bowl: heater 12.8 ohm (~1.1 kW, ~9.4 A at 120 V), NTC ~130 kohm at room temp.  230 V bowls: heater ~53 ohm.  Never swap bowls between versions.
- CY103 / CY104 Y-capacitors are present; their far-end connections were not traced (not drawn).""")
s.group("Mains input & EMI filter")
s.add(B["CONN_1"], "CN100", "BLACK spade (live)", {"1": "LINE"})
s.add(B["CONN_1"], "CN101", "WHITE spade (neutral)", {"1": "NEUT"})
cap(s, "CX102", "X2 capacitor", "LINE", "NEUT")
r2(s, "R103", "bleeder (not read)", "LINE", "BLEED1")
r2(s, "R104", "bleeder (not read)", "BLEED1", "BLEED2")
r2(s, "R105", "bleeder (not read)", "BLEED2", "NEUT")
s.add(B["CHOKE"], "L103", "EMI choke", {"L_IN": "LINE", "L_OUT": "L_F", "N_IN": "NEUT", "N_OUT": "N_F"})
s.group("Mains relays (coils on 'Safety logic')")
s.add(B["RELAY_1A"], "RY200", "Schrack RTH34012WG 12VDC 16A",
      {"COIL+": "V12RAW", "COIL-": "RY200_LO", "COM": "L_F", "NO": "NODE_Y"}, note="live-side heater/motor relay")
s.add(B["RELAY_1A"], "RY202", "Schrack RTH34012WG 12VDC 16A",
      {"COIL+": "V12RAW", "COIL-": "RY202_LO", "COM": "N_F", "NO": "NODE_X"}, note="neutral-side relay, via JC12-14")
s.group("Heater circuit")
s.add(B["CT"], "T700", "HARTU 711078-51", {"P1": "NODE_Y", "P2": "HEAT_HI", "S1": "CT_Q", "S2": "CT_P"},
      note="secondary leaves via JD5/JD6; S1/S2 order assumed")
s.add(B["CONN_1"], "CN703", "heater spade", {"1": "HEAT_HI"})
s.add(B["CONN_1"], "CN704", "heater spade", {"1": "HEAT_LO"})
s.add(HTR, "HTR1", "bowl heater 12.8 ohm", {"1": "HEAT_HI", "2": "HEAT_LO"}, offboard=True,
      note="in the bowl (off-board)")
s.add(B["TRIAC"], "CR700", "BTA24-600BW (BTA only)", {"A2": "NODE_X", "A1": "HEAT_LO", "G": "TRIAC_G"},
      note="heatsink at VBUS - insulated tab mandatory")
s.group("Triac firing (MCU pin 51)")
r2(s, "R714", "180", "PC700_MT6", "TRIAC_R")
r2(s, "R715", "180", "TRIAC_R", "TRIAC_G")
s.add(B["OPTOTRIAC"], "PC700", "MOC3063", {"A": "PC700_A", "K": "HEAT_CMD", "MT6": "PC700_MT6", "MT4": "NODE_X"})
r2(s, "R713", "not read", "+5V", "PC700_A")

# =============================================================== 3. motor DC bus
s = new_sheet("Motor DC bus (doubler) & pre-charge", "motor_bus.kicad_sch", 3)
notes(s, """MOTOR DC BUS - VOLTAGE DOUBLER (120 V version of a 230 V design)
- Live after RY200 (NODE_Y) feeds the capacitor midpoint MID through F100 (T6.3 A).  F100 is the MOTOR fuse, not part of the heater path.
- Neutral after RY202 (NODE_X) reaches BOTH AC pins of DB100 (tied together) through the pre-charge resistors R115 + R114, later shorted by RY201.
- Result: VBUS = ~340 V DC (~170 V per capacitor) - the same bus as a 230 V board's bridge, so the motor stage is shared with the EU design.
- Power-up sequence (the 3 clicks): RY202 + RY200 close -> C108/C109 charge through R115 (6.8 ohm, built-in 139 C thermal fuse) + R114 (15 ohm 5 W)
  -> RY201 switches DB100's AC node straight to NODE_X.  At rest, RY201 NC routes that node to D107 -> R110/R111 -> MCU pin 33 (ANI0),
  so the MCU can verify pre-charge voltage before closing RY201.
- Diagnostics: F100 open or R115 open = motor dead, heater still works.
- !! VBUS is also the potential of the heatsink/shield (mounting eyelet next to CN704). Measure from GND (= VBUS-) only with a floating DMM, never a grounded scope.
- APPROXIMATE: pairing of balancing resistors R118-R121; the MID-side lead of CX101; Z100 (unmarked, probably a varistor) and R214 are not drawn.""")
s.group("Doubler & bus capacitors")
s.add(FUSE, "F100", "T6.3AH 250V", {"1": "NODE_Y", "2": "MID"}, note="motor fuse")
ecap(s, "C109", "680uF 200V", "VBUS", "MID")
ecap(s, "C108", "680uF 200V", "MID", "GND")
r2(s, "R118", "balancing (not read)", "VBUS", "BAL1")
r2(s, "R119", "balancing (not read)", "BAL1", "MID")
r2(s, "R120", "balancing (not read)", "MID", "BAL2")
r2(s, "R121", "balancing (not read)", "BAL2", "GND")
s.add(B["BRIDGE"], "DB100", "bridge rectifier (SIP)", {"AC1": "DB_AC", "AC2": "DB_AC", "+": "VBUS", "-": "GND"},
      note="both AC pins tied: doubler")
s.group("Pre-charge & bypass relay")
r2(s, "R115", "6.8 ohm 5W TF 139C", "NODE_X", "PRECH", note="cement R with thermal fuse")
r2(s, "R114", "15 ohm 5W", "PRECH", "DB_AC")
s.add(B["RELAY_1C"], "RY201", "Song Chuan 899-1C-F-C 12VDC",
      {"COIL+": "V12RAW", "COIL-": "RY201_LO", "COM": "DB_AC", "NO": "NODE_X", "NC": "AC_SENSE_RAW"},
      note="pre-charge bypass")
s.group("Bus input X-capacitor & bleeders")
cap(s, "CX101", "X2 capacitor", "MID", "PRECH", note="MID-side lead assumed")
r2(s, "R100", "680k", "MID", "BLD1")
r2(s, "R107", "680k", "BLD1", "BLD2")
r2(s, "R112", "680k", "BLD2", "PRECH")
s.group("Pre-charge sense -> MCU pin 33")
dio(s, "D107", "1N4007-type", "AC_SENSE_RAW", "D107_K")
r2(s, "R110", "not read", "D107_K", "SENSE_M")
r2(s, "R111", "not read", "SENSE_M", "AC_SENSE", note="via JD1 to MCU pin 33")
r2(s, "RX1", "~10k (9.87k in-circuit)", "AC_SENSE", "+5V", note="measured MCU33 to +5V")

# =============================================================== 4. motor stage
s = new_sheet("Motor power stage (4-phase SR)", "motor_stage.kicad_sch", 4, paper="A2")
notes(s, """MOTOR POWER STAGE - 4-PHASE SWITCHED-RELUCTANCE MOTOR, SHARED HIGH-SIDE SWITCHES
- Motor: 8 stator poles, 4 phases of 8.5 ohm.  CN501 phases: 1-3 and 1-5 share high side Q501;  2-4 and 2-6 share high side Q502.
- IGBTs Q500-Q505: G04N60 (Infineon SGP04N60-type, 600 V).  Low-side emitters (LS_EMIT) return to GND through R600 // R601 (0.27 ohm each) -> motor current sense.
- Freewheel diodes: D504/D505 from GND up to the shared ends (pins 1/2);  D500/D506/D508/D507 from pins 3/4/5/6 up to VBUS (all ~0.475 V in diode mode).
- IC501/IC502 IR2106S: HO -> Q501/Q502, LO -> Q503/Q504 through 470 ohm.  Their supply (pin 1) is VGATE, which exists only while the safety logic
  enables Q205/Q206 (sheet 'Safety logic') -> a firmware crash or a refused permit removes ALL gate drive.
- Q500/Q505 use discrete totem-pole drivers (Q512/Q513, Q510/Q514) fed from VGATE through ~33 ohm.  INVERTED: MCU pin high = IGBT off.
  Gate: turn-on through 470 ohm, fast turn-off through 47 ohm + diode, 10 kohm gate-emitter pull-down.  Base drive: 30 kohm // speed-up capacitor.
- Hardware overcurrent cutoff: comparator IC610 (sheet 'Analog sensing') pulls TRIP low -> D512/D513 force both HIN inputs low (high sides off
  without firmware) and interrupt the MCU on pin 45 (INTP2).
- MCU pins: 1 HIN1, 2 LIN1, 3 HIN2, 4 LIN2, 5 -> Q505 driver, 6 -> Q500 driver.
- APPROXIMATE: bootstrap diodes (D514/D517 drawn; D518/D519 also exist), HO gate resistors, Q503/Q504 gate pull-downs not traced;
  the ~33 ohm feed (RX11) may be two resistors; DX2 = turn-off diode of Q505 (reference not read).""")
s.group("Motor connector & windings")
s.add(B["CONN_6"], "CN501", "to stator windings", {str(i): f"MOT{i}" for i in range(1, 7)})
for ref, a, b in (("M1", "MOT1", "MOT3"), ("M2", "MOT1", "MOT5"), ("M3", "MOT2", "MOT4"), ("M4", "MOT2", "MOT6")):
    s.add(IND, ref, "motor phase 8.5 ohm", {"1": a, "2": b}, offboard=True, note="stator winding (off-board)")
for ref, g, c, e in (("Q501", "HO1", "VBUS", "MOT1"), ("Q502", "HO2", "VBUS", "MOT2"),
                     ("Q503", "G503", "MOT3", "LS_EMIT"), ("Q504", "G504", "MOT4", "LS_EMIT"),
                     ("Q500", "G500", "MOT5", "LS_EMIT"), ("Q505", "G505", "MOT6", "LS_EMIT")):
    s.group("IGBTs")
    s.add(IGBT, ref, "G04N60", {"G": g, "C": c, "E": e})
s.group("Freewheel diodes")
dio(s, "D504", "fast diode", "GND", "MOT1")
dio(s, "D505", "fast diode", "GND", "MOT2")
dio(s, "D500", "fast diode", "MOT3", "VBUS")
dio(s, "D506", "fast diode", "MOT4", "VBUS")
dio(s, "D508", "fast diode", "MOT5", "VBUS")
dio(s, "D507", "fast diode", "MOT6", "VBUS")
s.group("Current shunts")
r2(s, "R600", "0.27 ohm", "LS_EMIT", "GND", note="current shunt")
r2(s, "R601", "0.27 ohm", "LS_EMIT", "GND", note="current shunt")
s.group("IR2106 drivers (Q501-Q504)")
s.add(B["IR2106"], "IC501", "IR2106S", {"VCC": "VGATE", "HIN": "HIN1", "LIN": "LIN1", "COM": "GND",
                                         "VB": "VB1", "HO": "HO1", "VS": "MOT1", "LO": "LO1"})
s.add(B["IR2106"], "IC502", "IR2106S", {"VCC": "VGATE", "HIN": "HIN2", "LIN": "LIN2", "COM": "GND",
                                         "VB": "VB2", "HO": "HO2", "VS": "MOT2", "LO": "LO2"})
dio(s, "D514", "bootstrap (approx)", "VGATE", "VB1")
ecap(s, "C500", "bootstrap", "VB1", "MOT1")
dio(s, "D517", "bootstrap (approx)", "VGATE", "VB2")
ecap(s, "C506", "bootstrap", "VB2", "MOT2")
r2(s, "RX2", "470", "LO1", "G503")
r2(s, "RX3", "470", "LO2", "G504")
r2(s, "R510", "not read", "P50_HIN1", "HIN1")
r2(s, "R511", "not read", "P52_HIN2", "HIN2")
r2(s, "R572", "not read", "P53_LIN2", "LIN2")
s.group("Hardware overcurrent cutoff")
dio(s, "D512", "small signal", "HIN1", "TRIP")
dio(s, "D513", "small signal", "HIN2", "TRIP", note="TRIP also reached via JC11")
r2(s, "R535", "not read", "TRIP", "P02_TRIP", note="to MCU pin 45 INTP2")
s.group("Q500 driver (MCU pin 6, inverted)")
r2(s, "RX11", "~33", "VGATE", "VGATE_D", note="feed to discrete drivers")
# Q500 driver (MCU pin 6)
r2(s, "R562", "30k", "P55_DRV500", "Q507_B")
cap(s, "CX1", "speed-up", "P55_DRV500", "Q507_B")
bjt(s, "Q507", "NPN", "BC846-type", "Q507_B", "DRVB500", "GND")
r2(s, "RX4", "2.2k", "VGATE", "DRVB500", note="via JA7")
bjt(s, "Q512", "NPN", "BC846-type", "DRVB500", "VGATE_D", "DRV500")
bjt(s, "Q513", "PNP", "BC856-type", "DRVB500", "GND", "DRV500")
r2(s, "RX5", "470", "DRV500", "G500")
r2(s, "RX6", "47", "G500", "D511_A")
dio(s, "D511", "turn-off diode", "D511_A", "DRV500")
r2(s, "RX7", "10k", "G500", "LS_EMIT")
# Q505 driver (MCU pin 5)
s.group("Q505 driver (MCU pin 5, inverted)")
r2(s, "RX8", "~30k (not read)", "P54_DRV505", "Q511_B")
cap(s, "CX2", "speed-up", "P54_DRV505", "Q511_B")
bjt(s, "Q511", "NPN", "BC846-type", "Q511_B", "DRVB505", "GND")
r2(s, "RX9", "2.2k", "VGATE", "DRVB505", note="via JB5")
bjt(s, "Q510", "NPN", "BC846-type", "DRVB505", "VGATE_D", "DRV505")
bjt(s, "Q514", "PNP", "BC856-type", "DRVB505", "GND", "DRV505")
r2(s, "RX10", "470", "DRV505", "G505")
r2(s, "RX12", "47", "G505", "DX2_A")
dio(s, "DX2", "turn-off diode", "DX2_A", "DRV505")
r2(s, "R517", "~10k", "G505", "LS_EMIT")

# =============================================================== 5. safety logic
s = new_sheet("Safety logic (relay permits, watchdog, gate-drive enable)", "safety_logic.kicad_sch", 5, paper="A2")
notes(s, """SAFETY LOGIC  (structure confirmed by continuity; MCU port types from the uPD78F0034 datasheet p.11)
- MCU pins 11-14 (P30-P33) are N-channel OPEN-DRAIN: they can only pull a line low, or read it.
- PERMIT1 (MCU 11) / PERMIT2 (MCU 12) are pulled DOWN by 47 kohm (R542, R706).  Only IC700's outputs (through D707 / D706) can hold them high.
  The MCU can veto (pull low) and read them.  A dead or disconnected detector therefore removes the permit (fail-safe).
- RY202 driver Q200: diode-AND of WD1 (watchdog timer 1), WD2 (timer 2), PERMIT1, PERMIT2.   RY200 driver Q204: diode-AND of WD2, PERMIT1, PERMIT2.
  Both AND nodes are pulled up from V12RAW by 47 kohm.  Q200/Q204 emitters return to GND through D225/D226 (raises the turn-on threshold).
- RY201 (pre-charge bypass) is driven directly by MCU pin 49 (P72) through Q202 - not safety-critical.
- Gate-driver supply VGATE: Q205 (NPN) + Q206 (PNP) high-side switch from V12RAW.  Q205's base is fed through a 3 x 47 kohm network from BOTH AND nodes,
  so the IGBT drivers are powered only while both mains relays are permitted.  MCU pin 16 (P35) sits directly on Q205's base (read-back / veto).
- IC503 74HC(T)123 dual retriggerable one-shot = hardware watchdog.  MCU pin 52 (P75/BUZ) pulses both B inputs.  Timer 1's arm input 1A (ARM) is pulled low
  by the front panel through PC503 and is also on MCU pin 14 (open-drain).  Timer 2's output WD2 is read back on MCU pin 13 (open-drain).
- IC700 TLC277 = two LATCHING fault comparators (D702/D703 feed each output back to its own + input).  Half A's threshold comes from WD1 through a
  39k/150k divider, so the latch clears when the watchdog restarts.  The sensed signals (via D601 / R708, and the JC3 path) were only partly traced -> APPROXIMATE.
  Most likely role: detect heater current when the triac should be off (shorted triac -> error 69).
- Values not read: R548 (timer 1, time-out ~0.45 x R548 x 22 uF), C514 (timer 2, ~0.45 x 1 M x C514), ARM pull-up (RX20, near R546/R547).""")
s.group("Relay coil drivers")
dio(s, "D223", "flyback", "RY202_LO", "V12RAW")
dio(s, "D224", "flyback", "RY200_LO", "V12RAW")
dio(s, "D209", "flyback", "RY201_LO", "V12RAW")
bjt(s, "Q200", "NPN", "BC846-type", "AND1", "RY202_LO", "Q_EMIT", note="drives RY202")
bjt(s, "Q204", "NPN", "BC846-type", "AND2", "RY200_LO", "Q_EMIT", note="drives RY200")
dio(s, "D225", "small signal", "Q_EMIT", "GND", note="via JA9")
dio(s, "D226", "small signal", "Q_EMIT", "GND", note="via JA4; series/parallel not certain")
r2(s, "RX13", "base R (not read)", "RY201_CMD", "Q202_B")
bjt(s, "Q202", "NPN", "BC846-type", "Q202_B", "RY201_LO", "GND", note="drives RY201 (MCU 49)")
s.group("Relay AND gates & permits")
r2(s, "R206", "47k", "V12RAW", "AND1")
r2(s, "RX14", "47k", "V12RAW", "AND2")
dio(s, "D213", "AND input", "AND1", "WD1")
dio(s, "D212", "AND input", "AND1", "WD2")
dio(s, "D222", "AND input", "AND1", "PERMIT1")
dio(s, "D210", "AND input", "AND1", "PERMIT2")
dio(s, "D215", "AND input", "AND2", "WD2")
dio(s, "D221", "AND input", "AND2", "PERMIT1")
dio(s, "DX3", "AND input (unnumbered)", "AND2", "PERMIT2")
r2(s, "R542", "47k", "PERMIT1", "GND", note="pull-down")
r2(s, "R706", "47k", "PERMIT2", "GND", note="pull-down")
s.group("Gate-driver supply enable (VGATE)")
r2(s, "RX15", "47k", "AND1", "EN_M")
r2(s, "RX16", "47k", "AND2", "EN_M")
r2(s, "RX17", "47k", "EN_M", "GD_EN")
bjt(s, "Q205", "NPN", "BC846-type", "GD_EN", "Q205_C", "GND", note="base also on MCU 16")
r2(s, "R213", "6.2k", "Q205_C", "Q206_B")
r2(s, "R212", "470", "V12RAW", "Q206_B")
bjt(s, "Q206", "PNP", "BC856-type", "Q206_B", "VGATE", "V12RAW", note="VGATE via JA2 to IR2106 pin 1")
s.group("Hardware watchdog")
s.add(B["74HC123"], "IC503", "74HC123 / 74HCT123",
      {"1A": "ARM", "1B": "WDCLK", "~{1CLR}": "+5V", "1Rx/Cx": "RC1", "1Cx": "GND", "2A": "GND", "2B": "WDCLK",
       "~{2CLR}": "+5V", "2Rx/Cx": "RC2", "2Cx": "GND", "1Q": "WD1", "~{1Q}": "NC", "2Q": "WD2", "~{2Q}": "NC",
       "VCC": "+5V", "GND": "GND"}, note="hardware watchdog; 1Q via JC7")
r2(s, "R548", "not readable", "+5V", "RC1")
ecap(s, "C513", "22uF", "RC1", "GND")
r2(s, "RX18", "1M (105)", "+5V", "RC2")
cap(s, "C514", "value unknown", "RC2", "GND")
r2(s, "RX20", "pull-up (not read)", "+5V", "ARM", note="near R546/R547")
s.group("Latching fault comparators")
s.add(B["DUAL_OPAMP"], "IC700", "TLC277",
      {"+IN_A": "IC700_INA_P", "-IN_A": "IC700_INA_N", "OUT_A": "IC700_OA", "+IN_B": "IC700_INB_P",
       "-IN_B": "IC700_INB_N", "OUT_B": "IC700_OB", "V+": "+5V", "V-": "GND"}, note="latching fault comparators")
dio(s, "D707", "permit A", "IC700_OA", "PERMIT1")
dio(s, "D706", "permit B", "IC700_OB", "PERMIT2")
dio(s, "D702", "latch A", "IC700_INA_P", "IC700_OA")
dio(s, "D703", "latch B", "IC700_INB_P", "IC700_OB")
r2(s, "RX21", "39k", "WD1", "IC700_INA_N")
r2(s, "RX22", "150k", "IC700_INA_N", "GND")
r2(s, "R702", "47k", "IC700_INA_P", "NODE_N", note="approx")
r2(s, "RX23", "~470k", "NODE_N", "IC700_INB_N", note="approx")
cap(s, "CX3", "not read", "IC700_INB_N", "GND")
r2(s, "R708", "1M", "NODE_N", "D601_A", note="approx")
dio(s, "D601", "not read", "D601_A", "D601_K", note="anode source not traced")
r2(s, "RX24", "1.2k", "D601_K", "GND")
r2(s, "RX25", "39k", "IC700_INB_P", "GND")
r2(s, "RX26", "150k", "IC700_INB_P", "JC3_SIG", note="JC3 source not traced")
cap(s, "CX4", "not read", "IC700_INB_P", "JC3_SIG")

# =============================================================== 6. analog sensing
s = new_sheet("Analog sensing (currents, trip, motor sensors)", "analog_sense.kicad_sch", 6)
notes(s, """ANALOG SENSING  (approximate where marked)
- IC611 TLC277 is powered between IC611_VP (pin 8, ~0.78 kohm in-circuit to VGATE; exact feed not traced) and the NEGATIVE rail VNEG (pin 4, C230),
  so its outputs can swing below GND.
- Half A: current-to-voltage converter for the heater current transformer T700.  CT current enters the - input through 300 ohm; 68 kohm // C feedback;
  D700/D701 back-to-back clamp across the CT.  Where CT_P is referenced and where output A goes were NOT traced (probably to IC700 via D601).
- Half B: motor current from the shunts (LS_EMIT) via 22 kohm; output -> R605 51 kohm + C612 -> MCU pin 29 (ANI4).
  Gain network only partly traced (180 kohm + 22 kohm path between pins 5 and 6) -> APPROXIMATE.  Output also feeds IC610 (path not traced).
- IC610 LM393: output A -> JC11 -> TRIP (hardware overcurrent cutoff, see motor stage).  Output B goes to an unpopulated position (second trip, not fitted).
  Comparator inputs not traced.
- CN502 (sensor board inside the motor): pin 1 motor NTC (~12.5 kohm at room temperature, i.e. a 10 kohm NTC) -> ~1 kohm -> MCU 31 (ANI2);
  pins 2/3 rotor-position sensors -> 20 kohm -> MCU 44/43 (INTP1/INTP0); pin 4 sensor supply from Q508 + ZD500 zener follower; pin 5 GND.
  Q508's base bias resistor and the supply feeding R512 were not traced (V12RAW assumed).""")
s.group("Heater current amplifier (IC611 A)")
s.add(B["DUAL_OPAMP"], "IC611", "TLC277",
      {"+IN_A": "CT_P", "-IN_A": "IC611_INA_N", "OUT_A": "IC611_OA", "+IN_B": "IC611_INB_P", "-IN_B": "IC611_INB_N",
       "OUT_B": "IC611_OB", "V+": "IC611_VP", "V-": "VNEG"}, note="A: heater CT,  B: motor current")
r2(s, "RX30", "~780 (in-circuit)", "VGATE", "IC611_VP", note="feed not traced")
dio(s, "D700", "clamp", "CT_P", "CT_Q")
dio(s, "D701", "clamp", "CT_Q", "CT_P")
r2(s, "RX31", "300 (3000)", "CT_Q", "IC611_INA_N")
r2(s, "RX32", "68k (6802)", "IC611_INA_N", "IC611_OA")
cap(s, "CX5", "not read", "IC611_INA_N", "IC611_OA")
s.group("Motor current amplifier (IC611 B)")
r2(s, "RX33", "22k", "LS_EMIT", "IC611_INB_N")
r2(s, "RX34", "180k (1803)", "IC611_INB_P", "LS_EMIT", note="approx")
r2(s, "R605", "51k (5102)", "IC611_OB", "IMOT")
cap(s, "C612", "not read", "IMOT", "GND", note="to MCU pin 29")
s.group("Overcurrent comparator")
s.add(B["DUAL_OPAMP"], "IC610", "LM393",
      {"+IN_A": "IC610_INA_P", "-IN_A": "IC610_INA_N", "OUT_A": "TRIP", "+IN_B": "IC610_INB_P",
       "-IN_B": "IC610_INB_N", "OUT_B": "IC610_OB", "V+": "+5V", "V-": "GND"}, note="inputs not traced")
r2(s, "RX35", "not fitted", "IC610_OB", "TRIP", dnp=True, note="empty pads")
s.group("Motor sensor board (CN502)")
s.add(B["CONN_5"], "CN502", "motor sensor board",
      {"1": "MOT_NTC", "2": "POS_A_RAW", "3": "POS_B_RAW", "4": "VSENS", "5": "GND"})
r2(s, "RTH1", "10k NTC in motor", "MOT_NTC", "GND", offboard=True, note="off-board")
r2(s, "RX36", "~1k (975 in-circuit)", "MOT_NTC", "NTC_ADC", note="to MCU pin 31")
r2(s, "RX37", "20k", "POS_A_RAW", "POS_A", note="to MCU pin 44")
r2(s, "RX38", "20k", "POS_B_RAW", "POS_B", note="to MCU pin 43")
s.group("Sensor supply regulator")
bjt(s, "Q508", "NPN", "BC846-type", "Q508_B", "Q508_C", "VSENS", note="zener-follower regulator")
dio(s, "ZD500", "zener (V not read)", "GND", "Q508_B", sym=ZD)
r2(s, "R512", "not read", "V12RAW", "Q508_C", note="source assumed")
ecap(s, "C512", "filter", "Q508_C", "GND")

# =============================================================== 7. MCU & links
s = new_sheet("MCU, programming header & front-panel link", "mcu_links.kicad_sch", 7, paper="A2")
notes(s, """MCU AND LINKS
- MCU: NEC/Renesas uPD78F0034B (78K0, 32 KB flash, 64-pin QFP, marking read as D78F0034BCC).  Pin numbers per the datasheet's QFP drawing (p.6).
- Untraced MCU pins are deliberately left unconnected (ERC will list them).  Crystal/resonator on X1/X2 and the reset circuit were not traced.
- CN503 = factory flash-programming header (3-wire CSI30 mode): 1 GND, 2 RESET, 3 SO30, 4 +5V, 5 SI30, 6 VPP, 7 SCK30, 8 n.c.  Not connected in the machine.
- CN300 = front control panel (blue cable), on the COLD (isolated) side: 1 GND_COLD, 2 data from panel, 3 VCOLD supply, 4 data to panel, 5 panel enable.
- UART0: PC502 carries panel -> MCU RxD0 (pin 21); PC501 carries MCU TxD0 (pin 22) -> panel.
  PC503 (LED driven directly by the panel on pins 5/1) pulls ARM low = arms watchdog timer 1 (sheet 'Safety logic'); also read on MCU pin 14.
- APPROXIMATE on the cold side: Q506's exact role, LED polarities of PC501/PC503, pull-up/LED resistor values (RX40-RX42); R540 not drawn.
- Pin roles: 1-4 HIN1/LIN1/HIN2/LIN2 | 5-6 Q505/Q500 drivers (inverted) | 11/12 PERMIT1/2 | 13 WD2 read-back | 14 ARM | 16 gate-drive enable |
  29 motor current | 31 motor NTC | 33 pre-charge/mains sense | 43/44 rotor position | 45 overcurrent trip | 49 RY201 | 51 heater triac | 52 watchdog pulses.""")
mcu = {"1": "P50_HIN1", "2": "LIN1", "3": "P52_HIN2", "4": "P53_LIN2", "5": "P54_DRV505", "6": "P55_DRV500",
       "9": "GND", "10": "+5V", "11": "PERMIT1", "12": "PERMIT2", "13": "WD2", "14": "ARM", "16": "GD_EN",
       "18": "PROG_SI", "19": "PROG_SO", "20": "PROG_SCK", "21": "RXD", "22": "TXD", "24": "+5V", "25": "GND",
       "29": "IMOT", "31": "NTC_ADC", "33": "AC_SENSE", "34": "+5V", "35": "+5V", "36": "RESET", "38": "+5V",
       "39": "VPP", "42": "GND", "43": "POS_B", "44": "POS_A", "45": "P02_TRIP", "49": "RY201_CMD",
       "51": "HEAT_CMD", "52": "WDCLK"}
s.group("MCU")
s.add(B["UPD78F0034"], "IC1", "uPD78F0034B (GC 64-QFP)", mcu, note="board reference not read")
s.group("Flash programming header")
s.add(B["CONN_8"], "CN503", "programming header 2x4",
      {"1": "GND", "2": "RESET", "3": "PROG_SO", "4": "+5V", "5": "PROG_SI", "6": "VPP", "7": "PROG_SCK", "8": "NC"},
      note="not fitted in machine")
s.group("Front-panel link (CN300 side is COLD)")
s.add(B["CONN_5"], "CN300", "to front panel (blue)",
      {"1": "GND_COLD", "2": "LINK_IN", "3": "VCOLD", "4": "LINK_OUT", "5": "PANEL_EN"}, note="COLD side")
s.add(B["OPTO"], "PC501", "LTV-816 (MCU -> panel)", {"A": "PC501_A", "K": "TXD", "C": "LINK_OUT", "E": "COM_NODE"})
r2(s, "RX40", "not read", "+5V", "PC501_A")
s.add(B["OPTO"], "PC502", "LTV-816 (panel -> MCU)", {"A": "PC502_A", "K": "COM_NODE", "C": "RXD", "E": "GND"})
r2(s, "RX41", "1.5k", "VCOLD", "PC502_A")
r2(s, "RX42", "pull-up (not read)", "+5V", "RXD")
s.add(B["OPTO"], "PC503", "LTV-816 (panel enable)", {"A": "PANEL_EN", "K": "GND_COLD", "C": "ARM", "E": "GND"},
      note="LED polarity assumed")
bjt(s, "Q506", "NPN", "BC846 (1B)", "Q506_B", "COM_NODE", "GND_COLD", note="cold side, approx")
r2(s, "RX43", "470", "LINK_IN", "Q506_B")
r2(s, "RX44", "47k", "Q506_B", "GND_COLD")

# =============================================================== 8. power supply
s = new_sheet("Low-voltage power supply (flyback)", "power_supply.kicad_sch", 8)
notes(s, """LOW-VOLTAGE SUPPLY - FUNCTIONAL DIAGRAM  (structure confirmed; transformer pin-out and several values NOT traced)
- Fed from mains BEFORE the relays (it must power the MCU before RY200/RY202 close).  Exact tap (before/after L103) not confirmed; drawn after L103.
- F101 T1 A, Z101 varistor position empty on this board, bridge D100-D103, L101 + C110 (22 uF 400 V) filter, IC100 Panasonic MIP2E3D
  (forum reports MIP2E1D on 230 V boards), transformer T100 (D1D8A).  Feedback: PC100 + IC200 TL431 regulate the hot-side +5V.
- Hot-side outputs, referenced to GND (= motor bus negative = MCU ground):  V12RAW (D201/C200) for relays and gate drive,
  +5V (D220/C220) logic,  VNEG (D230/C230, C230 + on GND) for IC611.
- Cold (isolated) output: VCOLD (D214/C210, R211 across C210) with GND_COLD, to the front panel through CN300.
- Clamp ZD101/D104, the aux winding and the IC100 pin-out are drawn functionally (DX5 = aux rectifier, reference not read).""")
s.group("Input rectifier & filter")
s.add(FUSE, "F101", "T1AH 250V", {"1": "L_F", "2": "F101_OUT"})
s.add(VAR, "Z101", "varistor (not fitted)", {"1": "F101_OUT", "2": "N_F"}, dnp=True)
dio(s, "D100", "bridge", "HVDC_N", "F101_OUT")
dio(s, "D101", "bridge", "F101_OUT", "HV_RAW")
dio(s, "D102", "bridge", "HVDC_N", "N_F")
dio(s, "D103", "bridge", "N_F", "HV_RAW")
s.add(IND, "L101", "filter choke", {"1": "HV_RAW", "2": "HVDC"})
ecap(s, "C110", "22uF 400V", "HVDC", "HVDC_N")
s.group("Flyback converter")
s.add(B["T100"], "T100", "D1D8A flyback",
      {"PRI+": "HVDC", "PRI-": "DRAIN", "AUX+": "AUX", "AUX-": "HVDC_N", "12V": "W12", "5V": "W5", "NEG": "WNEG",
       "HOT_COM": "GND", "COLD": "WCOLD", "COLD_COM": "GND_COLD"})
s.add(B["MIP2E3D"], "IC100", "Panasonic MIP2E3D", {"DRAIN": "DRAIN", "SOURCE": "HVDC_N", "VDD": "IC100_VDD",
                                                   "FB": "IC100_FB"})
dio(s, "D104", "clamp", "DRAIN", "CLAMP")
dio(s, "ZD101", "clamp zener", "HVDC", "CLAMP", sym=ZD)
dio(s, "DX5", "aux rectifier", "AUX", "IC100_VDD")
s.group("Feedback")
s.add(B["OPTO"], "PC100", "feedback opto", {"A": "PC100_A", "K": "PC100_K", "C": "IC100_FB", "E": "HVDC_N"})
r2(s, "RX50", "not read", "+5V", "PC100_A")
s.add(B["TL431"], "IC200", "TL431", {"K": "PC100_K", "A": "GND", "REF": "TL_REF"})
r2(s, "RX51", "not read", "+5V", "TL_REF")
r2(s, "RX52", "not read", "TL_REF", "GND")
s.group("Hot-side rails")
dio(s, "D201", "rectifier", "W12", "V12RAW")
ecap(s, "C200", "not read", "V12RAW", "GND", note="relay / gate-drive source")
dio(s, "D220", "rectifier", "W5", "+5V")
ecap(s, "C220", "not read", "+5V", "GND", note="+5V logic")
dio(s, "D230", "rectifier", "VNEG", "WNEG")
ecap(s, "C230", "not read", "GND", "VNEG", note="negative rail")
s.group("Cold-side rail (front panel)")
dio(s, "D214", "rectifier", "WCOLD", "VCOLD")
ecap(s, "C210", "not read", "VCOLD", "GND_COLD", note="cold side")
r2(s, "R211", "not read", "VCOLD", "GND_COLD")

# =============================================================== write
os.makedirs(OUT, exist_ok=True)
for sh in sheets:
    sh.place_all()
    with open(os.path.join(OUT, sh.fname), "w", encoding="utf-8") as f:
        f.write(sh.emit())

legend = """KEY NETS (global labels)
LINE / NEUT ........ mains at CN100 / CN101 (before L103)
L_F / N_F .......... live / neutral after the EMI choke L103
NODE_Y ............. live after RY200 (feeds heater via T700, and motor bus via F100)
NODE_X ............. neutral after RY202 (triac A2, opto-triac, pre-charge, RY201 NO)
HEAT_HI / HEAT_LO .. bowl heater ends (CN703 / CN704)
MID / VBUS / GND ... doubler midpoint / motor bus + (~340 V, = heatsink) / bus - (= MCU ground)
DB_AC .............. both AC pins of DB100;  PRECH = between R115 and R114
LS_EMIT ............ low-side IGBT emitters, top of the R600//R601 shunt
MOT1..MOT6 ......... CN501 motor pins (1-3, 1-5, 2-4, 2-6 = the 4 phases)
V12RAW ............. raw ~12-15 V (relay coils, VGATE source);  VGATE = switched gate-drive supply
+5V / VNEG ......... logic supply / negative rail for IC611
VCOLD / GND_COLD ... isolated front-panel supply (CN300)
AND1 / AND2 ........ diode-AND nodes driving RY202 / RY200
PERMIT1 / PERMIT2 .. MCU 11 / 12 (open-drain), held high only by IC700
WD1 / WD2 .......... watchdog timer 1 / timer 2 outputs (IC503 pins 13 / 5)
ARM / WDCLK ........ watchdog arm (front panel via PC503, MCU 14) / pulse train (MCU 52)
TRIP ............... overcurrent trip node (IC610 out, D512/D513, MCU 45)
CT_P / CT_Q ........ T700 secondary (heater current)"""
root_notes = [("""THERMOMIX TM31-4C (120 V) POWER BOARD  NPVTM31LTA-3  -  REVERSE-ENGINEERED SCHEMATIC  rev 0.1 (2026-11)

HOW TO READ THIS PROJECT
- Netlist style: every pin connects through a short wire to a GLOBAL LABEL; identical labels are the same net across all sheets.
- References are the board's silkscreen references.  RXn / CXn / DXn = part present on the board whose reference was not read.
- 'not read' = marking or value unreadable.  'approx' / APPROXIMATE = connection inferred from photos or partial tracing, not confirmed by continuity.
- GND = MCU ground = motor DC bus negative (NOT neutral, NOT earth).  Everything except the CN300 'COLD' corner is at mains potential.
- Off-board items (bowl heater, motor windings, motor NTC) are drawn for clarity and excluded from the BOM.

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
- Shorted triac (230 V forum reports) -> continuous heating, error 69.   F100 open / R115 open -> no motor.
- Service-guide bowl values: 'sensor 48-55 ohm' is actually the 230 V heater; 'heater 110-130 kohm' is the bowl NTC.  120 V heater = 12.8 ohm.""",
               15.24, 96.52, 1.5), (legend, 228.6, 96.52, 1.5)]
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
print("written", len(sheets) + 1, "sheets;", sum(len(sh.parts) for sh in sheets), "parts")
