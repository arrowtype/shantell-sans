"""
    1. Copy sources to new folder
    2. Duplicate normal sources & run "bouncy" script on these, updating file & style names
    3. Run "organic" script on quirk sources
    4. copy features to UFOs
"""

import os
import shutil
# from fontParts.world import *
from fontParts.fontshell import RFont as Font

# start with hardcoded paths; optimize later

sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
    "quirkLight": "sources/shantell_organic--light.ufo",
    "quirkExtrabold": "sources/shantell_organic--extrabold.ufo",
    "bounceLight": "sources/shantell_bounce--light.ufo",
    "bounceExtrabold": "sources/shantell_bounce--extrabold.ufo",
}

prepDir = 'sources/wght_bnce_qurk'

# make folder 'wght_bnce_qurk' & copy in sources
def makePrepDir():
    if not os.path.exists(prepDir):
        os.mkdir(prepDir)

    for name, source in sources.items():
        try:
            copyTo = prepDir+'/'+os.path.split(source)[1]
            # destination = shutil.copytree(src, dest)
            if not os.path.exists(copyTo):
                shutil.copytree(source, copyTo)
        except FileNotFoundError:
            pass

        if name in ["light","extrabold"]:
            bounceCopy = prepDir+'/'+os.path.split(sources[f"bounce{name.title()}"])[1]
            if not os.path.exists(bounceCopy):
                shutil.copytree(source, bounceCopy)

# make alts in all fonts
def makeAlts(fonts, numOfAlts=2):
    """
        Make alts for all glyphs in fonts.
        Argument 'numOfAlts' is the number of alts. 
        E.g. Default numOfAlts=2 would result in a, a.alt1, a.alt2, etc
    """

    for font in fonts:
        layer = font.getLayer(font.defaultLayerName)

        newGlyphs = {}
        for glyph in font:
            glyph.clearImage()
            for i, alt in enumerate(range(numOfAlts)):
                glyphAltName = f"{glyph.name}.alt{i+1}"
                # glyphAlt = layer.newGlyph(glyphAltName)
                glyphAlt = glyph.copy()
                
                # glyphAlt.insertGlyph(glyph, name=glyphAltName)
                # layer[glyphAltName] = glyphAlt

                # newGlyphs[glyphAltName] = glyphAlt
                newGlyphs[glyphAltName] = layer[glyph.name]

        import pprint

        pprint.pprint(newGlyphs)

        for name,glyph in newGlyphs.items():
            layer[name] = glyph.copy()
            font[name].markColor = 0, 0, 1, 0.5

        font.save()




# shift baseline in bounce fonts
# def makeBounces():


# interpolate alts in quirk fonts
makePrepDir()

newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

fonts = [Font(path) for path in newFontPaths]

makeAlts(fonts)