"""
    This script will...
    1. Copy main & organic sources to new folder
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources

    # TODO
        - [x] remove unicodes from alts
        - [x] dont mess up component glyphs in the shifted alts (shift components along with bases)
            - [ ] figure out how to also cover ogonek (not working somehow) and single-component glyphs like oslash and lslash
        - [x] restrict this to *only* make shifted alts for a core character set (maybe ASCII?) – make this configurable with a list of characters
            - [x] decide what accented characters to add
        - [ ] generate fresh calt feature code to make all alts work
        - [x] copy designspaces into prep folder

        - [x] fix alignment of accents in organic/irregular glyphs – probably reattach to anchors

        Also
        - [ ] Link to this script at https://github.com/googlefonts/ufo2ft/issues/437 once the repo is public

        Maybe?
        - [ ] give diacritics different levels of bounce & pop/dynamics/variety(?)
        - [ ] build in feature copier? (currently, you have to separate copy in the features  )

        # TODO: generate calt feature code to catch all glyphs with .alts
"""

import os
import shutil
import shutil
from fontParts.fontshell import RFont as Font
from fontParts.world import *
from random import random

# --------------------------------------------------------
# START configuration

# start with hardcoded paths; optimize later

sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
    "quirkLight": "sources/shantell_organic--light.ufo",
    "quirkExtrabold": "sources/shantell_organic--extrabold.ufo",
    "bounceLight": "sources/shantell_bounce--light.ufo",
    "bounceExtrabold": "sources/shantell_bounce--extrabold.ufo",
}

designspaces = ["sources/shantell-wght_BNCE_FLUX--smpl.designspace", "sources/shantell-wght_BNCE_FLUX--smpl--static.designspace"]

prepDir = 'sources/wght_bnce_flux--smpl--prepped'

# all letters
altsToMake = "AÀÁÂÃÄÅĀĂĄǍBCÇĆČDĎEÈÉÊËĒĔĘĚFGĞHIÌÍÎÏĪĬĮİJKLMNÑŃŇOÒÓÔÕÖŌŎŐPQRŔŘSŚŞŠTŤUÙÚÛÜŪŬŮŰŲǓVWXYÝŸZŹŻŽÆØǾĲŁŒΩaàáâãäåāăąǎbcçćčdďeèéêëēĕęěfgğhiìíîïīĭįjklmnñńňoòóôõöōŏőpqrŕřsśşštťuùúûüūŭůűųǔvwxyýÿzźżžßæÞðþẞ"

# numbers & basic symbols
altsToMake += "0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”‘’"

# some glyphs just need to stick together
glyphsToDecompose = "ij oe".split()

# feature code to be inserted into generated UFOs
feaCode = """\
languagesystem DFLT dflt;
languagesystem latn dflt;

include(../features/features/common.fea);
include(../features/features/frac.fea);
include(../features/features/case.fea);
include(../features/features/numr_dnom_supr_infr.fea);
include(../features/cycle-calt.fea)
"""

# END configuration
# --------------------------------------------------------


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


def decomposeDigraphs(fonts):
    for font in fonts:
        for g in font:
            if g.name in glyphsToDecompose:
                g.decompose()

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

    altsToMakeGlyphNames = list(set(altsToMakeGlyphNames))

    print(" ".join(altsToMakeGlyphNames))

    for font in fonts:

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

def findMainBaseGlyphName(font, glyph):
    return [c.baseGlyph for c in glyph.components if font[c.baseGlyph].width >= 1][0]

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
            caron breve tilde macron dieresis dotaccent ring cedilla ogonek ogonekcmb \
        ".split()

    for g in font:
        moveY = 0

        if 'alt1' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * -1
            g.moveBy((0,moveY))

        if 'alt2' in g.name and g.name.split(".")[0] not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift)
            g.moveBy((0,moveY))

        # change non-alt glyphs
        if 'alt' not in g.name and g.name not in glyphsToNotShift and len(g.components) == 0:
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))

        # record shift in the glyph’s lib for later use
        g.lib['com.arrowtype.yShift'] = moveY

    # correct positioning of base glyphs in composed glyphs
    for g in font:

        if len(g.components) >= 1 and g.name.split(".")[0] not in glyphsToNotShift:

            # look up Yshift of main baseGlyph
            mainBase = findMainBaseGlyphName(font, g)
            baseShift = font[mainBase].lib['com.arrowtype.yShift']

            # in multi-component glyphs, shift accents to match bases
            if len(g.components) > 1:
                for c in g.components:
                    if c.baseGlyph is not mainBase:
                        c.moveBy((0,baseShift))
                # move glyph to normal position
                g.moveBy((0,-baseShift))

            #  correct single-component glyphs like oslash, lslash
            else:
                for c in g.components:
                    if c.baseGlyph is mainBase:
                        c.moveBy((0,-baseShift))

            # move full glyph in a new way
            moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative()
            g.moveBy((0,moveY))
            g.lib['com.arrowtype.yShift'] = moveY

            # TODO: correct ij, oe, which are out-of-whack

            # # TODO? maybe split accented alts into up/down/random, like other glyphs

    font.save()

def makeComponentsAlts(fonts, numOfAlts=2):
    """
       Set components to alt baseGlyphs – important for composed glyphs like i & j
    """
    for font in fonts:
        # print(font)
        for glyph in font:
            if ".alt" in glyph.name and glyph.components:
                suffix = glyph.name.split(".")[-1]
                for c in glyph.components:
                    if ".alt" not in c.baseGlyph:
                        c.baseGlyph = c.baseGlyph + "." + suffix
                glyph.update()

        font.save()

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


# def decomposeCoreGlyphs(fonts):
#     """
#         Go through fonts and decompose alt glyphs, to avoid alignment issues in glyphs like i & j

#         May not be necessary...

#         TODO: decide whether to remove this step
#     """
#     for font in fonts:
#         for g in font:
#             if ".alt" in g.name and g.components:
#                 g.decompose()
#                 g.update()
        
#         font.save()


def removeAltUnicodes(fonts):
    """
        Make sure alts don’t have unicode values, which would be duplicates and probably cause problems.
    """
    for font in fonts:
        for g in font:
            if ".alt" in g.name:
                g.unicodes = []
        font.save()

def correctAccents(fonts):
    """
        In composed glyphs, fix alignment between accents and bases, using anchor positions & shift records
    """

    for font in fonts:
        print("\n\n----------------------------------------------------------------")
        print(font.path)
        for g in font:
            if len(g.components) >= 2:
                mainBase = findMainBaseGlyphName(font, g)
                accents = [c for c in g.components if c.baseGlyph != mainBase]

                # dict of anchors in main base, name:(x,y)
                mainBaseAnchors = {anchor.name:anchor.position for anchor in font[mainBase].anchors}

                for c in accents:
                    accentAnchors = font[c.baseGlyph].anchors
                    # dict of anchors in accent, but exlude non-underscored anchors
                    accentAnchors = {anchor.name.replace("_",""):anchor.position for anchor in font[c.baseGlyph].anchors if "_" in anchor.name}

                    commonAnchors = set(mainBaseAnchors.keys()).intersection(accentAnchors.keys())

                    if len(commonAnchors) == 0:
                        # print("XXX no common anchors ", g.name, c.baseGlyph, commonAnchors)
                        # print()
                        # if no common anchors, skip
                        pass
                    elif len(commonAnchors) == 1:

                        transformBefore = c.offset

                        commonAnchor = list(commonAnchors)[0]

                        mainBaseAnchorPos = mainBaseAnchors[commonAnchor]
                        accentBaseAnchorPos = accentAnchors[commonAnchor]

                        shiftX = mainBaseAnchorPos[0] - accentBaseAnchorPos[0]
                        
                        try:
                            # add bounce Y-shift in base & composed glyphs, if applicable
                            shiftY = mainBaseAnchorPos[1] - accentBaseAnchorPos[1] - font[mainBase].lib['com.arrowtype.yShift'] + g.lib['com.arrowtype.yShift']
                        except:
                            shiftY = mainBaseAnchorPos[1] - accentBaseAnchorPos[1]

                        
                        c.transformation = [1,0,0,1,shiftX,shiftY]

                        g.update()

                    else:
                        pass
                        # TODO check if this needs special handling; it probably does
                        # print("MULTIPLE COMMON ANCHORS!")
                        # print("\t", g.name, c.baseGlyph, list(commonAnchors))
                        # print()

        font.save()

                    # get intersection


def addFeaCode(fonts):
    """
        Add feature code to generated UFOs
    """

    for font in fonts:
        font.features.text = feaCode
        font.save()


def main():

    # The setup

    if os.path.exists(prepDir):
        shutil.rmtree(prepDir,ignore_errors=True)

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir()

    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    # The sausage making

    print("🤖 Decomposing digraphs")
    decomposeDigraphs(fonts)

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

    # TODO? fix accent alignment in irregular glyphs – possibly by re-attaching accents to new anchor positions?
    
    # yes, this is needed twice. Once to make shifting work well, then again to make irregular sources compatible again after interpolation
    print("🤖 Making composed alts point to alt components – repeating to fix irregular sources")
    makeComponentsAlts(fonts)

    # maybe not needed?
    # print("🤖 Decomposing alts with components")
    # decomposeCoreGlyphs(fonts)

    print("🤖 Removing unicodes from alt glyphs")
    removeAltUnicodes(fonts)

    print("🤖 Fixing accent positions")
    correctAccents(fonts)

    print("🤖 Updating feature code")
    addFeaCode(fonts)

    print("🤖 Copying Designspace file")
    for ds in designspaces:
        shutil.copyfile(ds, prepDir+'/'+os.path.split(ds)[1])

if __name__ == "__main__":
    main()