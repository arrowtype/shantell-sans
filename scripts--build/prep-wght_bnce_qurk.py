"""
    1. Copy sources to new folder
    2. Duplicate normal sources & run "bouncy" script on these, updating file & style names
    3. Run "organic" script on quirk sources
    4. copy features to UFOs
"""

import os
import shutil
import shutil
from fontParts.fontshell import RFont as Font
from fontParts.world import *
from random import random

# start with hardcoded paths; optimize later

sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
    "quirkLight": "sources/shantell_organic--light.ufo",
    "quirkExtrabold": "sources/shantell_organic--extrabold.ufo",
    "bounceLight": "sources/shantell_bounce--light.ufo",
    "bounceExtrabold": "sources/shantell_bounce--extrabold.ufo",
}

prepDir = 'sources/wght_bnce_qurk--prepped'

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
                glyphAlt = glyph.copy()
                newGlyphs[glyphAltName] = layer[glyph.name]

        for name,glyph in newGlyphs.items():
            layer[name] = glyph.copy()
            font[name].markColor = 0, 0, 1, 0.5

        font.save()

def positiveOrNegative():
    return 1 if random() < 0.5 else -1

def shiftAlts(font,randomLimit=200,minShift=50):
    print(font)
    print(font.path)
    for g in font:
        print(g)
        if 'alt1' in g.name:
            moveY = round((randomLimit-minShift) * random() + minShift) * -1
            g.moveBy((0,moveY))
            print(f"→ {g.name} moved by {moveY}")

        if 'alt2' in g.name:
            moveY = round((randomLimit-minShift) * random() + minShift)
            g.moveBy((0,moveY))
            print(f"→ {g.name} moved by {moveY}")

        # offset bases, then correct components
        if 'alt' not in g.name:
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            print(f"→ {g.name} moved by {moveY}")

    font.save()
    print("font saved! (?)")


def main():
    if os.path.exists(prepDir):
        shutil.rmtree(prepDir,ignore_errors=True)

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir()

    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    print("🤖 Making alts")
    makeAlts(fonts)

    # shift alts in bounce fonts
    for font in fonts:
        if "bounce" in font.path:
            shiftAlts(font)

    # interpolate alts in quirk fonts

if __name__ == "__main__":
    main()