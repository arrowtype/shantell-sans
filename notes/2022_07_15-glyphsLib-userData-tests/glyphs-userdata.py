# from glyphsLib import GSFont, classes
import glyphsLib
from glyphsLib import GSFont

print(glyphsLib.__version__)

print(GSFont)

glyphs_file = "sources/shantellsans-wght_ital_IRGL.glyphs"

font =  GSFont(glyphs_file)

print(font)

userData = font.userData

userData["bounces"] = {}

userData["bounces"]["A"] = 36

font.save(glyphs_file)