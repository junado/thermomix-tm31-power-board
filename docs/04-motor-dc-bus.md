# 04 — Motor DC bus: voltage doubler, pre-charge and bypass

Schematic sheet: **Motor DC bus (doubler) & pre-charge**. Status: **confirmed**, except where marked approximate.

## Circuit

```
NODE_Y (live after RY200) ──[F100 T6.3A]── MID ──┬── C109 (680 µF 200 V) ── VBUS (+, ~340 V) = heatsink
                                                 └── C108 (680 µF 200 V) ── GND (bus −) = MCU ground
                                                 R118–R121: balancing resistors, two per capacitor (pairing approximate)

NODE_X (neutral after RY202) ──┬──[R115 6.8 Ω, TF 139 °C]── PRECH ──[R114 15 Ω 5 W]──┬── DB100 AC1 + AC2 (tied together)
                               │                                                     │
                               └── RY201 NO          RY201 COM ──────────────────────┘
                                                     RY201 NC ── D107 ─ R110 ─ R111 ─ JD1 ── MCU pin 33 (ANI0)
DB100 + ── VBUS ;  DB100 − ── GND
CX101 (X2): MID side (assumed) ↔ PRECH, with bleeders R100 + R107 + R112 (680 kΩ each) in series across it
```

## Why a doubler

The motor, IGBTs and bus capacitors are the same design as the 230 V machine, which rectifies 230 V to ~325 V DC.
On 120 V, live feeds the midpoint of the two series capacitors and neutral feeds both AC pins of the bridge (two
diodes up, two down). Each capacitor charges to the 120 V peak (~170 V), so the bus is ~340 V. Only the front end
changes between versions.

Consequences:
- F100 carries roughly twice the motor current a 230 V board would.
- Each capacitor recharges once per mains cycle, so ripple is higher than with a bridge (hence the large capacitors).

## Pre-charge and the three clicks

1. RY200 and RY202 close. The capacitors charge through **R115 + R114 ≈ 22 Ω** (peak inrush ≈ 8 A).
2. RY201 is a **changeover** (1C) relay. At rest, its COM connects the bridge's AC node to **D107 → R110/R111 → MCU
   pin 33 (ANI0)**, so the MCU can measure that pre-charge voltage is present. That proves RY200/RY202 actually closed.
   Forum reports of error 72 ("power relay fault") fit this check.
3. RY201 energises: COM connects to **NO = NODE_X**, shorting the pre-charge resistors.

**R115 contains a thermal fuse (139 °C).** If RY201 failed to close, motor current would flow through the pre-charge
resistors; R115 would heat up and open to prevent a fire.

## Parts

| Ref | Marking / value | Function |
|---|---|---|
| F100 | T6.3AH 250V (in a holder) | Motor bus fuse |
| C108, C109 | 680 µF 200 V, 105 °C | Doubler capacitors |
| R118–R121 | SMD, value not read | Capacitor balancing |
| DB100 | SIP bridge rectifier (on heatsink) | Both AC pins tied |
| R115 | "A5MC 6.8ΩJ UMI 139°C" cement resistor | Pre-charge with built-in thermal fuse |
| R114 | "5W 15ΩJ" | Pre-charge |
| RY201 | Song Chuan 899-1C-F-C 12 V DC | Pre-charge bypass; coil 390 Ω; flyback D209 |
| CX101 | X2 capacitor | Bus input filter |
| R100, R107, R112 | 680 kΩ each (measured) | Bleeders across CX101 |
| D107, R110, R111 | 1N4007-type, values not read | Pre-charge/mains sense to MCU pin 33 |
| — | ~10 kΩ (9.87 kΩ in-circuit) from MCU pin 33 to +5 V | Bias/divider on the sense input |
| Z100 | Unmarked, probably a varistor | Not placed in the schematic |

## Diagnostics

| Symptom | Check |
|---|---|
| Motor dead, heater works | F100 continuity; R115 continuity (thermal fuse); RY201 contacts |
| Relays click but motor never starts / error 72 | D107/R110/R111 path; RY201 NC contact |
| Breaker trips | DB100, C108/C109, IGBTs (see [05](05-motor-drive.md)) |

> [!CAUTION]
> C108 + C109 hold ~340 V. Discharge through a resistor (e.g. 2 kΩ 5 W) and measure before handling.
> The heatsink is at VBUS.
