'''
    Pseudo-randomly shift glyph Y positions in UFOs
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from random import random
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder

files = getFile("Select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])


randomLimit = 200
minShift = 50

makeAlts = False
shiftAlts = True
save  = False
close = False

def positiveOrNegative():
    return 1 if random() < 0.5 else -1

for file in files:
    font = OpenFont(file, showInterface=True)

    if makeAlts:

        constructionTxt = ''

        for g in font:

            constructionTxt += f'''
                {g.name}.alt1 = {g.name}
                {g.name}.alt2 = {g.name}\
            '''

        print(constructionTxt)

        constructions = ParseGlyphConstructionListFromString(constructionTxt)

        for construction in constructions:

            # build a construction glyph
            constructionGlyph = GlyphConstructionBuilder(construction, font)

            # if the construction for this glyph was preceded by `?`
            # and the glyph already exists in the font, skip it
            if constructionGlyph.name in font and constructionGlyph.name in ignoreExisting:
                continue

            # get the destination glyph in the font
            glyph = font.newGlyph(constructionGlyph.name, clear=True)

            # draw the construction glyph into the destination glyph
            constructionGlyph.draw(glyph.getPen())

            # copy construction glyph attributes to the destination glyph
            glyph.name = constructionGlyph.name
            glyph.unicode = constructionGlyph.unicode
            glyph.width = constructionGlyph.width
            glyph.markColor = 0, 0, 0, 0.5

    if shiftAlts:
        for g in font:

            # cheat to make it work more quickly
            if 'alt' in g.name:

                moveY = (randomLimit-minShift) * random() * positiveOrNegative() + minShift

                g.moveBy((0,moveY))

                print(f"→ {g.name} moved by {moveY}")

    # TODO: check for shifted base glyph; offset compenent shifts accordingly


    if save:
        font.save()

    if close:
        font.close()
