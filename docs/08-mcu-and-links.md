# 08 — MCU, programming header and front-panel link

Schematic sheet: **MCU, programming header & front-panel link**.

## MCU

- Marking: `D78F0034BCC` (last letters uncertain, likely `BGC`), `1402KP201`, `JAPAN`.
- Part: **NEC (now Renesas) µPD78F0034B**: 8-bit 78K0 core, 32 KB flash, 1 KB RAM, 10-bit 8-channel ADC, UART,
  2 × 3-wire serial, 64-pin QFP (14 × 14 mm, "GC" package).
- Pin numbers below follow the QFP drawing on p. 6 of the µPD78F0034 datasheet.

### Pin map

| Pin | Name | Use on this board |
|---|---|---|
| 1 | P50/A8 | HIN1 → R510 → IC501 pin 2 (Q501 high side) |
| 2 | P51/A9 | LIN1 → IC501 pin 3 (Q503) |
| 3 | P52/A10 | HIN2 → R511 → IC502 pin 2 (Q502 high side) |
| 4 | P53/A11 | LIN2 → R572 → IC502 pin 3 (Q504) |
| 5 | P54/A12 | Q505 driver (via Q511), inverted |
| 6 | P55/A13 | Q500 driver (via Q507), inverted |
| 9, 42 | VSS0, VSS1 | GND |
| 10, 24 | VDD0, VDD1 | +5 V |
| 11 | P30 (open-drain) | PERMIT1 (relay permit, veto/read) |
| 12 | P31 (open-drain) | PERMIT2 |
| 13 | P32 (open-drain) | WD2 (watchdog timer 2 output) |
| 14 | P33 (open-drain) | ARM (watchdog timer 1 arm; front panel via PC503) |
| 16 | P35/SO31 | Gate-drive enable read-back/veto (Q205 base) |
| 18 | P20/SI30 | CN503 pin 5 (programming SI) |
| 19 | P21/SO30 | CN503 pin 3 (programming SO) |
| 20 | P22/SCK30 | CN503 pin 7 (programming clock) |
| 21 | P23/RxD0 | UART receive ← PC502 (from front panel) |
| 22 | P24/TxD0 | UART transmit → PC501 (to front panel) |
| 25 | AVSS | GND |
| 29 | P14/ANI4 | Motor current (IC611 B via R605 51 kΩ) |
| 31 | P12/ANI2 | Motor NTC (CN502 pin 1 via ~1 kΩ) |
| 33 | P10/ANI0 | Pre-charge/mains sense (D107, R110, R111, JD1); ~10 kΩ to +5 V |
| 34, 35 | AVREF, AVDD | +5 V |
| 36 | RESET | CN503 pin 2 (reset circuit not traced) |
| 38 | XT1 | +5 V (subsystem clock unused) |
| 39 | VPP | CN503 pin 6 |
| 40, 41 | X2, X1 | Resonator (not traced) |
| 43 | P00/INTP0 | Rotor position B (CN502 pin 3 via 20 kΩ) |
| 44 | P01/INTP1 | Rotor position A (CN502 pin 2 via 20 kΩ) |
| 45 | P02/INTP2 | Overcurrent TRIP (R535) |
| 49 | P72/TO50 | RY201 driver (Q202) |
| 51 | P74/PCL | Heater triac command (PC700 LED cathode) |
| 52 | P75/BUZ | Watchdog pulses (IC503 1B/2B) |
| others | — | Not traced (7, 8, 15, 17, 23, 26–28, 30, 32, 37, 46–48, 50, 53–64) |

## CN503: flash programming header (2 × 4, not connected in the machine)

NEC 3-wire serial (CSI30) flash programming interface.

| Pin | Signal | MCU pin |
|---|---|---|
| 1 | GND | 9, 25, 42 |
| 2 | RESET | 36 |
| 3 | SO30 | 19 |
| 4 | +5 V (VDD) | 10, 24, 34, 38 |
| 5 | SI30 | 18 |
| 6 | VPP | 39 |
| 7 | SCK30 | 20 |
| 8 | Not connected | — |

Numbering: pins 1 and 2 share the row at the silkscreen "1 2" end; odd pins in pin 1's column. The resistance readings
from pin 2 (~20–22 kΩ to several MCU pins) are paths through the reset pull-up and other pull-ups via +5 V.

## CN300: front-panel link (blue cable, ISOLATED side)

| Pin | Signal | Path |
|---|---|---|
| 1 | GND_COLD | Cold-side ground (C210 −) |
| 2 | Data from panel | → Q506 (BC846) → PC502 LED → MCU RxD0 (pin 21) |
| 3 | VCOLD | Isolated supply from T100 (D214, C210, R211) |
| 4 | Data to panel | ← PC501 transistor ← MCU TxD0 (pin 22) |
| 5 | Panel enable | PC503 LED (directly between pins 5 and 1) → ARM (watchdog timer 1) |

- Optocouplers PC501–PC503: marking `816C`, Lite-On **LTV-816** (4-pin phototransistor). PC501 is mounted rotated
  relative to PC502/PC503: its LED is on the hot side (MCU → panel), while PC502/PC503 have their LEDs on the cold side.
- LTV-816s are slow phototransistor parts, so the link is probably ≤ 9600 baud.
- **Approximate:** Q506's exact role, LED polarities, and the values of the pull-up/LED resistors on the cold side.

See [15-future-work.md](15-future-work.md) for how to sniff and decode this link safely.
