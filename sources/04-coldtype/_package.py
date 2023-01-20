import shutil, subprocess
from pathlib import Path

coldtype_dir = Path(__file__).parent

# Render all coldtype scripts

if True: # (very time-consuming, though should be faster with -mp 1)
    subprocess.run(["coldtype", coldtype_dir, "-mp", "1", "-rd"])

# Find all gifs & mp4s and copy them to a top-level specimens/coldtype directory

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