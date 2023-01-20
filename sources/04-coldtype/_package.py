import shutil, subprocess
from pathlib import Path

coldtype_dir = Path(__file__).parent

# Render all coldtype scripts

for src in coldtype_dir.glob("*.coldtype.py"):
    if src.name.startswith("loop-glyphs"):
        subprocess.run(["coldtype", src, "-ps", "0.25", "-rar", "-mp", "1"])
    else:
        subprocess.run(["coldtype", src, "-ps", "0.25", "-rar"])

# Find all gifs & mp4s and copy them to a top-level specimens/coldtype directory
# (could be part of step above but this way that can be debugged separately)

root_dir = coldtype_dir.parent.parent
specimens_dir = root_dir / "specimens/coldtype"
specimens_dir.mkdir(exist_ok=True)

specimens = []

for render in (coldtype_dir / "renders").iterdir():
    if render.is_dir():
        specimens.extend(list(render.glob("*.gif")))
        specimens.extend(list(render.glob("*.mp4")))

for s in specimens:
    shutil.copy2(s, specimens_dir)
    print(s)