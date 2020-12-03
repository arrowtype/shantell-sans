"""
    This script will...
    1. Copy main & organic sources to new folder
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources

    # TODO
        - [x] remove unicodes from alts
        - [x] dont mess up component glyphs in the shifted alts (shift components along with bases)
        - [ ] restrict this to *only* make shifted alts for a core character set (maybe ASCII?) – make this configurable with a list of characters
        - [ ] decompose glyphs in the core charset which include components, to avoid issue https://github.com/googlefonts/ufo2ft/issues/437

        Maybe?
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

prepDir = 'sources/wght_bnce_flux--smpl--prepped'

# characters from Python string.printable
altsToMake = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

# get integer unicode values for string of characters from above
altsToMakeList = [ord(char) for char in altsToMake]


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

    altsToMakeGlyphNames = [g.name for g in fonts[0] if g.unicodes and g.unicodes[0] in altsToMakeList]


    for gname in altsToMakeGlyphNames:
        g = fonts[0][gname]
        for c in g.components:
            altsToMakeGlyphNames.append(c.baseGlyph)

    print(" ".join(altsToMakeGlyphNames))

    for font in fonts:

        print(font)
        # for glyph in alts, if glyph has components, add those components to the list of glyphs to make alts for - e.g. add idotless, jdotless, and dotcomb
    

        layer = font.getLayer(font.defaultLayerName)

        newGlyphs = {}
        for glyph in font:
            # if glyph.unicodes and glyph.unicodes[0] in altsToMakeList:
            if glyph.name in altsToMakeGlyphNames:
                glyph.clearImage()
                # make alts
                for i, alt in enumerate(range(numOfAlts)):
                    glyphAltName = f"{glyph.name}.alt{i+1}"
                    glyphAlt = glyph.copy()
                    newGlyphs[glyphAltName] = layer[glyph.name]

        # mark new glyphs with colors
        for name,glyph in newGlyphs.items():
            layer[name] = glyph.copy()
            font[name].markColor = 0, 0, 1, 0.5

        # set components to alt baseGlyphs – especially vital for i & j
        for glyph in font:
            if ".alt" in glyph.name and len(glyph.components) >= 1:
                suffix = glyph.name.split(".")[-1]
                for c in glyph.components:
                    c.baseGlyph = c.baseGlyph + "." + suffix

        font.save()

    return altsToMakeGlyphNames

def positiveOrNegative():
    return 1 if random() < 0.5 else -1

def shiftAlts(font,randomLimit=200,minShift=50):
    # print(font)
    # print(font.path)

    glyphsToNotShift ="\
            onesuperior twosuperior threesuperior fraction zero.dnom one.dnom two.dnom three.dnom \
            four.dnom five.dnom six.dnom seven.dnom eight.dnom nine.dnom zero.numr one.numr two.numr \
            three.numr four.numr five.numr six.numr seven.numr eight.numr nine.numr zero.inferior \
            one.inferior two.inferior three.inferior four.inferior five.inferior six.inferior seven.inferior \
            eight.inferior nine.inferior zero.superior four.superior five.superior six.superior \
            seven.superior eight.superior nine.superior \
            gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcmb dieresiscomb \
            ringcomb hungarumlautcmb caroncomb dotbelowcmb cedillacomb acute grave hungarumlaut circumflex \
            caron breve tilde macron dieresis dotaccent ring cedilla ogonek \
        ".split()

    movements = {}

    for g in font:
    
        # print(g)
        if 'alt1' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * -1
            g.moveBy((0,moveY))
            movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

        if 'alt2' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift)
            g.moveBy((0,moveY))
            movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

        # change non-alt glyphs
        if 'alt' not in g.name and g.name not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

    
    for g in font:

        if len(g.components) >= 1 and g.name.split(".")[0] not in glyphsToNotShift:
            # TODO? split into up/down/random, like other glyphs
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))

            movements[g.name] = moveY

            for c in g.components:
                if c.baseGlyph in movements.keys():
                    # move by opposite Y value of movement of parent glyph
                    correctedY = -1 * movements[c.baseGlyph]
                    c.moveBy((0,correctedY))

    font.save()

def interpolateAlts(normalFont, organicFont, altsMadeForList):
    for g in organicFont:
        # if g.unicodes and g.unicodes[0] in altsToMakeList and 'alt' not in g.name:
        if g.name in altsMadeForList and 'alt' not in g.name:
            # interpolate gOneThird and move to organicFont[f'{g.name}.alt1']
            # factor = 0.33
            factor = 0.1
            # print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt1'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            # interpolate gTwoThirds and move to organicFont[f'{g.name}.alt2']
            # factor = 0.66
            factor = 0.6
            # print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt2'].interpolate(factor, normalFont[g.name], organicFont[g.name])

    organicFont.save()

# TODO decompose alts with components
# i j etc - check list of alts for components & decompose
def decomposeCoreGlyphs(fonts):
    """
        Go through fonts and decompose alt glyphs, to avoid alignment issues in glyphs like i & j
    """
    for font in fonts:
        for g in font:
            if ".alt" in g.name and g.components:
                g.decompose()
                g.update()
        
        font.save()

def removeAltUnicodes(fonts):
    for font in fonts:
        for g in font:
            if ".alt" in g.name:
                g.unicodes = []
        font.save()

def main():
    if os.path.exists(prepDir):
        shutil.rmtree(prepDir,ignore_errors=True)

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir()

    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    print("🤖 Making alts")
    altsMadeForList = makeAlts(fonts)

    # shift alts in bounce fonts
    print("🤖 Shifting bouncy alts")
    for font in fonts:
        if "bounce" in font.path:
            shiftAlts(font)

    # interpolate alts in quirk fonts
    print("🤖 Interpolating organic alts")

    # print([f for f in fonts if "shantell--light" in f.path][0])

    # Dumb setup. Will it work?
    interpolateAlts([f for f in fonts if "shantell--light" in f.path][0], [f for f in fonts if "organic--light" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--extrabold" in f.path][0], [f for f in fonts if "organic--extrabold" in f.path][0], altsMadeForList)
    
    print("🤖 Decomposing alts with components")
    decomposeCoreGlyphs(fonts)

    print("🤖 Removing unicodes from alt glyphs")
    removeAltUnicodes(fonts)

if __name__ == "__main__":
    main()