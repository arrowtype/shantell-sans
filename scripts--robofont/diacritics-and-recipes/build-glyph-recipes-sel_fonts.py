'''
Build accented glyphs in RoboFont3 using Glyph Construction.
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder

center = False

# ringcomb.A = ringcomb
txt="""\
hyphen_line.3 = hyphen.line & hyphen.line & hyphen.line
hyphen_line.4 = hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.5 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.6 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.7 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.8 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.9 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.10 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.11 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.12 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.13 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.14 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.15 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.16 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.17 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.18 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.19 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.20 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.21 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.22 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.23 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.24 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.25 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.26 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.27 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.28 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.29 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.30 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.31 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.32 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.33 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.34 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.35 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.36 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.37 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.38 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.39 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.40 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.41 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.42 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.43 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.44 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.45 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.46 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.47 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.48 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.49 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
hyphen_line.50 = hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line & hyphen.line
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



    font.save()
    font.close()
