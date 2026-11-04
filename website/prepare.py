"""Stage the repository as an MkDocs project, so the website is built from the same Markdown files as the repo.

Usage: python3 website/prepare.py REPO_DIR STAGE_DIR
Result: STAGE_DIR/mkdocs.yml and STAGE_DIR/docs/ (a copy of the repository plus generated pages).

The repository layout is kept as-is inside docs/, so every relative link written for GitHub keeps working.
Generated additions:
  - index.md pages for linked folders (photo galleries, file listings),
  - hardware/schematic.md (the SVG sheets),
  - license.md (the LICENSE text),
  - links to folders and to LICENSE rewritten to those pages.
"""
import os
import re
import shutil
import sys

REPO, STAGE = (os.path.abspath(a) for a in sys.argv[1:3])
DOCS = os.path.join(STAGE, "docs")
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = (".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp")

if os.path.exists(STAGE):
    shutil.rmtree(STAGE)
shutil.copytree(REPO, DOCS, ignore=shutil.ignore_patterns(".git", ".github", "site", "website", "__pycache__", "*.zip"))
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(DOCS, "assets"))
os.makedirs(os.path.join(DOCS, "website"))
shutil.copy(os.path.join(HERE, "README.md"), os.path.join(DOCS, "website", "README.md"))
shutil.copy(os.path.join(HERE, "mkdocs.yml"), os.path.join(STAGE, "mkdocs.yml"))


def title(name):
    base = os.path.splitext(name)[0]
    base = re.sub(r"^\d+-", "", base).replace("-", " ").replace("_", " ")
    return base[:1].upper() + base[1:]


def write(rel, text):
    path = os.path.join(DOCS, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


# ---- license page
with open(os.path.join(REPO, "LICENSE"), encoding="utf-8") as f:
    write("license.md", "# License\n\n```text\n" + f.read().strip() + "\n```\n\n"
          "Machine-readable licensing: `REUSE.toml` in the repository.\n")


# ---- galleries
def gallery(folder, heading, intro, sub_sections=False):
    root = os.path.join(DOCS, folder)
    out = [f"# {heading}\n", intro + "\n"]
    dirs = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))) if sub_sections else [""]
    for d in dirs:
        if d:
            out.append(f"\n## {title(d)}\n")
        files = sorted(f for f in os.listdir(os.path.join(root, d)) if f.lower().endswith(IMG))
        for f in files:
            rel = f"{d}/{f}" if d else f
            out.append(f"\n### {title(f)}\n\n[![{title(f)}]({rel}){{ loading=lazy }}]({rel})\n")
    write(os.path.join(folder, "index.md"), "\n".join(out))


gallery("photos", "Photos", "Original photos of the board (resized, metadata removed). Click a photo for full size.",
        sub_sections=True)
gallery("images/annotated", "Annotated maps",
        "Functional blocks and traced nets marked on both sides of the board. Click an image for full size.")
gallery("images/diagrams", "Diagrams",
        "PNG copies of the Mermaid diagrams used in the documentation pages.")

# ---- schematic viewer
sheets = sorted(f for f in os.listdir(os.path.join(DOCS, "hardware", "svg")) if f.endswith(".svg"))
out = ["# Schematic sheets\n",
       "Rev 0.2, drawn from continuity tests on a working board. Read the confidence notes on each sheet: "
       "`?` = value not read, *approx* = inferred.  \n"
       "Click a sheet to open it full size (zoom in your browser). "
       "Also available as [PDF](TM31_power_board_schematic.pdf) and as a [KiCad project](kicad/index.md); "
       "see [how to read it](README.md).\n"]
SHEET_TITLES = {"1": "1. Overview", "2": "2. Mains input & heater", "3": "3. Motor DC bus (doubler) & pre-charge",
                "4": "4. Motor power stage", "5": "5. Safety logic", "6": "6. Analog sensing",
                "7": "7. MCU, programming header & front-panel link", "8": "8. Low-voltage power supply"}
for f in sheets:
    t = SHEET_TITLES.get(f.split("-")[0], title(f))
    out.append(f"\n## {t}\n\n[![{t}](svg/{f}){{ loading=lazy }}](svg/{f})\n")
write("hardware/schematic.md", "\n".join(out))


# ---- index pages for any other linked folder (file listings)
def listing(folder):
    root = os.path.join(DOCS, folder)
    files = sorted(f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and f != "index.md")
    lines = [f"# {folder}/\n", "Files in this folder (click to download):\n"]
    lines += [f"- [`{f}`]({f})" for f in files]
    write(os.path.join(folder, "index.md"), "\n".join(lines) + "\n")


LINK = re.compile(r"(\]\()([^)\s#]+)(#[^)\s]*)?(\))")
md_files = []
for dp, dn, fn in os.walk(DOCS):
    md_files += [os.path.join(dp, f) for f in fn if f.endswith(".md")]
for path in md_files:
    with open(path, encoding="utf-8") as f:
        text = f.read()

    def fix(m):
        target = m.group(2)
        if re.match(r"^[a-z]+:", target):
            return m.group(0)
        here = os.path.dirname(path)
        abs_t = os.path.normpath(os.path.join(here, target))
        if os.path.basename(abs_t) == "LICENSE":
            new = os.path.relpath(os.path.join(DOCS, "license.md"), here)
        elif os.path.isdir(abs_t):
            for name in ("index.md", "README.md"):
                if os.path.exists(os.path.join(abs_t, name)):
                    break
            else:
                listing(os.path.relpath(abs_t, DOCS))
                name = "index.md"
            new = os.path.relpath(os.path.join(abs_t, name), here)
        else:
            return m.group(0)
        return m.group(1) + new.replace(os.sep, "/") + (m.group(3) or "") + m.group(4)

    new_text = LINK.sub(fix, text)
    if new_text != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)

if not os.path.exists(os.path.join(DOCS, "hardware", "kicad", "index.md")):
    listing("hardware/kicad")
print("staged", DOCS)
