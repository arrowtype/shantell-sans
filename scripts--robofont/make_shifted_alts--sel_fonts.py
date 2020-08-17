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


            # if 'alt1' in g.name:

            #     moveY = ((randomLimit-minShift) * random() + minShift) * -1

            #     g.moveBy((0,moveY))

            #     print(f"→ {g.name} moved by {moveY}")

            # if 'alt2' in g.name:

            #     moveY = ((randomLimit-minShift) * random() + minShift)

            #     g.moveBy((0,moveY))

            #     print(f"→ {g.name} moved by {moveY}")

            # offset bases, then correct components
            if 'alt' not in g.name:

                moveY = ((randomLimit-minShift) * random() + minShift) * positiveOrNegative()

                g.moveBy((0,moveY))

                print(f"→ {g.name} moved by {moveY}")

                alt1 = font[g.name + ".alt1"]
                alt1Moved = alt1.components[0].transformation
                alt1.components[0].transformation = (alt1Moved[0],alt1Moved[1],alt1Moved[2],alt1Moved[3],alt1Moved[4],alt1Moved[5]-moveY)

                alt2 = font[g.name + ".alt2"]
                alt2Moved = alt2.components[0].transformation
                alt2.components[0].transformation = (alt2Moved[0],alt2Moved[1],alt2Moved[2],alt2Moved[3],alt2Moved[4],alt2Moved[5]-moveY)



    # TODO: check for shifted base glyph; offset compenent shifts accordingly


    if save:
        font.save()

    if close:
        font.close()
