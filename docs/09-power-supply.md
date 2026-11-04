# 09 — Low-voltage power supply

Schematic sheet: **Low-voltage power supply (flyback)**. Status: **structure confirmed**; transformer pin-out and most
values not traced, so the sheet is a functional diagram.

## Structure

```
mains (before the relays) ─ F101 T1AH 250V ─ [Z101 varistor: position empty] ─ bridge D100–D103
   ─ L101 filter choke ─ C110 22 µF 400 V ─ T100 (D1D8A) primary ─ IC100 Panasonic MIP2E3D (switcher + MOSFET)
   clamp ZD101 / D104 ; aux winding feeds IC100 VDD
   feedback: IC200 TL431 + PC100 opto, regulating the hot-side +5 V
```

The supply must be fed **before** RY200/RY202, because it powers the MCU that closes them. Whether it taps mains
before or after L103 was not confirmed.

## Outputs

| Rail | Rectifier / capacitor | Reference | Used by |
|---|---|---|---|
| **V12RAW** (~12–15 V) | D201 / C200 | GND (hot) | Relay coils, Q206 → VGATE (gate drivers), AND-gate pull-ups |
| **+5 V** | D220 / C220 | GND (hot) | MCU, 74HC123, IC700, IC610, PC700 LED, pull-ups |
| **VNEG** (negative) | D230 / C230 (**C230 + on GND**) | GND (hot) | IC611 pin 4 |
| **VCOLD** | D214 / C210, R211 across C210 | GND_COLD (isolated) | Front panel via CN300 |
| **VGATE** | switched from V12RAW by Q206 | GND (hot) | IR2106 pin 1, discrete IGBT drivers, IC611 (via ~0.78 kΩ?) |

## Parts

| Ref | Marking | Notes |
|---|---|---|
| F101 | T1AH 250V | Supply input fuse |
| IC100 | MIP2E3DMY | Panasonic IPD flyback switcher. Forum reports MIP2E1DMY on 230 V boards |
| T100 | D1D8A 3N2E | Only flyback transformer on the board |
| L101 | black choke near F101 | **Not a transformer** (first photo map mislabelled it "T101") |
| IC200 | `3CW40KI TL431I` (TI) | Shunt reference for feedback |
| PC100 | opto | Feedback to IC100 |
| Z101 | — | Footprint empty on this board |

## Diagnostics

| Symptom | Check |
|---|---|
| Machine completely dead | F101; IC100 (forum: MIP2E1DMY failures on 230 V boards); C110; bridge |
| Power-up loop / flickering display | Low-voltage rails under load; C200/C220 (ESR); IC100 |
| Relays never click, panel lights | V12RAW (C200) |

Safe measurement points: across capacitor leads only, with clip leads attached while unplugged. Hot rails: reference
**C220 −** (= GND = CN503 pin 1). VCOLD: across C210's own leads.
