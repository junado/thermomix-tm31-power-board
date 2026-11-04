# Tools

Python 3 scripts used to produce the schematic and annotated images. The image scripts need Pillow
(`pip install pillow`) and the DejaVu fonts (`fonts-dejavu-core` on Debian/Ubuntu). The schematic check needs
`kicad-cli` (KiCad 7 or later).

| Script | Produces | Usage (from the repository root) |
|---|---|---|
| `tm31w.py` | The published, wired KiCad project (rev 0.2) | `python3 tools/tm31w.py hardware/kicad` |
| `kisch2.py` | Library: KiCad 7 writer for wired schematics (rotation, multi-unit symbols, power symbols, wires, automatic junctions) | imported by `tm31w.py` |
| `tm31.py` | Reference netlist drawing (rev 0.1: every pin on a global label). The connection data in plain form | `python3 tools/tm31.py /tmp/ref` |
| `kisch.py` | Library: label-per-pin KiCad writer with auto layout | imported by `tm31.py` |
| `netcmp.py` | Compares two KiCad netlists node by node | `python3 tools/netcmp.py a.net b.net` |
| `check_schematic.sh` | Regenerates both projects, exports their netlists and compares them | `tools/check_schematic.sh` (prints `PASS`) |
| `build_site.sh` | The documentation website in `./site` (see `website/README.md`) | `tools/build_site.sh` |
| `annotate_component_side.py` | `images/annotated/component-side-block-map.jpg` | `python3 tools/annotate_component_side.py photos/03-component-side/component-side-full.jpg images/annotated/component-side-block-map.jpg` |
| `annotate_quadrants.py` | Solder-side quadrant A, B, C maps | `python3 tools/annotate_quadrants.py photos/04-solder-side images/annotated` |
| `annotate_quadrant_D.py` | Solder-side quadrant D map | `python3 tools/annotate_quadrant_D.py photos/04-solder-side/quadrant-D-heater-and-power.jpg images/annotated/solder-side-quadrant-D-heater-and-power.jpg` |

Box coordinates in the annotation scripts are in pixels of a 1200 × 1600 preview; the scripts resize the photo
to that size first.

`tm31.py` holds the traced connections in their simplest form (one `s.add(...)` / `r2(...)` / `dio(...)` line per part).
`tm31w.py` draws the same parts with coordinates and wires. To correct a connection, edit both and run
`tools/check_schematic.sh`: it fails if the drawing no longer matches the data.
