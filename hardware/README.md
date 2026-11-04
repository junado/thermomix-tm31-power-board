# Hardware: reverse-engineered schematic (rev 0.1)

- [`TM31_power_board_schematic.pdf`](TM31_power_board_schematic.pdf): 8 pages, printable.
- [`kicad/`](kicad): KiCad project. Open `TM31_power_board.kicad_pro`. Written in KiCad 7 format; KiCad 8–10 open it
  and offer to upgrade the files on first save.

## Sheets

| Page | File | Contents |
|---|---|---|
| 1 | `TM31_power_board.kicad_sch` | Overview, how to read, architecture summary, known failures, key nets |
| 2 | `mains_heater.kicad_sch` | Mains input, EMI filter, RY200/RY202, T700, heater, triac + opto-triac |
| 3 | `motor_bus.kicad_sch` | Voltage doubler, F100, pre-charge R115/R114, RY201, pre-charge sense |
| 4 | `motor_stage.kicad_sch` | CN501 + windings, 6 IGBTs, freewheel diodes, IR2106s, discrete drivers, overcurrent cut-off |
| 5 | `safety_logic.kicad_sch` | Relay drivers, diode-AND permits, VGATE enable, 74HC123 watchdog, IC700 fault latch |
| 6 | `analog_sense.kicad_sch` | IC611 (heater CT amp, motor current amp), IC610 trip comparator, CN502 sensor board |
| 7 | `mcu_links.kicad_sch` | µPD78F0034B pinout, CN503 programming header, CN300 front-panel link |
| 8 | `power_supply.kicad_sch` | Flyback supply and all rails (functional) |

## How to read it

- **Netlist style:** every pin connects through a short wire to a **global label**; identical labels are the same net
  on every sheet. Parts are grouped in titled functional blocks.
- **References** are the board's silkscreen references. `RXn`, `CXn`, `DXn` = part present on the board whose reference
  was not read.
- `not read` = marking or value unreadable. `approx` / **APPROXIMATE** in the sheet notes = inferred, not confirmed by
  continuity.
- Off-board items (bowl heater, motor windings, motor NTC) are drawn for clarity, excluded from the BOM.
- **GND = motor DC bus negative = MCU ground.**

## Checks done

- The project opens and plots with `kicad-cli` 7.0.11.
- Netlist export checked: no duplicate references. The only single-pin nets are expected: untraced MCU pins, untraced
  LM393 inputs and unused outputs.
- An ERC in KiCad will list the untraced MCU pins as unconnected. That is deliberate: they were not traced, so they are
  not marked "no connect".

## Regenerating

The schematic is generated from [`../tools/tm31.py`](../tools/tm31.py) (netlist data) and
[`../tools/kisch.py`](../tools/kisch.py) (KiCad writer):

```sh
python3 tools/tm31.py hardware/kicad
kicad-cli sch export pdf -o hardware/TM31_power_board_schematic.pdf hardware/kicad/TM31_power_board.kicad_sch
```

Editing in KiCad directly is fine too, but then the generator and the files diverge. Pick one.
