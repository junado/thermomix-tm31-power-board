# 05 — Motor drive: 4-phase switched-reluctance motor

Schematic sheet: **Motor power stage (4-phase SR)**. Status: **confirmed**, except where marked approximate.

## Motor

- Vorwerk "reluctance motor", **8 stator poles, 4 phases**, each winding **8.5 Ω** (measured at CN501, unplugged).
- The phases are paired on **shared high-side switches**:

| Phase (CN501 pins) | High-side switch | Low-side switch |
|---|---|---|
| 1 – 3 | Q501 (MCU pin 1 via IC501) | Q503 (MCU pin 2 via IC501) |
| 1 – 5 | Q501 | Q500 (MCU pin 6, discrete driver, inverted) |
| 2 – 4 | Q502 (MCU pin 3 via IC502) | Q504 (MCU pin 4 via IC502) |
| 2 – 6 | Q502 | Q505 (MCU pin 5, discrete driver, inverted) |

Phases that share a high-side switch are non-adjacent in the firing sequence, the standard layout for this topology.
Rotor position comes from two sensors on a small board inside the motor (CN502, see [07](07-analog-sensing.md)).

## Power stage

```
VBUS ──┬── Q501 C   Q501 E ── MOT1 (CN501.1) ──┬── windings to MOT3, MOT5
       └── Q502 C   Q502 E ── MOT2 (CN501.2) ──┴── windings to MOT4, MOT6
MOT3 ── Q503 C,  MOT4 ── Q504 C,  MOT5 ── Q500 C,  MOT6 ── Q505 C
Low-side emitters = LS_EMIT ──[R600 0.27 Ω ∥ R601 0.27 Ω]── GND   (motor current shunt)

Freewheel diodes (all ~0.475 V in diode mode):
  D504: GND → MOT1      D505: GND → MOT2
  D500: MOT3 → VBUS     D506: MOT4 → VBUS     D508: MOT5 → VBUS     D507: MOT6 → VBUS
```

- IGBTs Q500–Q505: marking **G04N60** (Infineon SGP04N60-type, 600 V, 4 A), TO-220, on the heatsink.
- When a switch opens, the winding's energy returns to the bus through the freewheel diodes.

## Gate drivers

| Driver | Inputs (from MCU) | Outputs |
|---|---|---|
| IC501 IR2106S | HIN = MCU 1 (P50) via R510; LIN = MCU 2 (P51) | HO → Q501 gate; LO → 470 Ω → Q503 gate; VS = MOT1 |
| IC502 IR2106S | HIN = MCU 3 (P52) via R511; LIN = MCU 4 (P53) via R572 | HO → Q502 gate; LO → 470 Ω → Q504 gate; VS = MOT2 |

- IR2106 pin 1 (VCC) = **VGATE**, a supply that only exists while the safety logic allows it
  (Q205/Q206, see [06](06-safety-logic.md)). COM (pin 4) = GND.
- Bootstrap: C500 (IC501) and C506 (IC502) with diodes from VGATE (D514/D518 and D517/D519 area; exact pairing
  approximate).

### Discrete drivers for Q500 and Q505

```
MCU pin 6 (P55) ─[R562 30 kΩ ∥ speed-up C]─ Q507 base      Q507: NPN, emitter GND, collector = DRVB500
VGATE ─[2.2 kΩ, via JA7]─ DRVB500 = bases of Q512 (NPN) and Q513 (PNP)
Q512 collector ─[~33 Ω]─ VGATE ;  Q513 collector ─ GND ;  emitters joined = DRV500
DRV500 ─[470 Ω]─ Q500 gate ;  gate ─[47 Ω]─ D511 ─ DRV500 (fast turn-off) ;  gate ─[10 kΩ]─ LS_EMIT
```

The Q505 driver is identical: MCU pin 5 (P54) → Q511 → Q510 (NPN) / Q514 (PNP) → 470 Ω → Q505 gate, 2.2 kΩ pull-up
via JB5, R517 gate–emitter.

**Inverted logic:** MCU pin high → Q507/Q511 on → totem-pole output low → IGBT off.
During an MCU reset the pins float, which would turn these IGBTs on. That is harmless because VGATE is off whenever the
watchdog is not running.

Resistor codes: SMD "471" = 470 Ω, "470" = 47 Ω, "222" = 2.2 kΩ, "303" = 30 kΩ.

## Hardware overcurrent cut-off

```
IC501 HIN ──|>|── D512 ──┐
IC502 HIN ──|>|── D513 ──┼── TRIP ──[R535]── MCU pin 45 (INTP2, interrupt)
IC610 (LM393) output A ──┘  (via JC11)
IC610 output B ── empty footprint (second trip not fitted on this board)
```

When the comparator pulls TRIP low, D512/D513 force both high-side inputs low, so Q501/Q502 switch off in hardware.
The MCU is interrupted at the same time.

## Diagnostics

| Symptom | Likely area |
|---|---|
| Error 34 (motor does not turn) | Liquid in the motor/sensor board; sensor board; IGBTs; F100; R115 |
| Error 38 / 39 (motor drive) | IGBTs, IR2106, motor cable/connector CN501 |
| Rough rotation, weak heating ("tachometer" fault per Vorwerk) | Sensor board (CN502) or position signals |
| Breaker trips when turning the speed knob | Shorted IGBT or freewheel diode |

Out-of-circuit IGBT check (diode mode): no conduction C–E in either direction (SGP type has no internal diode);
gate–emitter open.
