# 10 — Parts identification and values

Legend for **Confidence**: ✅ read/measured, 🟡 inferred from function or partially read, ❓ unknown.
SMD resistor codes: 3 digits = 2 significant + multiplier (`473` = 47 kΩ, `471` = 470 Ω, `470` = 47 Ω);
4 digits = 3 significant + multiplier (`5102` = 51.0 kΩ, `6802` = 68.0 kΩ, `3000` = 300 Ω).
In-circuit resistance readings are approximate (parallel paths).

## Semiconductors and ICs

| Ref | Marking | Identified as | Function | Conf. |
|---|---|---|---|---|
| IC1 (ref not read) | D78F0034BCC 1402KP201 JAPAN | NEC/Renesas µPD78F0034B, 64-QFP | Power-board MCU | ✅ |
| IC100 | MIP2E3DMY | Panasonic MIP2E3D IPD | Flyback switcher | ✅ |
| IC200 | 3CW40KI TL431I | TI TL431 | SMPS feedback reference | ✅ |
| IC501, IC502 | IR2106S 403P | Infineon/IR IR2106S | High/low-side gate drivers | ✅ |
| IC503 | 74H?123? (DY106) | 74HCT123D / 74HC123 | Dual retriggerable one-shot (watchdog) | ✅ family / 🟡 suffix |
| IC610 | 393 GZ405 (ST) | ST LM393 | Overcurrent comparator | ✅ |
| IC611 | 277C (TI) | TI TLC277 | Heater CT amp (A) + motor current amp (B) | ✅ |
| IC700 | 277C (TI) | TI TLC277 | Latching fault comparators (permits) | ✅ |
| CR700 | ST, part no. rubbed off, date 409 | BTA-series triac (BTA12-600BW on 230 V boards) | Heater switch | 🟡 → replaced by BTA24-600BW |
| PC700 | MOC3063 (Fairchild logo) | MOC3063 zero-cross opto-triac | Triac firing | ✅ |
| PC501–PC503 | 816C (Lite-On) | LTV-816 | Front-panel link optocouplers | ✅ |
| PC100 | — | Optocoupler | SMPS feedback | 🟡 |
| Q500–Q505 | G04N60 | Infineon SGP04N60-type IGBT, 600 V | Motor switches | ✅ (Q501/Q502 read; others same look) |
| Q200, Q202, Q204, Q205, Q507, Q508, Q510, Q511, Q512 | — | Small NPN (BC846-type, SOT-23) | Relay drivers, enables, gate drivers, regulator | ✅ type by diode test |
| Q206, Q513, Q514 | — | Small PNP (SOT-23) | VGATE switch, gate drivers | ✅ type by diode test |
| Q506 | 1B W33 | BC846 (NPN) | Cold-side link | ✅ |
| DB100 | — | SIP bridge rectifier | Motor bus (doubler) | 🟡 marking not read |
| D100–D103 | — | Rectifier diodes | SMPS input bridge | 🟡 |
| D500, D504–D508 | — | Fast diodes | Motor freewheel (0.475 V) | ✅ function |
| D107 | — | 1N4007-type | Pre-charge sense | 🟡 |
| D209, D223, D224 | — | SMD diodes | Relay flyback (RY201, RY202, RY200) | ✅ |
| D210, D212, D213, D215, D221, D222, DX3 | — | SMD diodes | Relay diode-AND inputs | ✅ |
| D225, D226 | — | Diodes | Relay driver emitter threshold | ✅ (series/parallel 🟡) |
| D512, D513 | — | Diodes | Overcurrent trip to HIN | ✅ |
| D511, DX2 | — | Diodes | IGBT fast turn-off (Q500, Q505) | ✅ |
| D514/D517 (+D518/D519) | — | Diodes | IR2106 bootstrap | 🟡 |
| D601, D700–D703, D706, D707 | — | Diodes | Analog/latch/permit | ✅ (D601 role 🟡) |
| ZD500 | — | Zener (voltage not read) | Sensor supply reference | ✅ |
| ZD101, D104 | — | Zener + diode | Flyback clamp | 🟡 |
| D201, D214, D220, D230 | — | Rectifiers | SMPS outputs | ✅ |

## Electromechanical and magnetic

| Ref | Marking | Notes | Conf. |
|---|---|---|---|
| RY200, RY202 | SCHRACK RTH34012WG, 12VDC, 16A/250VAC, (TE) | Live / neutral relays. Coils ~348 / ~354 Ω | ✅ |
| RY201 | 899-1C-F-C E 12V-DC (Song Chuan) | Pre-charge bypass (changeover). Coil 390 Ω | ✅ |
| T700 | HARTU 04/14 711078-51 | Heater current transformer | ✅ |
| T100 | D1D8A 3N2E | Flyback transformer | ✅ |
| L103 | — | Mains common-mode choke | ✅ |
| L101 | — | SMPS filter choke | ✅ |
| F100 | T6.3AH 250V | Motor bus fuse | ✅ |
| F101 | T1AH 250V | SMPS fuse | ✅ |

## Passives with known values

| Ref | Value | Function | Conf. |
|---|---|---|---|
| C108, C109 | 680 µF 200 V 105 °C | Doubler capacitors | ✅ |
| C110 | 22 µF 400 V | SMPS bulk | ✅ |
| C513 | 22 µF | Watchdog timer 1 | ✅ |
| R114 | 15 Ω 5 W ("5W 15ΩJ 412") | Pre-charge | ✅ |
| R115 | 6.8 Ω, thermal fuse 139 °C ("A5MC 6.8ΩJ UMI") | Pre-charge with thermal fuse | ✅ |
| R600, R601 | 0.27 Ω ("0.27ΩG") | Motor current shunts (in parallel) | ✅ |
| R100, R107, R112 | 680 kΩ | Bleeders across CX101 | ✅ (measured) |
| R206 + one more | 47 kΩ ("473") | AND-gate pull-ups | ✅ |
| 3 resistors (EN network) | 47 kΩ each | Q205 base network | ✅ |
| R212 | 470 Ω ("471") | Q206 base–emitter | ✅ |
| R213 | 6.2 kΩ ("622") | Q205 → Q206 base | ✅ |
| R542, R706 | 47 kΩ | PERMIT pull-downs | ✅ |
| R562 | 30 kΩ ("303") ∥ speed-up C | Q507 base | ✅ |
| (Q511 base) | ~30 kΩ ∥ C | Q511 base | 🟡 |
| 2 resistors | 2.2 kΩ ("222") | Totem-pole pull-ups (JA7, JB5) | ✅ |
| 1–2 resistors | ~33 Ω | Discrete driver supply | 🟡 |
| 4 resistors | 470 Ω ("471") | IGBT gate (Q503, Q504, Q500, Q505) | ✅ |
| 2 resistors | 47 Ω ("470") | Fast turn-off path | ✅ |
| (Q500 G–E), R517 | ~10 kΩ | Gate pull-downs | ✅ / 🟡 |
| R714, R715 | 180 Ω ("181") | Triac gate | ✅ |
| R605 | 51 kΩ ("5102") | Motor current to ADC | ✅ |
| (IC611) | 68 kΩ ("6802") ∥ C, 300 Ω ("3000") | Heater CT amplifier | ✅ |
| (IC611) | 22 kΩ ("2202"), 180 kΩ ("1803") | Motor current gain network | 🟡 |
| (IC700) | 39 kΩ ("3902"), 150 kΩ ("1503") × 2 sets | Thresholds | ✅ |
| R702 | 47 kΩ | Latch network | ✅ |
| R708 | 1 MΩ | Latch network | ✅ |
| (IC700) | ~470 kΩ, 1.2 kΩ ("122") | Latch network | ✅ / 🟡 |
| (IC503 pin 7) | 1 MΩ ("105") | Timer 2 | ✅ |
| (CN502) | 20 kΩ ("203") × 2, ~1 kΩ | Sensor inputs | ✅ |
| (PC502 LED) | 1.5 kΩ | Cold side | ✅ |
| (Q506 base) | 470 Ω ("471"), 47 kΩ ("473") | Cold side | 🟡 |
| (MCU 33) | ~10 kΩ to +5 V (9.87 kΩ in-circuit) | Sense bias | 🟡 |

## Unknown values

R548 (timer 1, unmarked), C514 (timer 2, unmarked), R713 (PC700 LED), R510/R511/R572/R535, R110/R111,
R118–R121, R103–R105, ZD500 voltage, C200/C220/C230/C210 values, R211, Z100 type.
