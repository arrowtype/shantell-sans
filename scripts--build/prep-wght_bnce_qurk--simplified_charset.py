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

altsToMake += "éñ"

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
        
        font.save()

    return altsToMakeGlyphNames


def positiveOrNegative():
    return 1 if random() < 0.5 else -1

def shiftGlyphs(font,randomLimit=200,minShift=50):
    """
        Shift glyphs in Bouncy sources.
    """

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

    # movements = {}

    print("shifting glyphs ", font.path)

    for g in font:

        moveY = 0
    
        # print(g)
        if 'alt1' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * -1
            g.moveBy((0,moveY))
            # movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

        if 'alt2' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift)
            g.moveBy((0,moveY))
            # movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

        # change non-alt glyphs
        if 'alt' not in g.name and g.name not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            # movements[g.name] = moveY
            # print(f"→ {g.name} moved by {moveY}")

        g.lib['com.arrowtype.yShift'] = moveY

    # correct positioning of base glyphs in composed glyphs
    for g in font:

        if len(g.components) >= 1 and g.name.split(".")[0] not in glyphsToNotShift:

            print("now shifting ", g.name)

            # look up Yshift of main baseGlyph (how to find the main one? check that its base glyph has a positive width)
            mainBase = [c.baseGlyph for c in g.components if font[c.baseGlyph].width >= 1][0]
            baseShift = font[mainBase].lib['com.arrowtype.yShift']

            print("mainBase is ", mainBase)
            print("baseShift is ", baseShift)
            print()

            for c in g.components:
                if c.baseGlyph is not mainBase:
                    c.moveBy((0,baseShift))

            # wait, do you have to set components to alts, first?

            # inverse that shift in the main base


            ## move BOTH components in a new way
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            g.lib['com.arrowtype.yShift'] = moveY


            # ? record moveY
            
            # # TODO? split into up/down/random, like other glyphs

            # for c in g.components:
            #     correctedY = -1 * g.lib['com.arrowtype.yShift']
            #     c.moveBy((0,correctedY))
            #     # if c.baseGlyph in movements.keys():
            #         # move by opposite Y value of movement of parent glyph
            #         # correctedY = -1 * movements[c.baseGlyph]

    print()
    print()

    font.save()

# TODO: this seems to be disrupting component references in the organic fonts – fix it
def interpolateAlts(normalFont, organicFont, altsMadeForList):
    """
        Make partially-irregular glyphs in "organic" sources.
    """
    for g in organicFont:
        # if g.unicodes and g.unicodes[0] in altsToMakeList and 'alt' not in g.name:
        if g.name in altsMadeForList and '.alt' not in g.name:
            # interpolate alt1 10% towards organicFont glyph
            factor = 0.1
            organicFont[f'{g.name}.alt1'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            # interpolate alt2 66% towards organicFont glyph
            factor = 0.66
            # print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt2'].interpolate(factor, normalFont[g.name], organicFont[g.name])

    organicFont.save()

def makeComponentsAlts(fonts, numOfAlts=2):
    """
       Set components to alt baseGlyphs – important for composed glyphs like i & j
    """
    for font in fonts:
        print(font)
        for glyph in font:
            if ".alt" in glyph.name and glyph.components:
                suffix = glyph.name.split(".")[-1]
                for c in glyph.components:
                    if ".alt" not in c.baseGlyph:
                        c.baseGlyph = c.baseGlyph + "." + suffix
                glyph.update()

        font.save()


def decomposeCoreGlyphs(fonts):
    """
        Go through fonts and decompose alt glyphs, to avoid alignment issues in glyphs like i & j

        May not be necessary...

        TODO: decide whether to remove this step
    """
    for font in fonts:
        for g in font:
            if ".alt" in g.name and g.components:
                g.decompose()
                g.update()
        
        font.save()

def removeAltUnicodes(fonts):
    """
        Make sure alts don’t have unicode values, which would be duplicates and probably cause problems.
    """
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

    print("🤖 Making composed alts point to alt components")
    makeComponentsAlts(fonts)

    # shift alts in bounce fonts
    print("🤖 Shifting bouncy alts")
    for font in fonts:
        if "bounce" in font.path:
            shiftGlyphs(font)

    # interpolate alts in quirk fonts
    print("🤖 Interpolating organic alts")

    # Dumb setup. Will it work?
    interpolateAlts([f for f in fonts if "shantell--light" in f.path][0], [f for f in fonts if "organic--light" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--extrabold" in f.path][0], [f for f in fonts if "organic--extrabold" in f.path][0], altsMadeForList)
    
    print("🤖 Making composed alts point to alt components")
    makeComponentsAlts(fonts)

    # print("🤖 Decomposing alts with components")
    # decomposeCoreGlyphs(fonts)

    print("🤖 Removing unicodes from alt glyphs")
    removeAltUnicodes(fonts)

if __name__ == "__main__":
    main()