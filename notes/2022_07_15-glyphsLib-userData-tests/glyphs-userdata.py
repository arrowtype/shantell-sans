# from glyphsLib import GSFont, classes
import glyphsLib
from glyphsLib import GSFont

print(glyphsLib.__version__)

print(GSFont)

glyphs_file = "sources/shantellsans.glyphs"

font =  GSFont(glyphs_file)

print(font)

# userData = font.userData

# print(userData)

# font.save(glyphs_file)