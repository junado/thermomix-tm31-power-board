# Hardware: reverse-engineered schematic (rev 0.2)

- [`TM31_power_board_schematic.pdf`](TM31_power_board_schematic.pdf): 8 pages, printable.
- [`kicad/`](kicad): KiCad project. Open `TM31_power_board.kicad_pro`. Written in KiCad 7 format; KiCad 8–10 open it
  and offer to upgrade the files on first save.
- [`TM31_power_board.net`](TM31_power_board.net): the netlist exported from the project (KiCad S-expression format),
  for anyone who wants the connections without opening KiCad.

## Sheets

| Page | File | Contents |
|---|---|---|
| 1 | `TM31_power_board.kicad_sch` | Overview, how to read, architecture summary, known failures, key nets |
| 2 | `mains_heater.kicad_sch` | Mains input, EMI filter, RY200/RY202 contacts, T700, heater, triac + opto-triac |
| 3 | `motor_bus.kicad_sch` | Voltage doubler, F100, pre-charge R115/R114, RY201 contacts, pre-charge sense |
| 4 | `motor_stage.kicad_sch` | Asymmetric bridge (6 IGBTs, freewheel diodes, windings), shunts, IR2106s, discrete drivers, overcurrent cut-off |
| 5 | `safety_logic.kicad_sch` | Diode-AND permits, relay coils and drivers, VGATE enable, 74HC123 watchdog, IC700 fault latch |
| 6 | `analog_sense.kicad_sch` | IC611 (heater CT amp, motor current amp), IC610 trip comparator, CN502 sensor board and its supply |
| 7 | `mcu_links.kicad_sch` | µPD78F0034B pinout, CN503 programming header, CN300 opto-isolated front-panel link |
| 8 | `power_supply.kicad_sch` | Flyback supply and all rails (transformer drawn functionally) |

## How to read it

- **Drawn as circuits.** Parts are wired together the way you would draw them to lay out a PCB. Supply rails use
  **power symbols** (GND, +5V, V12RAW, VGATE, VNEG, VBUS, HVDC/HVDC_N, VCOLD/GND_COLD). Only signals that leave a
  sheet use **global labels** (flag shape). A few busy nodes inside a sheet use **local net labels** (plain text on a
  wire): the same name on the same sheet is the same net.
- **Multi-unit parts.** Each relay has a contacts unit (A), drawn where it switches power, and a coil unit (B), drawn
  next to its driver on the safety sheet. The TLC277/LM393 dual op-amps are split into halves A and B plus a supply
  unit C; the 74HC123 into timers A and B plus a supply unit C.
- **References** are the board's silkscreen references. `RXn`, `CXn`, `DXn` = part present on the board whose reference
  was not read.
- `?` = value not read. `approx` / **APPROXIMATE** in the sheet notes = inferred, not confirmed by continuity.
- Off-board items (bowl heater, motor windings, motor NTC) are drawn in dashed frames and excluded from the BOM.
- **GND = motor DC bus negative = MCU ground.** Not neutral, not earth.

## Checks done

- The project opens and plots with `kicad-cli` 7.0.11.
- **Connections proven unchanged from rev 0.1.** Rev 0.1 was a label-per-pin "netlist" drawing; rev 0.2 redraws it as
  wired circuits. Both projects were exported to netlists and compared node by node: same 195 components, same 186
  nets (`tools/check_schematic.sh`, prints `PASS`).
- An ERC in KiCad will list the untraced MCU pins and the untraced LM393 inputs as unconnected. That is deliberate:
  they were not traced, so they are not marked "no connect".

## Regenerating

The connection data lives in [`../tools/tm31.py`](../tools/tm31.py) (reference netlist); the drawing in
[`../tools/tm31w.py`](../tools/tm31w.py) (wired layout, using [`../tools/kisch2.py`](../tools/kisch2.py)).

```sh
python3 tools/tm31w.py hardware/kicad
kicad-cli sch export pdf -o hardware/TM31_power_board_schematic.pdf hardware/kicad/TM31_power_board.kicad_sch
tools/check_schematic.sh        # must print PASS
```

To correct a connection, change it in **both** `tm31.py` and `tm31w.py` and run the check. Editing in KiCad directly
is fine too, but then the generators and the files diverge. Pick one.
