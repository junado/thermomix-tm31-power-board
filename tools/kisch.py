"""Minimal KiCad 7 schematic writer: embedded symbols, auto-placed parts,
every pin connected by a short wire stub + global label (netlist style)."""
import uuid

G = 2.54  # grid


def U():
    return str(uuid.uuid4())


def q(s):
    s = str(s).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def r(v):
    return f"{round(v * 100) / 100:g}"


FONT = "(effects (font (size 1.27 1.27)))"
FONT_HIDE = "(effects (font (size 1.27 1.27)) hide)"


class Sym:
    """Library symbol. pins: list of dict(num,name,x,y,ang,len,type). Symbol coords are Y-up."""

    def __init__(self, name, graphics, pins, show_names=True, show_numbers=True,
                 ref="U", body=(0, 0, 0, 0)):
        self.name = name
        self.graphics = graphics
        self.pins = pins
        self.show_names = show_names
        self.show_numbers = show_numbers
        self.ref = ref
        self.body = body  # (xmin, ymin, xmax, ymax) symbol coords, for text placement
        self.by_name = {}
        for p in pins:
            self.by_name.setdefault(p["name"], p["num"])

    def pin(self, key):
        for p in self.pins:
            if p["num"] == key:
                return p
        if key in self.by_name:
            return self.pin(self.by_name[key])
        raise KeyError(f"{self.name}: no pin {key}")

    def sexpr(self, lib="tm31"):
        nm = self.name
        out = [f'(symbol "{lib}:{nm}"']
        if not self.show_numbers:
            out.append("(pin_numbers hide)")
        out.append("(pin_names (offset 0.762)" + ("" if self.show_names else " hide") + ")")
        out.append("(in_bom yes) (on_board yes)")
        out.append(f'(property "Reference" {q(self.ref)} (at 0 0 0) {FONT})')
        out.append(f'(property "Value" {q(nm)} (at 0 0 0) {FONT})')
        out.append(f'(property "Footprint" "" (at 0 0 0) {FONT_HIDE})')
        out.append(f'(property "Datasheet" "" (at 0 0 0) {FONT_HIDE})')
        out.append(f'(symbol "{nm}_0_1" ' + " ".join(self.graphics) + ")")
        pins = []
        for p in self.pins:
            pins.append(
                f'(pin {p.get("type", "passive")} line (at {r(p["x"])} {r(p["y"])} {p["ang"]}) '
                f'(length {r(p["len"])}) (name {q(p["name"])} {FONT}) (number {q(p["num"])} {FONT}))')
        out.append(f'(symbol "{nm}_1_1" ' + " ".join(pins) + ")")
        out.append(")")
        return " ".join(out)


def stroke(w=0.254):
    return f"(stroke (width {w}) (type default))"


def poly(pts, w=0.254, fill="none"):
    p = " ".join(f"(xy {r(x)} {r(y)})" for x, y in pts)
    return f"(polyline (pts {p}) {stroke(w)} (fill (type {fill})))"


def rect(x1, y1, x2, y2, w=0.254, fill="background"):
    return f"(rectangle (start {r(x1)} {r(y1)}) (end {r(x2)} {r(y2)}) {stroke(w)} (fill (type {fill})))"


def circ(cx, cy, rad, w=0.254):
    return f"(circle (center {r(cx)} {r(cy)}) (radius {r(rad)}) {stroke(w)} (fill (type none)))"


def arc(s, m, e, w=0.254):
    return (f"(arc (start {r(s[0])} {r(s[1])}) (mid {r(m[0])} {r(m[1])}) (end {r(e[0])} {r(e[1])}) "
            f"{stroke(w)} (fill (type none)))")


def stext(t, x, y, size=1.27):
    return f"(text {q(t)} (at {r(x)} {r(y)} 0) (effects (font (size {size} {size}))))"


def P(num, name, x, y, ang, length=2.54, typ="passive"):
    return dict(num=str(num), name=name, x=x, y=y, ang=ang, len=length, type=typ)


# ---------------------------------------------------------------- symbol library
def two_pin(name, graphics, half=5.08, n1="1", n2="2", nm1="~", nm2="~", ref="R", plen=2.54):
    return Sym(name, graphics, [P(n1, nm1, -half, 0, 0, plen), P(n2, nm2, half, 0, 180, plen)],
               show_names=False, show_numbers=False, ref=ref, body=(-half + plen, -1.6, half - plen, 1.6))


def make_lib():
    L = {}
    L["R"] = two_pin("R", [rect(-2.54, 1.016, 2.54, -1.016, fill="none")], ref="R")
    L["C"] = two_pin("C", [poly([(-0.635, 1.905), (-0.635, -1.905)], 0.4),
                           poly([(0.635, 1.905), (0.635, -1.905)], 0.4)], half=3.81, plen=3.175, ref="C")
    L["CP"] = two_pin("CP", [poly([(-0.635, 1.905), (-0.635, -1.905)], 0.4),
                             arc((1.27, 1.905), (0.635, 0), (1.27, -1.905), 0.4),
                             stext("+", -1.6, 1.6)], half=3.81, plen=3.175, ref="C",
                      n1="1", n2="2", nm1="+", nm2="-")
    dtri = poly([(-1.27, 1.27), (1.27, 0), (-1.27, -1.27), (-1.27, 1.27)], 0.254, "outline")
    L["D"] = Sym("D", [dtri, poly([(1.27, 1.27), (1.27, -1.27)])],
                 [P("2", "A", -3.81, 0, 0), P("1", "K", 3.81, 0, 180)],
                 show_names=False, show_numbers=False, ref="D", body=(-1.3, -1.6, 1.3, 1.6))
    L["ZD"] = Sym("ZD", [dtri, poly([(0.635, 1.27), (1.27, 1.27), (1.27, -1.27), (1.905, -1.27)])],
                  [P("2", "A", -3.81, 0, 0), P("1", "K", 3.81, 0, 180)],
                  show_names=False, show_numbers=False, ref="ZD", body=(-1.3, -1.6, 1.3, 1.6))
    L["FUSE"] = two_pin("FUSE", [rect(-2.54, 0.762, 2.54, -0.762, fill="none"),
                                 poly([(-2.54, 0), (2.54, 0)])], ref="F")
    L["L"] = two_pin("L", [arc((-2.54, 0), (-1.905, 0.635), (-1.27, 0)),
                           arc((-1.27, 0), (-0.635, 0.635), (0, 0)),
                           arc((0, 0), (0.635, 0.635), (1.27, 0)),
                           arc((1.27, 0), (1.905, 0.635), (2.54, 0))], ref="L")
    L["VAR"] = two_pin("VAR", [rect(-2.54, 1.016, 2.54, -1.016, fill="none"),
                               poly([(-2.0, -1.6), (1.4, 1.6), (2.2, 1.6)])], ref="Z")
    L["HEATER"] = two_pin("HEATER", [rect(-2.54, 1.016, 2.54, -1.016, fill="none"),
                                     poly([(-2.0, 0), (-1.2, 0.8), (-0.4, -0.8), (0.4, 0.8), (1.2, -0.8), (2.0, 0)])],
                          ref="HTR")

    def bjt(name, pnp):
        g = [circ(0.635, 0, 3.175), poly([(-2.54, 0), (-0.635, 0)]),
             poly([(-0.635, 1.905), (-0.635, -1.905)], 0.4),
             poly([(-0.635, 0.762), (2.54, 2.54)]), poly([(-0.635, -0.762), (2.54, -2.54)])]
        if not pnp:
            g.append(poly([(2.0, -2.24), (1.435, -1.41), (0.995, -2.19), (2.0, -2.24)], 0.1, "outline"))
        else:
            g.append(poly([(0.476, -1.384), (1.481, -1.433), (1.041, -2.215), (0.476, -1.384)], 0.1, "outline"))
        return Sym(name, g, [P("1", "B", -5.08, 0, 0), P("3", "C", 5.08, 2.54, 180),
                             P("2", "E", 5.08, -2.54, 180)],
                   show_names=False, show_numbers=False, ref="Q", body=(-2.6, -3.3, 2.6, 3.3))

    L["NPN"] = bjt("NPN", False)
    L["PNP"] = bjt("PNP", True)
    L["IGBT"] = Sym("IGBT", [circ(0.635, 0, 3.175), poly([(-2.54, 0), (-1.905, 0)]),
                             poly([(-1.905, 1.905), (-1.905, -1.905)], 0.3),
                             poly([(-1.016, 1.905), (-1.016, -1.905)], 0.4),
                             poly([(-1.016, 0.762), (2.54, 2.54)]), poly([(-1.016, -0.762), (2.54, -2.54)]),
                             poly([(2.0, -2.24), (1.435, -1.41), (0.995, -2.19), (2.0, -2.24)], 0.1, "outline")],
                    [P("1", "G", -5.08, 0, 0), P("2", "C", 5.08, 2.54, 180), P("3", "E", 5.08, -2.54, 180)],
                    show_names=False, show_numbers=False, ref="Q", body=(-2.6, -3.3, 2.6, 3.3))
    return L


def box(name, left, right, width=None, ref="U", title=None):
    """left/right: list of (num, name) or None for a gap. Pins spaced 2.54."""
    n = max(len(left), len(right), 1)
    h = (n - 1) * G
    maxl = max([len(p[1]) for p in left if p] + [0])
    maxr = max([len(p[1]) for p in right if p] + [0])
    if width is None:
        width = max(10.16, (maxl + maxr) * 1.0 + 5.08, len(title or "") * 0.85 + 2.54)
        width = round(width / G + 0.49) * G
    hw = width / 2
    top = h / 2 + 1.27 + (2.54 if title else 0)
    bot = -h / 2 - 1.27
    pins = []
    for i, p in enumerate(left):
        if p:
            pins.append(P(p[0], p[1], -hw - 2.54, h / 2 - i * G, 0))
    for i, p in enumerate(right):
        if p:
            pins.append(P(p[0], p[1], hw + 2.54, h / 2 - i * G, 180))
    g = [rect(-hw, top, hw, bot)]
    if title:
        g.append(stext(title, 0, h / 2 + 1.9, 1.0))
    return Sym(name, g, pins, show_names=True, show_numbers=True, ref=ref, body=(-hw, bot, hw, top))


# ---------------------------------------------------------------- schematic
class Sheet:
    def __init__(self, project, title, fname, page, paper="A3", root_uuid=None, sheet_uuid=None):
        self.project = project
        self.title = title
        self.fname = fname
        self.page = page
        self.paper = paper
        self.uuid = U()
        self.root_uuid = root_uuid
        self.sheet_uuid = sheet_uuid  # uuid of sheet symbol in root
        self.libs = {}
        self.items = []
        self.notes = []
        self.parts = []  # (sym, ref, value, pins{key: net}, extra)

    cur_group = None

    def group(self, title):
        self.cur_group = title

    def add(self, sym, ref, value, pins, **kw):
        self.libs[sym.name] = sym
        kw["_group"] = self.cur_group
        self.parts.append((sym, ref, value, pins, kw))

    def note(self, text, x=None, y=None, size=1.27):
        self.notes.append((text, x, y, size))

    # ---- layout
    @staticmethod
    def label_w(name):
        return len(name) * 1.05 + 3.5

    def extents(self, sym, pins):
        lw = rw = 0
        for key, net in pins.items():
            p = sym.pin(key)
            w = 2.54 + (self.label_w(net) if net and net != "NC" else 1)
            if p["ang"] == 0:
                lw = max(lw, w + 0)
            else:
                rw = max(rw, w)
        xs = [p["x"] for p in sym.pins]
        left = -min(xs) + lw
        right = max(xs) + rw
        b = sym.body
        ys = [p["y"] for p in sym.pins] + [b[1], b[3]]
        top = max(ys) + 3.0
        bottom = -min(ys) + 3.0
        return left, right, top, bottom

    PAPERS = [("A4", 297, 210), ("A3", 420, 297), ("A2", 594, 420)]

    def _layout(self, W, H, x0=15.24, colgap=10.16):
        """Column-major layout of titled groups. Returns (placed, headers, fits)."""
        ymax = H - 42  # keep clear of the title block
        y0 = self.y_start
        groups = []
        for part in self.parts:
            g = part[4]["_group"]
            if not groups or groups[-1][0] != g:
                groups.append((g, []))
            groups[-1][1].append(part)
        x, y, colw = x0, y0, 0
        placed, headers = [], []
        for title, parts in groups:
            dims = [self.extents(p[0], p[3]) for p in parts]
            gh = sum(d[2] + d[3] + 2.54 for d in dims) + (6 if title else 0)
            if y + min(gh, ymax - y0) > ymax and y > y0:  # start group in a new column
                x += colw + colgap
                y, colw = y0, 0
            if title:
                headers.append((title, x, y))
                y += 6
            for part, (l, rgt, t, b) in zip(parts, dims):
                if y + t + b > ymax and y > y0 + 6:
                    x += colw + colgap
                    y, colw = y0, 0
                ox = round((x + l) / 1.27) * 1.27
                oy = round((y + t) / 1.27) * 1.27
                placed.append(part + (ox, oy, t, b))
                y += t + b + 2.54
                colw = max(colw, l + rgt, len(title or "") * 1.45 + 2)
            y += 5.08
        fits = x + colw <= W - 12
        return placed, headers, fits

    def place_all(self):
        longest = max((len(line) for t, *_ in self.notes for line in t.split("\n")), default=0)
        for name, W, H in self.PAPERS:
            if longest * 1.08 + 30 > W:
                continue
            placed, headers, fits = self._layout(W, H)
            if fits:
                break
        else:
            print(f"WARNING {self.fname}: does not fit A2")
        self.paper = name
        self.placed, self.headers = placed, headers

    # ---- output
    def emit(self):
        o = []
        o.append(f"(kicad_sch (version 20230121) (generator eeschema)")
        o.append(f"(uuid {self.uuid})")
        o.append(f'(paper "{self.paper}")')
        o.append(f'(title_block (title {q(self.title)}) (date "2026-11-03") (rev "0.1") '
                 f'(company "Thermomix TM31-4C (120 V) power board NPVTM31LTA-3")'
                 f' (comment 1 "Traced from a working board by continuity tests; see notes for confidence levels"))')
        o.append("(lib_symbols " + " ".join(s.sexpr() for s in self.libs.values()) + ")")
        path = f"/{self.root_uuid}" + (f"/{self.sheet_uuid}" if self.sheet_uuid else "")
        for sym, ref, value, pins, kw, ox, oy, t, b in self.placed:
            su = U()
            body = sym.body
            ref_y = oy - body[3] - 1.6
            val_y = oy - body[1] + 1.9
            fields = [f'(property "Reference" {q(ref)} (at {r(ox)} {r(ref_y)} 0) {FONT})',
                      f'(property "Value" {q(value)} (at {r(ox)} {r(val_y)} 0) {FONT})',
                      f'(property "Footprint" "" (at {r(ox)} {r(oy)} 0) {FONT_HIDE})',
                      f'(property "Datasheet" "" (at {r(ox)} {r(oy)} 0) {FONT_HIDE})']
            if kw.get("note"):
                fields.append(f'(property "Note" {q(kw["note"])} (at {r(ox)} {r(val_y + 2.3)} 0) '
                              f'(effects (font (size 1.0 1.0) italic)))')
            in_bom = "no" if kw.get("offboard") else "yes"
            dnp = "yes" if kw.get("dnp") else "no"
            pinlist = " ".join(f'(pin {q(p["num"])} (uuid {U()}))' for p in sym.pins)
            o.append(f'(symbol (lib_id "tm31:{sym.name}") (at {r(ox)} {r(oy)} 0) (unit 1) '
                     f'(in_bom {in_bom}) (on_board {"no" if kw.get("offboard") else "yes"}) (dnp {dnp}) '
                     f'(uuid {su}) ' + " ".join(fields) + " " + pinlist +
                     f' (instances (project {q(self.project)} (path {q(path)} (reference {q(ref)}) (unit 1)))))')
            # stubs + labels
            for key, net in pins.items():
                p = sym.pin(key)
                cx = ox + p["x"]
                cy = oy - p["y"]
                if net is None:
                    continue
                if net == "NC":
                    o.append(f"(no_connect (at {r(cx)} {r(cy)}) (uuid {U()}))")
                    continue
                if p["ang"] == 0:  # left side pin -> stub to the left
                    ex, ang, just = cx - 2.54, 180, "right"
                else:
                    ex, ang, just = cx + 2.54, 0, "left"
                o.append(f"(wire (pts (xy {r(cx)} {r(cy)}) (xy {r(ex)} {r(cy)})) "
                         f"(stroke (width 0) (type default)) (uuid {U()}))")
                o.append(f'(global_label {q(net)} (shape passive) (at {r(ex)} {r(cy)} {ang}) '
                         f'(fields_autoplaced) (effects (font (size 1.27 1.27)) (justify {just})) (uuid {U()}) '
                         f'(property "Intersheetrefs" "${{INTERSHEET_REFS}}" (at {r(ex)} {r(cy)} 0) {FONT_HIDE}))')
        for text, x, y, size in self.notes:
            o.append(f'(text {q(text)} (at {r(x)} {r(y)} 0) (effects (font (size {size} {size})) '
                     f'(justify left top)) (uuid {U()}))')
        for title, x, y in self.headers:
            o.append(f'(text {q(title)} (at {r(x)} {r(y)} 0) (effects (font (size 1.8 1.8) bold) '
                     f'(justify left top)) (uuid {U()}))')
            o.append(f'(polyline (pts (xy {r(x)} {r(y + 3.6)}) (xy {r(x + len(title) * 1.45)} {r(y + 3.6)})) '
                     f'(stroke (width 0.3) (type default)) (uuid {U()}))')
        o.append(")")
        return "\n".join(o)


def root_sheet(project, title, root_uuid, children, notes, paper="A3"):
    o = [f"(kicad_sch (version 20230121) (generator eeschema)", f"(uuid {root_uuid})", f'(paper "{paper}")',
         f'(title_block (title {q(title)}) (date "2026-11-03") (rev "0.1") '
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
