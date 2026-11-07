# 12 — Measurements

All measured on this machine (TM31-4C, 120 V). "In-circuit" readings include parallel paths and are only indicative.

## Bowl, motor and sensors (out of circuit)

| What | Where | Value |
|---|---|---|
| Bowl heater (120 V bowl) | bowl contacts | **12.8 Ω** |
| Bowl NTC | bowl contacts | **~130 kΩ** at room temperature |
| Motor phase windings | CN501 unplugged: 1–3, 1–5, 2–4, 2–6 | **8.5 Ω** each; 1–4, 1–6, 2–3, 2–5 open |
| Motor NTC | CN502 cable, pins 1–5 | **12.56 kΩ** at room temperature, drops when warmed |

## Board (unpowered)

| What | Value | Notes |
|---|---|---|
| RY200 coil (across D224) | 348 Ω | Normal 12 V coil |
| RY202 coil (across D223) | 354 Ω | Normal |
| RY201 coil | 390 Ω | Normal |
| Freewheel diodes CN501 pins 3–6 → VBUS | 0.475 V each (diode mode) | D500, D506, D508, D507 |
| R100, R107, R112 | 680 kΩ each | |
| F100 far end → DB100 | ~2.4 MΩ | Through bleeders (3 × 680 kΩ) + R114 |
| MCU 11 / 12 → GND | 47 kΩ | Permit pull-downs |
| MCU 33 → +5 V | 9.87 kΩ | In-circuit |
| CN502 pin 1 path → MCU 31 | ~975 Ω | ~1 kΩ series |
| IC611 pin 8 → IR2106 pin 1 (VGATE) | ~0.78 kΩ | In-circuit |
| IC611 pin 8 → +5 V / C200 + / C230 + / C500 + | 4.5 kΩ / 10.6 kΩ / 1.375 kΩ / 13 MΩ | In-circuit |
| IC611 pin 4 → C230 − | 0 Ω (beep) | Negative rail |
| Q510 / Q512 collectors → VGATE | ~33 Ω | |
| Totem-pole outputs → IGBT gates | 466 Ω (own IGBT), ~20 kΩ (other) | |
| Original CR700 A1 leg near body → pad | **open** | The fault (cracked leg) |

## Powered (floating DMM, heat requested, before the repair)

| What | Value | Meaning |
|---|---|---|
| Triac MT1–MT2, idle | 1.2–1.5 VAC | Floating node (A1 disconnected) |
| Triac MT1–MT2, heat requested | 2.7–4.7 VAC | Pickup only |
| Across heater | ~0 V | Heater not the open element |
| Relay clicks | 3 at power-up, independent of heat request | Relays = power-on / pre-charge sequence |

## Reference values from other sources (230 V boards)

| What | Value | Source |
|---|---|---|
| Original triac (230V model) | BTA12-600BW | CommentReparer forum |
| Shorted triac symptom | continuous heating, error 69 | Forum, Vorwerk service procedure |
| Triac in-circuit, 120 V board (forum) | ~73 Ω between outer legs | CommentReparer forum (in-circuit) |
| Heating test | 1 L water, 80 °C, speed 1, 11 min: 30→70 °C in < 4 min, ±5 °C | Vorwerk service procedure |
| Varoma test | 15 min Varoma, speed 1, no cup: 220–270 g water lost | Vorwerk service procedure |
