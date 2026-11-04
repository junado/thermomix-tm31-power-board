# 07 — Analog sensing: currents, overcurrent trip, motor sensor board

Schematic sheet: **Analog sensing**. Status: **partly confirmed**. Gain networks and some links are approximate.

## Chips

| Ref | Marking | Part | Supply |
|---|---|---|---|
| IC611 | `277C` (TI logo) | TI **TLC277** dual precision op-amp | Pin 8 from the VGATE side (~0.78 kΩ in-circuit, exact feed not traced); pin 4 = **VNEG** (negative rail, C230) |
| IC700 | `277C` (TI logo) | TI **TLC277** | +5 V / GND (see [06](06-safety-logic.md)) |
| IC610 | `393` (ST logo) | ST **LM393** dual comparator | +5 V / GND |

Pin layout of all three (standard 8-pin dual): 1 OUT A, 2 −IN A, 3 +IN A, 4 V−/GND, 5 +IN B, 6 −IN B, 7 OUT B, 8 V+.
On the board, pins 4 and 5 sit on enlarged pads (wave-solder "thief" pads), which confirms all three chips share
one orientation.

## IC611 half A: heater current (T700)

```
T700 secondary (via JD5/JD6) ── CT_Q ──[300 Ω]── −IN A ──[68 kΩ ∥ C]── OUT A
                                 CT_P ── +IN A
D700 / D701: back-to-back clamp between CT_Q and CT_P
```

A current-to-voltage converter: the CT secondary current flows into the inverting input; output = I × 68 kΩ, filtered
by the capacitor. The clamp diodes protect the op-amp from CT spikes. The negative rail lets the output swing both
ways for the AC signal.
**Not traced:** where CT_P is referenced, and where OUT A goes (probably to IC700 via D601).

## IC611 half B: motor current

```
LS_EMIT (shunt R600 ∥ R601, 0.135 Ω) ─[22 kΩ]─ −IN B ;  +IN B ─[180 kΩ]─ (shunt side, approximate)
OUT B ─[R605 51 kΩ]─ IMOT ─ C612 ─ GND ;  IMOT = MCU pin 29 (ANI4)
OUT B also feeds IC610's inputs (path not traced)
```

Gain roughly ×8 (180 kΩ / 22 kΩ), not confirmed.

## IC610: overcurrent comparator

- Output A → JC11 → **TRIP** node (D512/D513 cathodes, R535 → MCU 45). Hardware cut-off of the high-side IGBTs (see
  [05](05-motor-drive.md)).
- Output B → unpopulated footprint (second trip function not fitted on this board version).
- Inputs: not traced (motor current from IC611 B, plus a reference).

## Motor sensor board (CN502)

A small board inside the motor ("tachometer board" in Vorwerk's service guide).

| CN502 pin | Signal | To MCU |
|---|---|---|
| 1 | Motor NTC (**12.56 kΩ** at room temperature → 10 kΩ @ 25 °C type; resistance drops when warmed) | ~1 kΩ (975 Ω in-circuit) → pin 31 (ANI2) |
| 2 | Rotor position sensor A | 20 kΩ → pin 44 (INTP1) |
| 3 | Rotor position sensor B | 20 kΩ → pin 43 (INTP0) |
| 4 | Sensor supply | From Q508 emitter (zener follower) |
| 5 | GND | MCU pin 9 (VSS0) |

Sensor supply regulator: raw supply → R512 → Q508 collector (C512 filter); ZD500 zener holds the base; emitter →
CN502 pin 4. The source feeding R512 (V12RAW assumed) and the base bias resistor were not traced. ZD500's voltage was
not read.
