
'''
    Decompose alt1 & alt2
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from random import random

files = getFile("Select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])

for file in files:
    f = OpenFont(file, showInterface=False)

    for g in f:
        if 'alt1' in g.name or 'alt2' in g.name:
            g.decompose()

    f.save()
    f.close()
