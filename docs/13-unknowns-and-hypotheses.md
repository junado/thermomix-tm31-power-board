# 13 — Confidence levels, hypotheses and unknowns

## Confirmed by continuity and/or measurement

- Complete heater current path, relays, triac firing (PC700, R714/R715, MCU 51).
- Voltage doubler: F100 → capacitor midpoint; DB100 AC pins tied; bus polarity; balancing resistors present.
- Pre-charge: R115 (6.8 Ω TF 139 °C) + R114 (15 Ω), RY201 COM/NO/NC roles, D107 sense → MCU 33.
- Motor: 4 phases, pairing on CN501, all 6 IGBTs' roles, all 6 freewheel diodes, both IR2106 drivers and their MCU
  pins, both discrete totem-pole drivers and their MCU pins.
- Overcurrent trip: IC610 out A → JC11 → D513/D512 → HIN lines, R535 → MCU 45.
- Relay drivers Q200/Q204/Q202, diode-AND inputs, 47 kΩ pull-ups and pull-downs.
- VGATE switch Q205/Q206 and its 3 × 47 kΩ enable network from both AND nodes.
- 74HC123 watchdog: every pin.
- IC700 outputs → D707/D706 → MCU 11/12 (cathodes on the MCU lines), latch diodes D702/D703.
- CN300, CN502, CN503 pinouts; MCU pins listed in [08](08-mcu-and-links.md).
- Ground domains: GND = bus negative = MCU ground; C230 + on GND (negative rail); heatsink eyelet = VBUS.

## Inferred (high confidence, not directly proven)

| Item | Reasoning |
|---|---|
| IC700 latches remove the permits on a heater/motor current fault | Topology (latch diodes, permit diodes, watchdog-based threshold); purpose of T700 |
| Power-up order: RY200/RY202, then RY201 | 3 clicks heard; pre-charge circuit logic |
| MCU checks pre-charge before closing RY201; error 72 = this check failing | RY201 NC → D107 → ANI0; forum error-72 reports |
| Front panel can veto RY202 via PC503 → watchdog arm | Unless firmware also drives MCU 14 low |
| IC611 half A converts T700's current to a voltage | 300 Ω input, 68 kΩ ∥ C feedback, clamp diodes, negative rail |
| IC611 half B amplifies the shunt voltage ~×8 to MCU 29 | 22 kΩ / 180 kΩ, R605 51 kΩ + C612 |
| LTV-816 link speed ≤ 9600 baud | Slow phototransistor optocouplers |
| Board is the post-2012 revision (Vorwerk 30468) | 2014 date codes on parts |

## Unknown / not traced

| Item | How to resolve |
|---|---|
| IC700 inputs: D601 anode source, "JC3" signal, exact thresholds | Follow traces from D601 anode and JC3; scope during heating |
| Where IC611 OUT A goes, and CT_P's reference | Follow pin 1 trace past the 68 kΩ; beep CT_P to GND |
| IC611 motor-current gain network (exact feedback) | Trace pins 5–7 |
| IC610 inputs and reference | Trace pins 2, 3, 5, 6 |
| IC611 supply (pin 8 feed) | Find the resistor between pin 8 and VGATE |
| R548 and C514 values (watchdog time-outs) | Scope: time from last MCU pulse to 1Q / 2Q falling |
| Cold side: Q506 role, LED polarities, resistor values | Trace with the board out; or scope the link (see [15](15-future-work.md)) |
| Supply: transformer pin-out, IC100 pins, aux winding, divider for TL431 | Trace around T100/IC100 |
| SMPS tap point: before or after L103 | Beep F101 to CN100 vs L103 output |
| Z100 type, CY103/CY104 far ends | Inspect / beep |
| Bootstrap diode pairing (D514/D517/D518/D519) | Beep from VGATE to C500/C506 |
| D225/D226 series or parallel | Beep each diode's ends |
| MCU pins 7, 8, 15, 17, 23, 26–28, 30, 32, 46–48, 50, 53–64 | Follow traces; some may go to test pads or be unused |
| Resonator frequency (X1/X2), reset circuit | Inspect near the MCU |
| What reads the bowl NTC, scale and lid (front panel assumed) | Open the front panel |

## Hypotheses considered for the original fault (for the record)

| Hypothesis | Status |
|---|---|
| Triac failed open | Rejected (triac fine; its leg was cracked) |
| Gate drive / opto-triac failure | Rejected |
| Relay contacts burnt | Rejected |
| F100 blown (initially thought to be in the heater path) | Rejected; F100 is the motor fuse |
| Cracked solder joint | Close: it was the **leg** cracking at its C-bend |
| Bowl / heater element | Rejected (12.8 Ω, sensor works) |
