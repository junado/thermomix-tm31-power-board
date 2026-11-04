"""KiCad 7 schematic writer for hand-laid-out, wired schematics.

Parts are placed explicitly (with rotation and multi-unit support), connected by wires,
power symbols for supply rails, and global labels only for signals that leave the sheet.
Junction dots are added automatically wherever three or more connections meet.
"""
import math
import uuid

G = 2.54


def U():
    return str(uuid.uuid4())


def q(s):
    s = str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def r(v):
    return f"{round(v * 1000) / 1000:g}"


def snap(v):
    return round(v * 1000) / 1000


def font(size=1.27, hide=False, justify=None, bold=False, italic=False):
    f = f"(font (size {size} {size})" + (" bold" if bold else "") + (" italic" if italic else "") + ")"
    j = f" (justify {justify})" if justify else ""
    return f"(effects {f}{j}" + (" hide" if hide else "") + ")"


# ------------------------------------------------------------------ library symbols
class Sym:
    """units: list of (graphics, pins); pins are dicts num,name,x,y,ang,len,type,hide. Y-up coordinates."""

    def __init__(self, name, units, show_names=True, show_numbers=True, ref="U", power=False,
                 name_offset=0.762):
        self.name = name
        self.units = units
        self.show_names = show_names
        self.show_numbers = show_numbers
        self.ref = ref
        self.power = power
        self.name_offset = name_offset

    def pins(self, unit=None):
        out = []
        for i, (g, ps) in enumerate(self.units, 1):
            if unit is None or unit == i:
                out += ps
        return out

    def pin(self, key, unit):
        for p in self.pins(unit):
            if p["num"] == key:
                return p
        for p in self.pins(unit):
            if p["name"] == key:
                return p
        raise KeyError(f"{self.name} unit {unit}: no pin {key}")

    def sexpr(self, lib="tm31"):
        nm = self.name
        o = [f'(symbol "{lib}:{nm}"']
        if self.power:
            o.append("(power)")
        if not self.show_numbers:
            o.append("(pin_numbers hide)")
        o.append(f"(pin_names (offset {self.name_offset})" + ("" if self.show_names else " hide") + ")")
        o.append("(in_bom yes) (on_board yes)")
        o.append(f'(property "Reference" {q(self.ref)} (at 0 0 0) {font(hide=self.power)})')
        o.append(f'(property "Value" {q(nm)} (at 0 0 0) {font()})')
        o.append(f'(property "Footprint" "" (at 0 0 0) {font(hide=True)})')
        o.append(f'(property "Datasheet" "" (at 0 0 0) {font(hide=True)})')
        for i, (g, ps) in enumerate(self.units, 1):
            pins = []
            for p in ps:
                hide = " hide" if p.get("hide") else ""
                pins.append(f'(pin {p.get("type", "passive")} line (at {r(p["x"])} {r(p["y"])} {p["ang"]}) '
                            f'(length {r(p["len"])}){hide} (name {q(p["name"])} {font(1.0)}) '
                            f'(number {q(p["num"])} {font(1.0)}))')
            o.append(f'(symbol "{nm}_{i}_1" ' + " ".join(g + pins) + ")")
        o.append(")")
        return " ".join(o)


def stroke(w=0.254, typ="default"):
    return f"(stroke (width {w}) (type {typ}))"


def poly(pts, w=0.254, fill="none"):
    p = " ".join(f"(xy {r(x)} {r(y)})" for x, y in pts)
    return f"(polyline (pts {p}) {stroke(w)} (fill (type {fill})))"


def rect(x1, y1, x2, y2, w=0.254, fill="background"):
    return f"(rectangle (start {r(x1)} {r(y1)}) (end {r(x2)} {r(y2)}) {stroke(w)} (fill (type {fill})))"


def circ(cx, cy, rad, w=0.254, fill="none"):
    return f"(circle (center {r(cx)} {r(cy)}) (radius {r(rad)}) {stroke(w)} (fill (type {fill})))"


def arc(s, m, e, w=0.254):
    return (f"(arc (start {r(s[0])} {r(s[1])}) (mid {r(m[0])} {r(m[1])}) (end {r(e[0])} {r(e[1])}) "
            f"{stroke(w)} (fill (type none)))")


def stext(t, x, y, size=1.0):
    return f"(text {q(t)} (at {r(x)} {r(y)} 0) {font(size)})"


def P(num, name, x, y, ang, length=2.54, typ="passive", hide=False):
    return dict(num=str(num), name=name, x=x, y=y, ang=ang, len=length, type=typ, hide=hide)


def coil_arcs(x0, y, n=4, step=1.27, up=True):
    g = []
    s = 1 if up else -1
    for i in range(n):
        a = x0 + i * step
        g.append(arc((a, y), (a + step / 2, y + s * step / 2), (a + step, y)))
    return g


def two_pin(name, graphics, half=5.08, n1="1", n2="2", nm1="~", nm2="~", ref="R", plen=2.54):
    return Sym(name, [(graphics, [P(n1, nm1, -half, 0, 0, plen), P(n2, nm2, half, 0, 180, plen)])],
               show_names=False, show_numbers=False, ref=ref)


def make_lib():
    L = {}
    L["R"] = two_pin("R", [rect(-2.54, 0.889, 2.54, -0.889, fill="none")], half=3.81, plen=1.27)
    L["C"] = two_pin("C", [poly([(-0.508, 1.778), (-0.508, -1.778)], 0.4),
                           poly([(0.508, 1.778), (0.508, -1.778)], 0.4)], half=2.54, plen=2.032, ref="C")
    L["CP"] = two_pin("CP", [poly([(-0.508, 1.778), (-0.508, -1.778)], 0.4),
                             rect(0.508, 1.778, 1.016, -1.778, 0.254, fill="outline"),
                             stext("+", -1.4, 1.6, 1.0)], half=3.81, plen=2.794, ref="C",
                      nm1="+", nm2="-")
    dtri = poly([(-1.27, 1.27), (1.27, 0), (-1.27, -1.27), (-1.27, 1.27)], 0.254, "outline")
    L["D"] = Sym("D", [([dtri, poly([(1.27, 1.27), (1.27, -1.27)])],
                        [P("2", "A", -3.81, 0, 0), P("1", "K", 3.81, 0, 180)])],
                 show_names=False, show_numbers=False, ref="D")
    L["ZD"] = Sym("ZD", [([dtri, poly([(0.635, 1.27), (1.27, 1.27), (1.27, -1.27), (1.905, -1.27)])],
                          [P("2", "A", -3.81, 0, 0), P("1", "K", 3.81, 0, 180)])],
                  show_names=False, show_numbers=False, ref="ZD")
    L["FUSE"] = two_pin("FUSE", [rect(-2.54, 0.762, 2.54, -0.762, fill="none"),
                                 poly([(-2.54, 0), (2.54, 0)])], half=3.81, plen=1.27, ref="F")
    L["L"] = two_pin("L", coil_arcs(-2.54, 0), half=3.81, plen=1.27, ref="L")
    L["VAR"] = two_pin("VAR", [rect(-2.54, 0.889, 2.54, -0.889, fill="none"),
                               poly([(-2.0, -1.6), (1.4, 1.6), (2.2, 1.6)])], half=3.81, plen=1.27, ref="Z")
    L["NTC"] = two_pin("NTC", [rect(-2.54, 0.889, 2.54, -0.889, fill="none"),
                               poly([(-2.6, -1.8), (-1.6, -1.8), (2.0, 1.8)]), stext("-t", 1.6, -2.4, 0.9)],
                       half=3.81, plen=1.27, ref="RT")
    L["HEATER"] = two_pin("HEATER", [rect(-3.81, 1.27, 3.81, -1.27, fill="none"),
                                     poly([(-3.0, 0), (-2.0, 0.9), (-1.0, -0.9), (0, 0.9), (1.0, -0.9),
                                           (2.0, 0.9), (3.0, 0)])], half=6.35, ref="HTR")
    L["WINDING"] = two_pin("WINDING", coil_arcs(-3.81, 0, 6), half=6.35, ref="M")

    # transistors: B left, collector/drain up, emitter down (NPN). PNP: emitter UP, collector down.
    def bjt(name, pnp):
        g = [circ(0.635, 0, 3.048), poly([(-2.54, 0), (-0.635, 0)]),
             poly([(-0.635, 1.905), (-0.635, -1.905)], 0.4),
             poly([(-0.635, 0.762), (2.54, 2.54)]), poly([(-0.635, -0.762), (2.54, -2.54)])]
        if not pnp:  # arrow out of base on the emitter (bottom)
            g.append(poly([(2.286, -2.413), (1.651, -1.524), (1.27, -2.286), (2.286, -2.413)], 0.1, "outline"))
            pins = [P("1", "B", -5.08, 0, 0), P("3", "C", 2.54, 5.08, 270), P("2", "E", 2.54, -5.08, 90)]
        else:  # arrow into base on the emitter (top)
            g.append(poly([(0.0, 1.143), (0.889, 1.016), (0.508, 1.905), (0.0, 1.143)], 0.1, "outline"))
            pins = [P("1", "B", -5.08, 0, 0), P("2", "E", 2.54, 5.08, 270), P("3", "C", 2.54, -5.08, 90)]
        return Sym(name, [(g, pins)], show_names=False, show_numbers=False, ref="Q")

    L["NPN"] = bjt("NPN", False)
    L["PNP"] = bjt("PNP", True)
    L["IGBT"] = Sym("IGBT", [([circ(0.635, 0, 3.048), poly([(-2.54, 0), (-1.905, 0)]),
                               poly([(-1.905, 1.905), (-1.905, -1.905)], 0.3),
                               poly([(-1.016, 1.905), (-1.016, -1.905)], 0.4),
                               poly([(-1.016, 0.762), (2.54, 2.54)]), poly([(-1.016, -0.762), (2.54, -2.54)]),
                               poly([(2.286, -2.413), (1.651, -1.524), (1.27, -2.286), (2.286, -2.413)], 0.1,
                                    "outline")],
                              [P("1", "G", -5.08, 0, 0), P("2", "C", 2.54, 5.08, 270), P("3", "E", 2.54, -5.08, 90)])],
                    show_names=False, show_numbers=False, ref="Q")

    # single spade terminal, pin to the right
    L["SPADE"] = Sym("SPADE", [([circ(0, 0, 0.889, 0.3)], [P("1", "1", 2.54, 0, 180, 1.651)])],
                     show_names=False, show_numbers=False, ref="CN")
    # pass-through terminal: board side (left) and wire side (right) are the same pin number
    L["SPADE2"] = Sym("SPADE2", [([circ(0, 0, 0.889, 0.3)], [P("1", "1", 0, 0, 0, 0)])],
                      show_names=False, show_numbers=False, ref="CN")
    L["SPADE2"].no_junction = True

    # relays: unit 1 = contacts (COM left), unit 2 = coil (vertical, A1 top)
    coil = ([rect(-1.905, 2.54, 1.905, -2.54, fill="none"), poly([(-1.905, -2.54), (1.905, 2.54)])],
            [P("A1", "A1", 0, 5.08, 270), P("A2", "A2", 0, -5.08, 90)])
    L["RELAY_1A"] = Sym("RELAY_1A", [
        ([poly([(-2.54, 0), (2.032, 1.778)], 0.3), poly([(2.54, 0), (2.54, 0.762)], 0.3),
          circ(-2.54, 0, 0.3, 0.2, "outline"), stext("NO", 2.6, 2.2, 0.9)],
         [P("11", "COM", -5.08, 0, 0), P("14", "NO", 5.08, 0, 180)]), coil],
        show_names=False, show_numbers=True, ref="RY")
    L["RELAY_1C"] = Sym("RELAY_1C", [
        ([poly([(-2.54, 0), (2.286, -1.778)], 0.3), poly([(2.54, 2.54), (2.54, 1.016)], 0.3),
          poly([(2.54, -2.54), (2.54, -1.778)], 0.3), circ(-2.54, 0, 0.3, 0.2, "outline"),
          stext("NO", 3.3, 4.0, 0.9), stext("NC", 3.3, -4.0, 0.9)],
         [P("11", "COM", -5.08, 0, 0), P("14", "NO", 5.08, 2.54, 180), P("12", "NC", 5.08, -2.54, 180)]), coil],
        show_names=False, show_numbers=True, ref="RY")
    # current transformer: primary straight through, secondary pins at the bottom
    L["CT"] = Sym("CT", [([poly([(-5.08, 0), (5.08, 0)], 0.5), circ(0, 0, 2.032, 0.3),
                           poly([(-2.54, -5.08), (-2.54, -3.302)]), poly([(2.54, -5.08), (2.54, -3.302)])]
                          + coil_arcs(-2.54, -3.302, 4, 1.27, up=False) + [stext("P1", -5.6, 1.4), stext("P2", 5.6, 1.4)],
                          [P("1", "P1", -7.62, 0, 0, 2.54), P("2", "P2", 7.62, 0, 180, 2.54),
                           P("3", "S1", -2.54, -7.62, 90, 2.54), P("4", "S2", 2.54, -7.62, 90, 2.54)])],
                 show_names=False, show_numbers=False, ref="T")
    # common-mode choke: live winding on top, neutral winding below (20.32 mm apart)
    L["CHOKE"] = Sym("CHOKE", [(coil_arcs(-2.54, 10.16, 4) + coil_arcs(-2.54, -10.16, 4, up=False) +
                                [poly([(-2.54, 10.16), (-5.08, 10.16)]), poly([(2.54, 10.16), (5.08, 10.16)]),
                                 poly([(-2.54, -10.16), (-5.08, -10.16)]), poly([(2.54, -10.16), (5.08, -10.16)]),
                                 poly([(-2.54, 1.016), (2.54, 1.016)], 0.3), poly([(-2.54, -1.016), (2.54, -1.016)], 0.3),
                                 circ(-3.2, 11.6, 0.3, 0.2, "outline"), circ(-3.2, -8.7, 0.3, 0.2, "outline")],
                                [P("1", "L_IN", -7.62, 10.16, 0), P("2", "L_OUT", 7.62, 10.16, 180),
                                 P("3", "N_IN", -7.62, -10.16, 0), P("4", "N_OUT", 7.62, -10.16, 180)])],
                     show_names=False, show_numbers=False, ref="L")
    # triac, horizontal: A2 left, A1 right, gate bottom right
    L["TRIAC"] = Sym("TRIAC", [([poly([(-1.27, 2.54), (-1.27, -2.54)], 0.3), poly([(1.27, 2.54), (1.27, -2.54)], 0.3),
                                 poly([(-1.27, 2.286), (1.27, 1.143), (-1.27, 0), (-1.27, 2.286)], 0.2, "outline"),
                                 poly([(1.27, 0), (-1.27, -1.143), (1.27, -2.286), (1.27, 0)], 0.2, "outline"),
                                 poly([(1.27, -1.016), (2.54, -2.54)]),
                                 stext("A2", -3.3, 1.4, 0.9), stext("A1", 3.3, 1.4, 0.9), stext("G", 3.6, -3.4, 0.9)],
                                [P("2", "A2", -5.08, 0, 0, 3.81), P("1", "A1", 5.08, 0, 180, 3.81),
                                 P("3", "G", 2.54, -5.08, 90, 2.54)])],
                     show_names=False, show_numbers=False, ref="CR")

    # op-amp / comparator: units A and B as triangles, unit C = supply pins
    def oa_unit(inv, non, out):
        g = [poly([(-5.08, 5.08), (5.08, 0), (-5.08, -5.08), (-5.08, 5.08)], 0.254, "background"),
             stext("-", -4.0, 2.54, 1.5), stext("+", -4.0, -2.54, 1.5)]
        return (g, [P(inv, "-", -7.62, 2.54, 0), P(non, "+", -7.62, -2.54, 0), P(out, "~", 7.62, 0, 180)])

    pw = ([rect(-1.905, 2.54, 1.905, -2.54, fill="background")],
          [P("8", "V+", 0, 5.08, 270, 2.54, "power_in"), P("4", "V-", 0, -5.08, 90, 2.54, "power_in")])
    L["DUAL_OPAMP"] = Sym("DUAL_OPAMP", [oa_unit("2", "3", "1"), oa_unit("6", "5", "7"), pw],
                          show_names=False, show_numbers=True, ref="IC")
    return L


def box(name, left, right, width=None, ref="U", title=None, top=None, bottom=None):
    """IC-style box. left/right: (num, name) or None (gap); pins every 2.54 mm.
    top/bottom: optional (num, name) lists of vertical pins, 5.08 mm apart, centred."""
    n = max(len(left), len(right), 1)
    h = (n - 1) * G
    maxl = max([len(p[1]) for p in left if p] + [0])
    maxr = max([len(p[1]) for p in right if p] + [0])
    if width is None:
        width = max(10.16, (maxl + maxr) * 1.0 + 5.08, len(title or "") * 0.85 + 2.54,
                    (len(top or []) + 1) * 5.08, (len(bottom or []) + 1) * 5.08)
    width = math.ceil(width / 5.08 - 1e-6) * 5.08
    hw = width / 2
    ytop = h / 2 + 2.54 + (2.54 if title else 0)
    ybot = -h / 2 - 2.54
    if (ytop - h / 2) % 2.54:
        pass
    pins = []
    for i, p in enumerate(left):
        if p:
            pins.append(P(p[0], p[1], -hw - 2.54, h / 2 - i * G, 0))
    for i, p in enumerate(right):
        if p:
            pins.append(P(p[0], p[1], hw + 2.54, h / 2 - i * G, 180))
    for lst, y0, ang, yb in ((top, ytop, 270, 1), (bottom, ybot, 90, -1)):
        if lst:
            k = len(lst)
            for i, p in enumerate(lst):
                if p is None:
                    continue
                x = (i - (k - 1) / 2) * 5.08
                pins.append(P(p[0], p[1], x, y0 + yb * 2.54, ang))
    g = [rect(-hw, ytop, hw, ybot)]
    if title:
        g.append(stext(title, 0, h / 2 + 2.6, 1.0))
    s = Sym(name, [(g, pins)], show_names=True, show_numbers=True, ref=ref)
    s.body = (-hw, ybot, hw, ytop)
    return s


def power_sym(rail, style):
    """style: 'gnd' (triangle below), 'up' (arrow above), 'gndc' (hollow triangle, cold ground)."""
    if style in ("gnd", "gndc"):
        fill = "outline" if style == "gnd" else "none"
        g = [poly([(0, 0), (0, -1.27)]), poly([(-1.27, -1.27), (1.27, -1.27), (0, -2.54), (-1.27, -1.27)], 0.254, fill)]
        ang = 270
    else:
        g = [poly([(0, 0), (0, 2.54)]), poly([(-0.762, 1.27), (0, 2.54), (0.762, 1.27)])]
        ang = 90
    s = Sym(rail, [(g, [P("1", rail, 0, 0, ang, 0, "power_in", hide=True)])], show_names=False,
            show_numbers=False, ref="#PWR", power=True, name_offset=0)
    s.vtext = -4.0 if style in ("gnd", "gndc") else 3.8  # value text offset (Y-up)
    return s


def field_orient(rot, just):
    """KiCad shows a field at (field angle + symbol rotation); a sum of 180 is flipped for readability,
    mirroring the justification. Return (field angle, justification) that display horizontally as asked."""
    fa = 90 if rot in (90, 270) else 0
    if (fa + rot) % 360 == 180 and just:
        sw = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}
        just = " ".join(sw.get(w, w) for w in just.split())
    return fa, just


# ------------------------------------------------------------------ placed parts
class Part:
    def __init__(self, sym, ref, value, x, y, rot, unit, kw):
        self.sym, self.ref, self.value = sym, ref, value
        self.x, self.y, self.rot, self.unit, self.kw = snap(x), snap(y), rot % 360, unit, kw
        self.fields = []

    def xf(self, px, py):
        c = round(math.cos(math.radians(self.rot)))
        s = round(math.sin(math.radians(self.rot)))
        return snap(self.x + px * c - py * s), snap(self.y - (px * s + py * c))

    def p(self, key):
        pin = self.sym.pin(key, self.unit)
        return self.xf(pin["x"], pin["y"])

    def pin_points(self):
        return [(p["num"], self.xf(p["x"], p["y"])) for p in self.sym.pins(self.unit)]


class WSheet:
    pwr_count = [0]

    def __init__(self, project, title, fname, page, paper="A3", root_uuid=None, sheet_uuid=None):
        self.project, self.title, self.fname, self.page, self.paper = project, title, fname, page, paper
        self.uuid = U()
        self.root_uuid, self.sheet_uuid = root_uuid, sheet_uuid
        self.libs = {}
        self.parts = []
        self.wires = []
        self.labels = []  # (kind, name, x, y, ang, shape)
        self.ncs = []
        self.texts = []
        self.graphics = []
        self.extra_junctions = []

    # ---- placement
    def place(self, sym, ref, value, x, y, rot=0, unit=1, fields="auto", **kw):
        self.libs[sym.name] = sym
        p = Part(sym, ref, value, x, y, rot, unit, kw)
        p.fields = fields
        self.parts.append(p)
        return p

    def two(self, sym, ref, value, at, d="down", pin=None, **kw):
        """Place a 2-pin part so that `pin` (default: its left pin in the library) sits at `at`
        and the other pin lies in direction d ('up','down','left','right')."""
        pins = sym.pins(1)
        left = min(pins, key=lambda p: p["x"])
        right = max(pins, key=lambda p: p["x"])
        half = right["x"]
        if pin is None or pin in (left["num"], left["name"]):
            rot = {"right": 0, "up": 90, "left": 180, "down": 270}[d]
        else:
            rot = {"left": 0, "down": 90, "right": 180, "up": 270}[d]
        dx, dy = {"right": (1, 0), "left": (-1, 0), "up": (0, -1), "down": (0, 1)}[d]
        return self.place(sym, ref, value, at[0] + dx * half, at[1] + dy * half, rot, **kw)

    # ---- connections
    def w(self, *pts):
        pts = [(snap(a), snap(b)) for a, b in pts]
        for a, b in zip(pts, pts[1:]):
            if a == b:
                continue
            if a[0] != b[0] and a[1] != b[1]:
                raise ValueError(f"{self.fname}: diagonal wire {a} -> {b}")
            self.wires.append((a, b))

    def hv(self, a, b):
        """L-shaped wire: horizontal first, then vertical."""
        self.w(a, (b[0], a[1]), b)

    def vh(self, a, b):
        self.w(a, (a[0], b[1]), b)

    def pwr(self, pt, rail, rot=0, toward=None):
        """Power symbol at pt. toward: direction the symbol points ('up','down','left','right')."""
        self.pwr_count[0] += 1
        style = "gnd" if rail in ("GND", "HVDC_N") else "gndc" if rail == "GND_COLD" else "up"
        if toward:
            if style == "up":
                rot = {"up": 0, "left": 90, "down": 180, "right": 270}[toward]
            else:
                rot = {"down": 0, "right": 90, "up": 180, "left": 270}[toward]
        key = rail
        if key not in self.libs:
            self.libs[key] = power_sym(rail, style)
        p = self.place(self.libs[key], f"#PWR{self.pwr_count[0]:03d}", rail, pt[0], pt[1], rot, fields="power")
        return p

    def gl(self, pt, name, ang=0, shape="passive"):
        self.labels.append(("global_label", name, snap(pt[0]), snap(pt[1]), ang, shape))

    def lb(self, pt, name, ang=0):
        self.labels.append(("label", name, snap(pt[0]), snap(pt[1]), ang, None))

    def nc(self, pt):
        self.ncs.append((snap(pt[0]), snap(pt[1])))

    def text(self, t, x, y, size=1.27, bold=False, italic=False, justify="left top"):
        self.texts.append((t, x, y, size, bold, italic, justify))

    def frame(self, x1, y1, x2, y2, title=None, dash=True):
        pts = [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
        self.graphics.append((pts, "dash" if dash else "solid", 0.15))
        if title:
            self.text(title, x1 + 1.27, y1 + 1.0, 1.4, bold=True)

    # ---- checks
    def _segments(self):
        return self.wires

    @staticmethod
    def _on_seg(pt, a, b, interior=True):
        (x, y), (x1, y1), (x2, y2) = pt, a, b
        if x1 == x2 == x and min(y1, y2) <= y <= max(y1, y2):
            return not interior or (y != y1 and y != y2)
        if y1 == y2 == y and min(x1, x2) <= x <= max(x1, x2):
            return not interior or (x != x1 and x != x2)
        return False

    def split_wires(self):
        """Split every wire at points where another wire ends, a pin sits or a label is anchored, so that
        all connections are endpoint-to-endpoint (KiCad does not join a wire end to the middle of a wire)."""
        pts = set()
        for a, b in self.wires:
            pts.add(a)
            pts.add(b)
        for part in self.parts:
            for _, pt in part.pin_points():
                pts.add(pt)
        for _, _, x, y, _, _ in self.labels:
            pts.add((x, y))
        out = []
        for a, b in self.wires:
            inner = [p for p in pts if self._on_seg(p, a, b)]
            if not inner:
                out.append((a, b))
                continue
            key = (lambda p: p[1]) if a[0] == b[0] else (lambda p: p[0])
            seq = sorted(inner + [a, b], key=key)
            out += [(u, v) for u, v in zip(seq, seq[1:]) if u != v]
        self.wires = out

    def junctions(self):
        pins = {}
        for part in self.parts:
            for num, pt in part.pin_points():
                pins.setdefault(pt, []).append(part.ref)
        cand = set()
        for a, b in self.wires:
            cand.add(a)
            cand.add(b)
        skip = {pt for part in self.parts if getattr(part.sym, "no_junction", False)
                for _, pt in part.pin_points()}
        out = []
        for pt in cand:
            if pt in skip:
                continue
            n = 0
            for a, b in self.wires:
                if pt == a or pt == b:
                    n += 1
                elif self._on_seg(pt, a, b):
                    n += 2
            n += len(pins.get(pt, []))
            if n >= 3:
                out.append(pt)
        return sorted(out)

    def check(self):
        """Warn about pins sitting in the middle of a wire (unintended connections) and
        dangling wire ends."""
        warn = []
        pinpts = {}
        for part in self.parts:
            for num, pt in part.pin_points():
                pinpts.setdefault(pt, []).append(f"{part.ref}.{num}")
        for pt, who in pinpts.items():
            for a, b in self.wires:
                if self._on_seg(pt, a, b):
                    warn.append(f"pin {who} on middle of wire {a}-{b}")
        ends = {}
        for a, b in self.wires:
            ends[a] = ends.get(a, 0) + 1
            ends[b] = ends.get(b, 0) + 1
        labpts = {(x, y) for _, _, x, y, _, _ in self.labels}
        for pt, n in ends.items():
            if n == 1 and pt not in pinpts and pt not in labpts and \
                    not any(self._on_seg(pt, a, b) for a, b in self.wires):
                warn.append(f"dangling wire end {pt}")
        for _, name, x, y, _, _ in self.labels:
            pt = (x, y)
            if pt not in pinpts and pt not in ends and not any(self._on_seg(pt, a, b, False) for a, b in self.wires):
                warn.append(f"label {name} at {pt} not connected")
        for w_ in warn:
            print(f"  [{self.fname}] {w_}")
        return warn

    # ---- output
    def _fields(self, part):
        """Return (ref_xy, ref_just, val_xy, val_just, note_xy)."""
        sym = part.sym
        X, Y = part.x, part.y
        f = part.fields
        if isinstance(f, dict):
            return f
        pins = sym.pins(part.unit)
        two = len(pins) == 2 and not hasattr(sym, "body") and sym.name not in ("SPADE2",)
        if f == "power":
            return None
        if sym.name.startswith("RELAY") and part.unit == 2:
            return dict(ref=(X - 2.8, Y - 0.4, "right bottom"), val=(X - 2.8, Y + 0.4, "right top"), just=None)
        if getattr(sym, "power_unit", None) == part.unit:
            return dict(ref=(X + 2.6, Y - 0.6, "left bottom"), val=(X + 2.6, Y + 0.6, "left top"), just=None)
        if hasattr(sym, "body"):  # box
            x1, y1, x2, y2 = sym.body
            corners = [part.xf(x1, y1), part.xf(x2, y2)]
            top = min(c[1] for c in corners)
            bot = max(c[1] for c in corners)
            return dict(ref=(X, top - 1.6, "bottom"), val=(X, bot + 1.6, "top"), just=None)
        if sym.name in ("NPN", "PNP", "IGBT"):
            if f == "left":
                return dict(ref=(X - 3.6, Y - 0.9, "right bottom"), val=(X - 3.6, Y + 0.9, "right top"), just=None)
            return dict(ref=(X + 4.4, Y - 0.6, "left bottom"), val=(X + 4.4, Y + 0.6, "left top"), just=None)
        if sym.name in ("SPADE", "SPADE2"):
            return dict(ref=(X, Y - 1.6, "bottom"), val=(X, Y + 1.6, "top"), just=None)
        horiz = part.rot in (0, 180)
        if sym.name in ("RELAY_1A", "RELAY_1C") and part.unit == 1:
            return dict(ref=(X, Y - 4.4, "bottom"), val=(X, Y + 4.0 if sym.name == "RELAY_1A" else Y + 5.2, "top"),
                        just=None)
        if sym.name == "DUAL_OPAMP":
            if part.unit == 3:
                return dict(ref=(X + 2.6, Y - 0.6, "left bottom"), val=(X + 2.6, Y + 0.6, "left top"), just=None)
            return dict(ref=(X + 1.0, Y - 5.0, "left bottom"), val=(X + 1.0, Y - 3.5, "left bottom"), just=None)
        if sym.name in ("CT", "CHOKE", "TRIAC"):
            dy = {"CT": 3.2, "CHOKE": 12.2, "TRIAC": 3.4}[sym.name]
            return dict(ref=(X, Y - dy, "bottom"), val=(X, Y + dy + (3.0 if sym.name == "CT" else 0), "top"),
                        just=None)
        if horiz:
            dy = 1.8 if sym.name not in ("HEATER",) else 2.2
            if f == "below":
                return dict(ref=(X, Y + dy, "top"), val=(X, Y + dy + 1.8, "top"), just=None)
            if f == "above":
                return dict(ref=(X, Y - dy - 1.8, "bottom"), val=(X, Y - dy, "bottom"), just=None)
            return dict(ref=(X, Y - dy, "bottom"), val=(X, Y + dy, "top"), just=None)
        dx = 2.0 if sym.name not in ("HEATER", "WINDING") else 2.6
        if f == "left":
            return dict(ref=(X - dx, Y - 0.4, "right bottom"), val=(X - dx, Y + 0.4, "right top"), just=None)
        return dict(ref=(X + dx, Y - 0.4, "left bottom"), val=(X + dx, Y + 0.4, "left top"), just=None)

    def emit(self, date="2026-11-03", rev="0.2"):
        o = ["(kicad_sch (version 20230121) (generator eeschema)", f"(uuid {self.uuid})", f'(paper "{self.paper}")',
             f'(title_block (title {q(self.title)}) (date "{date}") (rev "{rev}") '
             f'(company "Thermomix TM31-4C (120 V) power board NPVTM31LTA-3")'
             f' (comment 1 "Traced from a working board by continuity tests; see notes for confidence levels"))']
        o.append("(lib_symbols " + " ".join(s.sexpr() for s in self.libs.values()) + ")")
        self.split_wires()
        path = f"/{self.root_uuid}" + (f"/{self.sheet_uuid}" if self.sheet_uuid else "")
        for pt in self.junctions() + self.extra_junctions:
            o.append(f"(junction (at {r(pt[0])} {r(pt[1])}) (diameter 0) (color 0 0 0 0) (uuid {U()}))")
        for x, y in self.ncs:
            o.append(f"(no_connect (at {r(x)} {r(y)}) (uuid {U()}))")
        for a, b in self.wires:
            o.append(f"(wire (pts (xy {r(a[0])} {r(a[1])}) (xy {r(b[0])} {r(b[1])})) "
                     f"(stroke (width 0) (type default)) (uuid {U()}))")
        for kind, name, x, y, ang, shape in self.labels:
            just = {0: "left", 180: "right", 90: "left", 270: "right"}[ang]
            if kind == "global_label":
                o.append(f'(global_label {q(name)} (shape {shape}) (at {r(x)} {r(y)} {ang}) (fields_autoplaced) '
                         f'{font(1.27, justify=just)} (uuid {U()}) '
                         f'(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {r(x)} {r(y)} 0) {font(hide=True)}))')
            else:
                o.append(f'(label {q(name)} (at {r(x)} {r(y)} {ang}) (fields_autoplaced) '
                         f'{font(1.27, justify=just + " bottom")} (uuid {U()}))')
        for part in self.parts:
            sym = part.sym
            X, Y = part.x, part.y
            fl = self._fields(part)
            if fl is None:  # power symbol
                fa, _ = field_orient(part.rot, None)
                if part.rot in (90, 270):
                    vx, vy = part.xf(0, 3.3 if sym.vtext > 0 else -3.3)
                    vj = "left" if vx > X else "right"
                    _, vj = field_orient(part.rot, vj)
                else:
                    vx, vy = part.xf(0, sym.vtext)
                    vj = None
                fields = [f'(property "Reference" {q(part.ref)} (at {r(X)} {r(Y)} {fa}) {font(hide=True)})',
                          f'(property "Value" {q(part.value)} (at {r(vx)} {r(vy)} {fa}) {font(1.27, justify=vj)})']
            else:
                (rx, ry, rj), (vx, vy, vj) = fl["ref"], fl["val"]
                fa, rj2 = field_orient(part.rot, rj)
                _, vj2 = field_orient(part.rot, vj)
                fields = [f'(property "Reference" {q(part.ref)} (at {r(rx)} {r(ry)} {fa}) {font(1.27, justify=rj2)})',
                          f'(property "Value" {q(part.value)} (at {r(vx)} {r(vy)} {fa}) {font(1.0, justify=vj2)})']
                if part.kw.get("note"):
                    if "top" in vj:
                        nx, ny, nj = vx, vy + 1.5, vj
                    else:
                        nx, ny, nj = rx, ry - 1.7, rj
                    _, nj2 = field_orient(part.rot, nj)
                    fields.append(f'(property "Note" {q(part.kw["note"])} (at {r(nx)} {r(ny)} {fa}) '
                                  f'{font(0.9, justify=nj2, italic=True)})')
            fields += [f'(property "Footprint" "" (at {r(X)} {r(Y)} 0) {font(hide=True)})',
                       f'(property "Datasheet" "" (at {r(X)} {r(Y)} 0) {font(hide=True)})']
            in_bom = "no" if part.kw.get("offboard") else "yes"
            dnp = "yes" if part.kw.get("dnp") else "no"
            seen = set()
            pl = []
            for p in sym.pins(part.unit):
                if p["num"] in seen:
                    continue
                seen.add(p["num"])
                pl.append(f'(pin {q(p["num"])} (uuid {U()}))')
            o.append(f'(symbol (lib_id "tm31:{sym.name}") (at {r(X)} {r(Y)} {part.rot}) (unit {part.unit}) '
                     f'(in_bom {in_bom}) (on_board {in_bom}) (dnp {dnp}) (uuid {U()}) ' + " ".join(fields) + " " +
                     " ".join(pl) + f' (instances (project {q(self.project)} (path {q(path)} (reference {q(part.ref)}) '
                     f'(unit {part.unit})))))')
        for pts, typ, wdt in self.graphics:
            p = " ".join(f"(xy {r(x)} {r(y)})" for x, y in pts)
            o.append(f"(polyline (pts {p}) (stroke (width {wdt}) (type {typ})) (uuid {U()}))")
        for t, x, y, size, bold, italic, just in self.texts:
            o.append(f"(text {q(t)} (at {r(x)} {r(y)} 0) {font(size, justify=just, bold=bold, italic=italic)} "
                     f"(uuid {U()}))")
        o.append(")")
        return "\n".join(o)


def root_sheet(project, title, root_uuid, children, notes, paper="A3", rev="0.2", date="2026-11-03"):
    o = ["(kicad_sch (version 20230121) (generator eeschema)", f"(uuid {root_uuid})", f'(paper "{paper}")',
         f'(title_block (title {q(title)}) (date "{date}") (rev "{rev}") '
         f'(company "Thermomix TM31-4C (120 V) power board NPVTM31LTA-3"))', "(lib_symbols)"]
    x0, y0 = 20.32, 25.4
    for i, ch in enumerate(children):
        col, row = i % 4, i // 4
        x = x0 + col * 96.52
        y = y0 + row * 33.02
        w, h = 81.28, 20.32
        o.append(f'(sheet (at {r(x)} {r(y)}) (size {r(w)} {r(h)}) (fields_autoplaced) '
                 f'(stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0000)) (uuid {ch.sheet_uuid}) '
                 f'(property "Sheetname" {q(ch.title)} (at {r(x)} {r(y - 0.7)} 0) '
                 f'(effects (font (size 1.27 1.27)) (justify left bottom))) '
                 f'(property "Sheetfile" {q(ch.fname)} (at {r(x)} {r(y + h + 0.6)} 0) '
                 f'(effects (font (size 1.27 1.27)) (justify left top))) '
                 f'(instances (project {q(project)} (path "/{root_uuid}" (page "{ch.page}")))))')
    for text, x, y, size in notes:
        o.append(f'(text {q(text)} (at {r(x)} {r(y)} 0) (effects (font (size {size} {size})) '
                 f'(justify left top)) (uuid {U()}))')
    o.append('(sheet_instances (path "/" (page "1")))')
    o.append(")")
    return "\n".join(o)
