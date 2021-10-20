'''
    Pseudo-randomly shift glyph Y positions in UFOs
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from random import random

files = getFile("Select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])


randomLimit = 200

def positiveOrNegative():
    return 1 if random() < 0.5 else -1


for file in files:
    font = OpenFont(file, showInterface=True)

    for g in font:

        moveY = randomLimit * random() * positiveOrNegative()

        g.moveBy((0,moveY))

        print(f"→ {g.name} moved by {moveY}")


    if save:
        font.save()

    if close:
        font.close()
