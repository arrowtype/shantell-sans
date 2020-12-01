"""
    This script will...
    1. Copy main & organic sources to new folder
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources

    # TODO
        - [ ] remove unicodes from alts
        - [ ] dont mess up component glyphs in the shifted alts (shift components along with bases)
        - [ ] give diacritics different levels of bounce & pop/dynamics/variety(?)
        - [ ] build in feature copier? (currently, you have to separate copy in the features  )
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

prepDir = 'sources/wght_bnce_dynm--prepped'

# make folder 'wght_bnce_dynm' & copy in sources
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

        # set components to alt baseGlyphs – especially vital for i & j

        altSuffixes = [f".alt{x}" for x in range(1,numOfAlts+1)]

        for glyph in font:
            # check if glyphName includes alt suffix - https://www.geeksforgeeks.org/python-test-if-string-contains-element-from-list/
            if bool([suffix for suffix in altSuffixes if(suffix in glyph.name)]):
                suffix = glyph.name.split(".")[-1]
                if len(glyph.components) >= 1:
                    for c in glyph.components:
                        c.baseGlyph = c.baseGlyph + "." + suffix

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
        # and DON’t change accent positions
        accents = "gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcmb dieresiscomb ringcomb caroncomb dotbelowcmb cedillacomb ogonekcmb".split()
        if 'alt' not in g.name and g.name not in accents:
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            print(f"→ {g.name} moved by {moveY}")

    font.save()
    print("font saved!")

def interpolateAlts(normalFont, organicFont):
    for g in organicFont:
        if 'alt' not in g.name:
            # interpolate gOneThird and move to organicFont[f'{g.name}.alt1']
            # factor = 0.33
            factor = 0.1
            print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt1'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            # interpolate gTwoThirds and move to organicFont[f'{g.name}.alt2']
            # factor = 0.66
            factor = 0.6
            print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt2'].interpolate(factor, normalFont[g.name], organicFont[g.name])

    organicFont.save()


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
    print("🤖 Shifting bouncy alts")
    for font in fonts:
        if "bounce" in font.path:
            shiftAlts(font)

    # interpolate alts in quirk fonts
    print("🤖 Interpolating organic alts")

    print([f for f in fonts if "shantell--light" in f.path][0])

    # Dumb setup. Will it work?
    interpolateAlts([f for f in fonts if "shantell--light" in f.path][0], [f for f in fonts if "organic--light" in f.path][0])
    interpolateAlts([f for f in fonts if "shantell--extrabold" in f.path][0], [f for f in fonts if "organic--extrabold" in f.path][0])

if __name__ == "__main__":
    main()