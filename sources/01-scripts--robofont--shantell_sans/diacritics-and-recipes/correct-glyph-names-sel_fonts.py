'''
Build accented glyphs in RoboFont3 using Glyph Construction.
'''

from vanilla.dialogs import *
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder


files = getFile("Select files to build glyphs in", allowsMultipleSelection=True, fileTypes=["ufo"])

for file in files:
    font = OpenFont(file, showInterface=False)

    print(font.info.familyName, font.info.styleName)

    # adds unicode 00A0 (non-breaking space) to the 'space' glyph of the font
    font['gnrl:hyphen'].name = "uni2010"

    font.save()
    font.close()

