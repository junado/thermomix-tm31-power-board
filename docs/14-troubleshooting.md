# 14 — Troubleshooting guide (TM31 power board)

Based on this board (120 V, NPVTM31LTA-3), the Vorwerk service procedure and forum reports. Read the safety notes
in the [README](../README.md) first.

## Safe measurement practice

1. Unplug, wait, then **discharge C108/C109** (~340 V) and check with a meter.
2. Do continuity and diode tests **unpowered**.
3. For powered tests, **attach clip leads while unplugged**, then power up and read. Use a **floating DMM** only.
4. Reference for the hot-side logic: **CN503 pin 1 or C220 −** (= GND = motor bus negative). Not neutral, not earth.
5. Never connect a USB device, an earthed scope or a laptop on its charger to the hot side. Only CN300 is isolated.

## First, rule out the user-side causes

- **No heat:** the TM31 only heats with a **time set and the blade turning** (speed ≥ 1 or soft-stir).
- Clean the bowl contacts and the contact module; error 52 is often liquid on the contacts or NTC.
- Bowl check: 120 V bowl heater ~12.8 Ω, NTC ~130 kΩ at room temperature (230 V bowl: heater ~53 Ω).
- Never use a bowl from the other voltage version.

## Symptom → checks

### No heat, no error code
1. Bowl heater resistance and contacts.
2. **Triac CR700 legs**: continuity from each leg *at the component body* to its pad (the C-bend can crack).
3. Triac out of circuit: gate–A1 ~10–100 Ω; A1–A2 open.
4. Powered, heat requested (time set, motor turning), AC volts:
   - Across triac A1–A2: ~120 V means the triac is not firing (check PC700, R714/R715, the gate leg); ~1 V means it
     conducts.
   - From CN703 to CN101: ~120 V means live reaches the heater (RY200, T700 OK).
   - From NODE_X (triac A2) to CN100: ~120 V means RY202 closed.
5. DC across PC700 pins 1–2 while heating: ~1.1–1.3 V means the MCU is commanding heat.
6. Relay coils (DC across D224 / D223): ~12 V means energised.

### Heats continuously, error 69
- Shorted triac (classic on 230 V boards): A1–A2 reads low ohms. Replace with the same type (BTA, insulated tab).
- Bowl NTC shorted or open (error 69 also appears when the bowl reaches ~165 °C).

### Motor does not turn (error 34) or rough rotation
- Liquid in the motor or on the sensor board (CN502).
- Motor sensor board: CN502 pin 1 NTC ~12.5 kΩ at room temperature; position signals on pins 2/3.
- **F100** (T6.3 A) and **R115** (pre-charge resistor with thermal fuse): either open = no motor bus.
- Windings: 8.5 Ω on each of CN501 1–3, 1–5, 2–4, 2–6.
- IGBTs Q500–Q505 and diodes D500/D504–D508: no shorts.

### Errors 38 / 39 (motor drive)
- IGBTs, IR2106 (IC501/IC502), CN501 and the motor cable.
- VGATE present (IR2106 pin 1 vs GND) when the machine is idle with relays closed.

### Relays never click
- V12RAW (C200), +5 V (C220).
- MCU running: pulses on MCU pin 52 (watchdog), front panel connected (PC503 enable).
- IC700 outputs high (permits). After a fault latch, unplug for a while to reset.

### Error 72 (power relay)
- Pre-charge sense chain: RY201 NC contact, D107, R110, R111, JD1 → MCU 33.
- RY200/RY202 contacts (do they actually close?).
- RY201 coil (390 Ω) and its driver Q202.

### Completely dead / boot loop / flickering display
- F101 (T1 A), IC100 MIP2E3D, C110, bridge D100–D103.
- Liquid ingress on the power board (forum: overflow → dead board).

### Breaker trips
- Bowl outer pin broken (service guide), mains cord, CX102, DB100, C108/C109, IGBTs.

## Vorwerk error codes (TM31, from Vorwerk support and the service procedure)

| Code | Area | Notes |
|---|---|---|
| 22 | Power supply | Repair only if it keeps reappearing |
| 23 | Mixing bowl (heating) | At start-up: power board; while turning the knob: motor; during heating: bowl or power board |
| 34 | Motor does not turn | Liquid in the motor, tachometer (sensor) board, power board not delivering current |
| 38 | Motor drive | Power board splashed, motor cable, connector |
| 39 | Motor drive (forum) | Not related to the heater triac |
| 52 | Bowl contacts | Clean contacts; check contact module, leaking blade, NTC |
| 53 | Mixing bowl (heating) | Clean contacts and refit the bowl |
| 55, 67 | Scales | Load cells / control board |
| 58 | Power ↔ control board cable | Cable, splashes on either board |
| 61 | Board mismatch | Control/power board revisions incompatible (32008 + 30915, or 30466 + 30468) |
| 69 | Heating | Bowl NTC; power board heating constantly (shorted triac) |
| 70 | Blue cable | Control ↔ power board cable; else control board |
| 71, 72 | Hardware | 72: power relay (forum) |
