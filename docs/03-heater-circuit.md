# 03 — Mains input and heater circuit

Schematic sheet: **Mains input & heater** ([hardware/](../hardware/README.md)). Status: **confirmed by continuity**
unless marked.

## Circuit

```
CN100 (BLACK, live) ──┬── L103 ── L_F ──[RY200]── NODE_Y ──┬──[T700 primary]── HEAT_HI = CN703 ══ bowl heater ══ CN704 = HEAT_LO
                      │                                    └──[F100]── motor bus (see 04)                                 │
                     CX102 (+ bleeders R103–R105)                                                                         │
                      │                                                                                       A1 ─[CR700]─ A2
CN101 (WHITE, neutral)┴── L103 ── N_F ──[RY202]── JC12/JC13/JC14 ── NODE_X ────────────────────────────────────────────────┘
                                                                     ├── PC700 pin 4 (MT)
                                                                     ├── R115 pre-charge, RY201 NO (see 04)

Triac firing:   +5V ─R713─ PC700 pin 1 (LED anode) ; PC700 pin 2 (LED cathode) ── MCU pin 51 (P74, pulls low = fire)
                PC700 pin 6 ─R714 180 Ω─R715 180 Ω─ CR700 gate ;  PC700 pin 4 ── NODE_X (= A2)
```

## Parts

| Ref | Part | Notes |
|---|---|---|
| CN100 / CN101 | Spade tabs, BLACK / WHITE | Live / neutral input |
| L103 | Common-mode choke | Neutral winding on the CN101 side, live winding on the CN100 side |
| CX102 | X2 capacitor | Across the input, with bleeders R103–R105 (values not read) |
| CY103 / CY104 | Y capacitors | Far ends not traced |
| RY200 | Schrack (TE) RTH34012WG, 12 V DC, 16 A | **Live** relay. Coil ~348 Ω (measured across D224) |
| RY202 | Schrack (TE) RTH34012WG, 12 V DC, 16 A | **Neutral** relay. Coil ~354 Ω (measured across D223) |
| JC12–JC14 | Three parallel wire jumpers | Carry heater current from RY202 to NODE_X, hopping over a signal bus |
| T700 | HARTU 711078-51 current transformer | Heavy winding in series with the heater; secondary via JD5/JD6 to IC611 (see 07) |
| CN703 / CN704 | Spade tabs | Heater ends (via the bowl contact module) |
| CR700 | Triac, TO-220, riveted to heatsink | Original: ST, part number rubbed off, date 409. Replacement **BTA24-600BW** |
| PC700 | MOC3063 (zero-cross opto-triac, 6-DIP) | Pins 3 and 5 unused |
| R714, R715 | 180 Ω each | Gate resistors in series (360 Ω) |
| R713 | Value not read | LED current resistor from +5 V |

## How it works

- Both relays close at power-up and stay closed (see [06-safety-logic.md](06-safety-logic.md)). They are not the
  heat control: **the triac is**.
- The MCU fires PC700 by pulling its LED cathode low. The MOC3063's zero-cross detector turns the triac on near the
  voltage zero, so heating power is controlled by whole-cycle bursts.
- T700 lets the board measure heater current (and detect current that should not be there).
- **There is no fuse in the heater path on this board.** F100 is the motor bus fuse (see [04](04-motor-dc-bus.md)).

## Triac replacement notes

| Item | Requirement |
|---|---|
| Type | **BTA** (insulated tab) — the heatsink is at ~340 V DC. Never BTB |
| Rating | BTA24-600BW recommended on 120 V (heater ~9.4 A RMS). BTA12-600BW is the 230 V original |
| Gate | "BW" suffix (50 mA, snubberless). Avoid CW/SW (more sensitive, false triggering) |
| Pinout | TO-220AB: A1, A2, G, reading left to right with the marking facing you. Silkscreen marks G and A1 |
| Mounting | Drill out the rivet; thermal paste; M3 screw, lock washer, nut; firm but not excessive torque |
| Legs | Re-create the **C-bend** strain relief, at least 2–3 mm from the body, around a ~2 mm mandrel |
| Checks before power | CN704 → A1 leg *at the body*: beep. NODE_X → A2: beep. A1–A2: open. A1/A2/G → heatsink: open (MΩ) |

Unpowered triac test (out of circuit): gate to A1 about 10–100 Ω, A1 to A2 open in both directions.

## Bowl values (120 V bowl)

| Measured | Value |
|---|---|
| Heater element | **12.8 Ω** → ~1.1 kW and ~9.4 A at 120 V (~1.26 kW at 127 V) |
| Bowl NTC | **~130 kΩ** at room temperature |

The service guide's values ("sensor 48–55 Ω, heater 110–130 kΩ") have their labels swapped: 48–55 Ω is the
**230 V heater** (~53 Ω = 1 kW at 230 V) and 110–130 kΩ is the NTC. **Never swap bowls between versions**: a 120 V bowl
on 230 V would draw ~4 kW; a 230 V bowl on 120 V gives only ~270 W.
