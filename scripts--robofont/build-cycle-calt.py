'''
    Pseudo-randomly shift glyph Y positions in UFOs
'''

import sys
from fontParts.world import *

try:
    sourceUFO = sys.argv[1]
except IndexError:
    print("At least one arg required: path of UFO with code ligature glyphs")


font = OpenFont(sourceUFO, showInterface=False)

caltCode = f"""
feature calt {{
    @randomCycle1 = [{" ".join(sorted([g.name for g in font if 'alt' not in g.name]))}];
    @randomCycle2 = [{" ".join(sorted([g.name for g in font if 'alt1' in g.name]))}];
    @randomCycle3 = [{" ".join(sorted([g.name for g in font if 'alt2' in g.name]))}];

    sub @randomCycle1 @randomCycle1' by @randomCycle2;
    sub @randomCycle2 @randomCycle1' by @randomCycle3;
}} calt;
"""

font.close()


feaPath = "sources/features/cycle-calt.fea"
with open(feaPath, "w") as f:
    f.write(caltCode)

print(f"→ caltCode saved to {feaPath}")