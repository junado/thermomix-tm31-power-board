# Tools

Python 3 scripts used to produce the schematic and annotated images. They need Pillow (`pip install pillow`) and the
DejaVu fonts (`fonts-dejavu-core` on Debian/Ubuntu).

| Script | Produces | Usage (from the repository root) |
|---|---|---|
| `kisch.py` | Library: minimal KiCad 7 schematic writer (embedded symbols, auto layout, global labels) | imported by `tm31.py` |
| `tm31.py` | The whole KiCad project from the traced netlist | `python3 tools/tm31.py hardware/kicad` |
| `annotate_component_side.py` | `images/annotated/component-side-block-map.jpg` | `python3 tools/annotate_component_side.py photos/03-component-side/component-side-full.jpg images/annotated/component-side-block-map.jpg` |
| `annotate_quadrants.py` | Solder-side quadrant A, B, C maps | `python3 tools/annotate_quadrants.py photos/04-solder-side images/annotated` |
| `annotate_quadrant_D.py` | Solder-side quadrant D map | `python3 tools/annotate_quadrant_D.py photos/04-solder-side/quadrant-D-heater-and-power.jpg images/annotated/solder-side-quadrant-D-heater-and-power.jpg` |

Box coordinates in the annotation scripts are in pixels of a 1200 × 1600 preview; the scripts resize the photo
to that size first.

The netlist in `tm31.py` is the single source of truth for the schematic. To correct a connection, edit the
corresponding `s.add(...)`, `r2(...)`, `dio(...)` line and regenerate.
