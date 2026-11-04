# 01 — Repair log: "TM31 does not heat"

Machine: Thermomix **TM31-4C**, North American 120 V version.
Power board: **NPVTM31LTA-3** (Panasonic Electronic Devices Europe), date codes from 2014.

## 1. Symptom (2026-10-16)

- No heating at any temperature setting. **No error code.**
- Bowl temperature is displayed correctly (tested by pouring hot water into the bowl).
- Temperature keys work and the machine appears to "ask" for heat (temperature LED behaves normally).
- Motor works.
- With the machine open, **no 120 V at the heater outputs** while heat was requested.
- A first continuity check of the power board (unpowered) found nothing obviously wrong.

## 2. Research and first hypotheses

Sources: CommentReparer.com forum threads and a TM31 technical intervention procedure (see
[16-references.md](16-references.md)).

| Hypothesis | Basis | Outcome |
|---|---|---|
| Heater triac failed **open** or gate drive dead | Forum: the TM31 heater triac (BTA12-600BW on 230 V boards) is the classic failure | Partly right: triac circuit, but mechanical |
| Triac failed **short** | Forum: shorted triac → runaway heating, **error 69** | Rejected: symptom is no heat, not overheating |
| Bowl heater or contacts | Service guide bowl checks | Rejected: bowl reads fine and temperature works |
| Relay contacts burnt | High heater current (~9 A at 120 V) | Rejected later by the voltage readings |
| Cracked solder joint on a high-current part | Single-layer phenolic board, heat cycling, vibration | **Close: a cracked leg, not a joint** |
| Board replacement | One forum user with identical symptoms bought a used board | Not needed |

Note on unpowered testing: an **open** triac and a good triac both read "infinite" between MT1 and MT2, so continuity
tests cannot distinguish them. That's why the original check found nothing.

## 3. Triac identification (2026-10-17)

- The original triac's part-number line is rubbed off. Remaining marking: ST logo, `GK1 SJ`, `CHN`, `409`.
  **`409` is the assembly date code** (2004, week 9), not a part number.
- 230 V boards use a BTA12-600BW. For the 120 V heater (12.8 Ω → ~9.4 A RMS), a **BTA24-600BW** is the better
  choice: same TO-220AB package and pinout, same 50 mA "BW" gate sensitivity, more current margin and lower losses.
- **Must be a BTA (insulated tab)**: the triac is riveted to a heatsink that is later found to sit at the motor DC bus
  positive (~340 V). A BTB (live tab) would connect that heatsink to mains through the triac.

## 4. Tracing the heater path (2026-10-22)

From photos and continuity tests (details in [03-heater-circuit.md](03-heater-circuit.md)):

```
CN100 live ─ L103 ─[RY200]─ NODE_Y ─[T700 primary]─ CN703 ══ HEATER ══ CN704 ─ A1 ─[CR700]─ A2 = NODE_X ─[RY202]─ L103 ─ CN101 neutral
```

Measurements that pointed to the fault:

| Test (machine powered, heat requested, floating DMM) | Result | Meaning |
|---|---|---|
| Relays | 3 clicks at power-up, **with or without** heat requested | Relays are power-on relays, not "heat on" relays |
| AC across triac MT1–MT2, idle | 1.2–1.5 VAC | **Not** the 120 V expected if the loop were closed and the triac off |
| AC across triac MT1–MT2, heat requested | 2.7–4.7 VAC | Floating node: stray pickup only |
| AC across heater | ~0 V | Heater not open either (it would show 120 V) |

**Conclusion:** the series loop was open somewhere other than the triac's junction or the heater.

## 5. Root cause found

The user reported difficulty getting continuity from the probe on the triac leg to its pad on the other side.

- **CN704 beeped to the A1 pad, but not to the A1 leg near the triac body.**
- The A1 leg **cracked at its C-shaped bend**, the strain-relief bend formed near the PCB.
- The solder joint itself was fine; reflowing it would not have fixed anything.

Mechanism: the triac is fixed to a heatsink while its legs are soldered to a board that moves relative to it.
Motor vibration plus years of heat cycling at ~9 A fatigued the copper leg at the bend.

Diagnostic lesson: **check continuity from the leg right at the component body to the pad**, not only pad to pad.

## 6. Repair and the "timer" trap

1. Leg re-soldered: continuity from CN704 to the A1 leg was restored.
2. First test: **still no heat**. A full voltage-by-voltage test plan was prepared.
3. Re-test with a **time set and speed running**: heating works. The TM31 only heats while the timer is set and the
   blade turns. The second "failure" was a test-procedure error.
4. A BTA24-600BW was ordered for a permanent replacement (re-create the C-bend around a ~2 mm mandrel, at least
   2–3 mm from the body; thermal paste; M3 screw instead of the original rivet; verify A1/A2/G to heatsink is open).

Verification test from the service procedure: 1 L of water, 80 °C, speed 1, 11 minutes. 30 → 70 °C must take
< 4 minutes; final temperature within ±5 °C.

## 7. Afterwards: full reverse-engineering

With the board out, tracing continued so that the next failure (on this or any TM31) can be diagnosed from a
schematic instead of guessing. Timeline:

| Date | Milestone |
|---|---|
| 2026-10-22 | Component-side photo map; heater path; fault found and repaired |
| 2026-10-23 | Solder-side quadrant photos; doubler, pre-charge and supply structure; chip markings (MCU, IR2106, LM393, TLC277) |
| 2026-10-25 | MCU pinout from datasheet; CN503 = flash programming header; IC503 = 74HC(T)123 watchdog |
| 2026-10-30 | Relay drivers and diode-AND permit logic; motor phase/driver mapping; overcurrent trip |
| 2026-11-03 | Gate-drive enable, IC700 latching permits, sensor board connector, freewheel diodes; KiCad schematic rev 0.1 |
| 2026-11-03 | Schematic rev 0.2: redrawn as wired circuits (same netlist); MCU datasheet archived |
