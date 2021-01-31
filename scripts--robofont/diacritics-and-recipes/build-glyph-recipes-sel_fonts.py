'''
Build accented glyphs in RoboFont3 using Glyph Construction.
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder

center = False

# ringcomb.A = ringcomb
txt="""\
Aring = A + ringcomb.A@ring
"""


print(txt)
# get the actual glyph constructions from text
constructions = ParseGlyphConstructionListFromString(txt)



files = getFile("Select files to build glyphs in", allowsMultipleSelection=True, fileTypes=["ufo"])

# collect glyphs to ignore if they already exist in the font
ignoreExisting = [L.split('=')[0].strip()[1:] for L in txt.split('\n') if L.startswith('?')]

for file in files:
    font = OpenFont(file, showInterface=True)
    # font = OpenFont(file, showInterface=False)

    print(font)

    # iterate over all glyph constructions
    for construction in constructions:

        print(construction)
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
        glyph.markColor = 1, 0, 0, 0.5

        # if no unicode was given, try to set it automatically
        if glyph.unicode is None:
            glyph.autoUnicodes()

        if center:
            width = font["e"].width

            glyph.width = width

            totalMargin = glyph.leftMargin + glyph.rightMargin
            glyph.leftMargin = totalMargin/2
            glyph.rightMargin = totalMargin/2

            glyph.width = width



    # font.save()
    # font.close()
