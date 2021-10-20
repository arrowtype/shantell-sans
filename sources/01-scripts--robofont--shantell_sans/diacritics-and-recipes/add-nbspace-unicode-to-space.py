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
    # font['space'].unicodes = (font['space'].unicodes[0], int("00A0",16))
    font['space'].unicodes = (int("0020",16), )

    print("space unicodes now ", font['space'].unicodes)

    font.save()
    font.close()