# 15 — Future work

## 1. Decode the front-panel ↔ power-board serial link (CN300)

Goal: capture and map the messages between the front panel and the power board (speed, temperature, status,
error flags), for diagnostics and possibly home-automation integration.

### Where to tap

**Only at CN300**, the isolated side. Never on the MCU's RxD/TxD pins (21/22) or anywhere else on the power board:
those are at mains potential.

| CN300 pin | Signal |
|---|---|
| 1 | GND_COLD (reference) |
| 2 | Panel → power board |
| 3 | VCOLD |
| 4 | Power board → panel |
| 5 | Panel enable (PC503; may be a steady level or a heartbeat; capture it too) |

### Pre-checks

1. Unplugged: ohms from CN300 pin 1 to the hot GND (CN503 pin 1) and to the CN100 tab → must be open (MΩ+).
2. Powered, meter only: DC volts between CN300 pins 1 and 3 → logic level (5 V expected).
3. Solder thin wires to CN300's pads with the machine unplugged rather than probing a live connector.
4. Keep the sniffer itself isolated: laptop on battery, or an ESP32 on a power bank logging over Wi-Fi.

### Tools

| Tool | Notes |
|---|---|
| ESP32 (preferred) | Two spare hardware UART receivers (both directions at once), hardware signal inversion, timestamps. **3.3 V only**: use a divider (e.g. 10 k / 20 k) if VCOLD is 5 V. RX pins and GND only; do not connect TX or power it from VCOLD |
| USB-TTL adapter | One RX per adapter (two needed); most cannot invert (FTDI can) |
| 8-channel logic analyzer + PulseView | Fastest way to find baud rate, polarity, parity and framing before writing code |

Expect ≤ 9600 baud (LTV-816 optocouplers are slow). The signal may be inverted by the opto/Q506 stage.

### Decoding plan

1. Capture idle traffic and find the packet structure (start byte, length/command, data, checksum).
2. Change one thing at a time with timestamps: speed, temperature, timer, start/stop, lid, scale.
3. Diff packets and look for the checksum (often an XOR or sum).
4. Map the power board's replies (motor speed, status, fault flags → error codes).

> [!CAUTION]
> Reading is low-risk. **Sending** commands to the power board makes your code part of the safety chain: the front
> panel checks the lid and the bowl temperature, and the power board needs the panel's enable to keep its watchdog
> armed. Any custom controller must reproduce those checks before it heats or spins anything.

## 2. Finish the schematic

See the "Unknown" table in [13-unknowns-and-hypotheses.md](13-unknowns-and-hypotheses.md). Highest value:
IC700's inputs (what exactly trips the permits), IC611 output A's destination, watchdog time-outs, supply details.

## 3. Other boards

Photos and traces of a 230 V power board and a pre-2012 board would show what differs (front end, F100 rating,
MIP2E1D vs MIP2E3D, doubler jumpers). The front control panel is completely undocumented.
