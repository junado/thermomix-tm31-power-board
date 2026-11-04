#!/bin/sh
# Regenerate the wired schematic and prove its connections match the reference netlist.
#   tools/tm31.py   = reference netlist (rev 0.1, one global label per pin: the connection data)
#   tools/tm31w.py  = wired drawing (rev 0.2, what is published in hardware/)
# Needs python3 and kicad-cli (KiCad 7 or later). Run from the repository root.
set -e
TMP=$(mktemp -d)
python3 tools/tm31.py "$TMP/ref" >/dev/null
python3 tools/tm31w.py "$TMP/wired" >/dev/null
kicad-cli sch export netlist --format kicadsexpr -o "$TMP/ref.net" "$TMP/ref/TM31_power_board.kicad_sch" >/dev/null
kicad-cli sch export netlist --format kicadsexpr -o "$TMP/wired.net" "$TMP/wired/TM31_power_board.kicad_sch" >/dev/null
python3 tools/netcmp.py "$TMP/ref.net" "$TMP/wired.net"
rm -rf "$TMP"
