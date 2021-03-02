"""
    This script will...
    1. Copy main & organic sources to new folder
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources

    # TODO
        - [x] remove unicodes from alts
        - [x] dont mess up component glyphs in the shifted alts (shift components along with bases)
            - [x] figure out how to also cover ogonek (not working somehow) and single-component glyphs like oslash and lslash
        - [x] restrict this to *only* make shifted alts for a core character set (maybe ASCII?) – make this configurable with a list of characters
            - [x] decide what accented characters to add
        - [x] generate fresh calt feature code to make all alts work
        - [x] copy designspaces into prep folder
        - [x] fix alignment of accents in organic/irregular glyphs – probably reattach to anchors
        - [ ] split "sources" dict into core sources vs generated sources

        Kerning/repeatability
        - Does a typeface build need to be repeatable? That’s a philosophical question ... is it generally more useful if repeatable? Probably yes.
        - That means that This script probably should be a build script used *every time*, but only something used once, or for new glyphs.
            - [x] Probably, the generated UFOs should get a lib entry of shifted glyphs / transformations, and these could be repeated during this build.
            - [x] check for recorded bounces before generating random new one
                - [x] save to main font’s lib?
                - [x] look in main font for moveY, then apply to bounce font
            - [x] There also probably needs to be a way to record interpolations - ACTUALLY, this is already currently hard-coded to 0.1 and 0.66
        - [ ] first, extend kerning groups to include all .alt1 and .alt2 glyphs with default glyphs - CRITICAL for kerning to work AT ALL, e.g. `Y.alt2 o y.alt1 o.alt2`
        - This would also allow kerning exceptions to persist between builds.
            - In this case, you need a way to record which kerns have been overridden versus which are just outdated.
            - This could be a separate script which you run on saving the bouncy / irregular sources:
                - [ ] First, do a manual test: are kerning overrides in bouncy sources good?
                    - kerning orders: alt2_default, default_alt1, alt1_alt2
                - [ ] check kerning vs normal, and record new diffs in baseFont lib
                
            - [ ] each time fonts are generated, check kerning overrides, and bring those in
                
            - This *should, in theory* allow new kerns to be introduced, where they were previously overridden 
            - Overridden kerns should be kept deliberately sparse, to keep things clean overall

        Maybe??
        - [x] try a bouncy axis that can before 0 in the middle, but bounce up *or* down, to allow for a "wavy" animation
        - [ ] figure out best sequence for up/down variation
        - [x] re-fix accent attachment with this new postivie/negative bounce system

        Also
        - [ ] Link to this script at https://github.com/googlefonts/ufo2ft/issues/437 once the repo is public

        Maybe?
        - [x] build in feature copier? (currently, you have to separate copy in the features  )

        # TODO: generate calt feature code to catch all glyphs with .alts, which would be:
            - .case punctuation
            - fractional figures

        - [x] probably, you should make sure to SKIP shifting to numr/dnom figures, or it will break fractions
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

# TODO: split "sources" dict into core sources vs generated sources
sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
    "quirkLight": "sources/shantell_organic--light.ufo",
    "quirkExtrabold": "sources/shantell_organic--extrabold.ufo",
    "bounceLight": "sources/shantell_bounce--light.ufo",
    "bounceExtrabold": "sources/shantell_bounce--extrabold.ufo",
    "bounceReverseLight": "sources/shantell_reverse_bounce--light.ufo",
    "bounceReverseExtrabold": "sources/shantell_reverse_bounce--extrabold.ufo",
}

# where prepped UFOs are put
# prepDir = 'sources/wght_bnce_flux--bnce_rev--prepped'
prepDir = 'sources/wght_bnce_flux--bnce_rev--4_alts_b--prepped'

# designspaces copied into prepped folder
designspaces = ["sources/shantell-wght_BNCE_IRGL--reverse_bounce.designspace", "sources/shantell-wght_BNCE_IRGL--reverse_bounce--static.designspace"]

# letters to make alts for (all letters)
altsToMake = "AÀÁÂÃÄÅĀĂĄǍBCÇĆČDĎEÈÉÊËĒĔĘĚFGĞHIÌÍÎÏĪĬĮİJKLMNÑŃŇOÒÓÔÕÖŌŎŐPQRŔŘSŚŞŠTŤUÙÚÛÜŪŬŮŰŲǓVWXYÝŸZŹŻŽÆØǾĲŁŒΩaàáâãäåāăąǎbcçćčdďeèéêëēĕęěfgğhiìíîïīĭįjklmnñńňoòóôõöōŏőpqrŕřsśşštťuùúûüūŭůűųǔvwxyýÿzźżžßæÞðþẞ"

# numbers & basic symbols
altsToMake += "0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”‘’"

# some glyphs just need to stick together or they look broken
glyphsToDecompose = "ij oe".split()

# feature code to be inserted into generated UFOs
feaCode = """\
languagesystem DFLT dflt;
languagesystem latn dflt;

include(../features/features/common.fea);
include(../features/features/frac.fea);
include(../features/features/case.fea);
include(../features/features/numr_dnom_supr_infr.fea);
include(./cycle-calt.fea) # this is generated
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
    hyphen.line hyphen_line.3 hyphen_line.4 hyphen_line.5 hyphen_line.6 hyphen_line.7 hyphen_line.8 hyphen_line.9 hyphen_line.10 hyphen_line.11 hyphen_line.12 hyphen_line.13 hyphen_line.14 hyphen_line.15 hyphen_line.16 hyphen_line.17 hyphen_line.18 hyphen_line.19 hyphen_line.20 hyphen_line.21 hyphen_line.22 hyphen_line.23 hyphen_line.24 hyphen_line.25 hyphen_line.26 hyphen_line.27 hyphen_line.28 hyphen_line.29 hyphen_line.30 hyphen_line.31 hyphen_line.32 hyphen_line.33 hyphen_line.34 hyphen_line.35 hyphen_line.36 hyphen_line.37 hyphen_line.38 hyphen_line.39 hyphen_line.40 hyphen_line.41 hyphen_line.42 hyphen_line.43 hyphen_line.44 hyphen_line.45 hyphen_line.46 hyphen_line.47 hyphen_line.48 hyphen_line.49 hyphen_line.50\
".split()

# END configuration
# --------------------------------------------------------

# add just the basic upper & lowercase (used later in the calt code generator)
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = "abcdefghijklmnopqrstuvwxyz"

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

        # make bounce UFOs
        if name in ["light","extrabold"]:
            bounceCopy = prepDir+'/'+os.path.split(sources[f"bounce{name.title()}"])[1]
            if not os.path.exists(bounceCopy):
                shutil.copytree(source, bounceCopy)

        # make bounce-reverse UFOs
        if name in ["light","extrabold"]:
            bounceReverseCopy = prepDir+'/'+os.path.split(sources[f"bounceReverse{name.title()}"])[1]
            if not os.path.exists(bounceReverseCopy):
                shutil.copytree(source, bounceReverseCopy)

def sortGlyphOrder(fonts):
    """
    Sorts all fonts in the list of *fonts* to have a common sort order.

    *fonts* is a `list` of font objects (Defcon or FontParts).
    """
    for font in fonts:
        newGlyphOrder = font.naked().unicodeData.sortGlyphNames(font.glyphOrder, sortDescriptors=[dict(type="cannedDesign", ascending=True, allowPseudoUnicode=True)])

        # Trick here to put the .notdef first, as the cannedDesign sort puts it
        # last, and it must be the first glyph in a font.
        newGlyphOrder.insert(0, newGlyphOrder.pop())
        font.glyphOrder = newGlyphOrder

        font.save()

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

    # print(" ".join(altsToMakeGlyphNames))

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


def makeBounce(font, glyph, randomLimit=100, minShift=50, factor=1):
    """
        Determine pseudo-random bounce, then move the glyph
    """

    moveY=0

    # alt 1 → shift downwards
    if 'alt1' in glyph.name and glyph.name.split(".")[0]:
        moveY = round((randomLimit-minShift) * random() + minShift) * -1 * factor
        glyph.moveBy((0,moveY))

    # alt 2 → shift upwards
    if 'alt2' in glyph.name and glyph.name.split(".")[0]:
        moveY = round((randomLimit-minShift) * random() + minShift) * factor
        glyph.moveBy((0,moveY))

    # alt 3 or more → shift up or down by up to 66% (not necessarily needed)
    if 'alt' in glyph.name and \
        glyph.name.split(".")[0] and\
        'alt1' not in glyph.name and \
        'alt2' not in glyph.name:
        moveY = round((randomLimit-minShift) * random() + (minShift*0.66)) * positiveOrNegative() * factor # reduce shift other alt glyphs
        glyph.moveBy((0,moveY))

    # non-alt glyphs → shift up or down by up to 20%
    if 'alt' not in glyph.name and glyph.name:
        # moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative() * factor
        moveY = round((randomLimit-minShift) * random() + (minShift*0.2)) * positiveOrNegative() * factor # mostly remove minShift for default glyphs, so more are in the middle
        glyph.moveBy((0,moveY))

    if moveY == 0:
        print("moveY = 0:")
        print("\t",font.path)
        print("\t",glyph.name)

    return moveY


def recordBounce(font, glyphName, moveY):
    """
        Record amount of Y-axis movement for a given glyph in the font lib.
    """
    try:
        font.lib["com.arrowtype.glyphBounces"][glyphName] = moveY
    except KeyError:
        font.lib["com.arrowtype.glyphBounces"] = {}
        font.lib["com.arrowtype.glyphBounces"][glyphName] = moveY


def resetBounces():
    """
        ONLY USE if you want to blow up the previously-set bounce values.

        Only use during active design, not afterward when repeating the build to refine/fix issues.
    """

    light = Font(sources["light"])
    light.lib["com.arrowtype.glyphBounces"].clear()
    light.save()

    extrabold = Font(sources["extrabold"])
    extrabold.lib["com.arrowtype.glyphBounces"].clear()
    extrabold.save()


def shiftGlyphs(font,randomLimit=100,minShift=50,factor=1):
    """
        Shift glyphs in Bouncy sources.
    """

    print(font.path)
    print("factor is ", factor)

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

    if "bounce" in font.path:
        # determine whether style is light or extrabold bouncy, then open that base font
        if "light" in font.path:
            baseFont = Font(sources["light"])
        elif "extrabold" in font.path:
            baseFont = Font(sources["extrabold"])

        # print(baseFont)

        for g in font:
            if g.name not in glyphsToNotShift and len(g.components) == 0:

                moveY = 0

                try:
                    # try: look up bounce dict in the core light/extrabold font, use in this font
                    moveY = baseFont.lib["com.arrowtype.glyphBounces"][g.name] * factor
                    g.moveBy((0,moveY))
                except KeyError:
                    # except KeyError: generate bounce value and add to core light/extrabold font
                    moveY = makeBounce(font, g, randomLimit, minShift, factor)
                    recordBounce(baseFont, g.name, moveY)

                # record shift in the glyph’s lib for later use
                g.lib['com.arrowtype.yShift'] = moveY

        # correct positioning of base glyphs in composed glyphs
        for g in font:

            if len(g.components) >= 1 and g.name.split(".")[0] not in glyphsToNotShift and g.name not in glyphsToNotShift:

                try:
                    # look up Yshift of main baseGlyph
                    mainBase = findMainBaseGlyphName(font, g)
                    baseShift = font[mainBase].lib['com.arrowtype.yShift']

                    # in multi-component glyphs, shift accents to match bases
                    if len(g.components) > 1:
                        for c in g.components:
                            if c.baseGlyph is not mainBase:
                                c.moveBy((0,baseShift))
                        # move glyph to normal position to "reset" it
                        g.moveBy((0,-baseShift))

                    #  correct single-component glyphs like oslash, lslash
                    else:
                        for c in g.components:
                            if c.baseGlyph is mainBase:
                                c.moveBy((0,-baseShift))
                except KeyError:
                    # if base glyph isn’t shifted, lib['com.arrowtype.yShift'] will fail
                    pass

                # move full glyph again # BUT WAIT, this just breaks it? ... does it need all components moved separately, rather than the whole thing moved?
                try:
                    moveY = baseFont.lib["com.arrowtype.glyphBounces"][g.name] * factor
                    g.moveBy((0,moveY))
                except KeyError:
                    moveY = makeBounce(font, g, randomLimit, minShift, factor)
                    recordBounce(baseFont, g.name, moveY)

                g.lib['com.arrowtype.yShift'] = moveY

                # print(g.name, moveY)


        font.save()
        baseFont.save()


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

            # interpolate alt2 33% towards organicFont glyph
            factor = 0.33
            # print(f'interpolating {g.name}…')
            organicFont[f'{g.name}.alt2'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            try:
                # IF USING 3 alts (4 total versions of each glyph)
                # interpolate alt2 66% towards organicFont glyph
                factor = 0.66
                # print(f'interpolating {g.name}…')
                organicFont[f'{g.name}.alt3'].interpolate(factor, normalFont[g.name], organicFont[g.name])
            except:
                pass

    organicFont.save()


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


def extendKerning(fonts):
    """
        Add .alt1 and .alt2 glyphs to kerning groups with defaults.
    """

    # first, copy groups from main font
    # coreGroups = Font(sources["extrabold"]).groups

    for font in fonts:
        # font.groups = coreGroups

        # print("\n\n", font.path)

        # then, add alt glyphs into the groups of default glyphs
        for g in font:
            baseName = g.name.split(".")[0]

            # check what kern1 group font[baseName] is in
            kernGroups = [groupName for groupName in font.groups.findGlyph(baseName) if "kern" in groupName]
            
            for kernGroup in kernGroups:
                if g.name not in font.groups[kernGroup]:
                    font.groups[kernGroup] = font.groups[kernGroup] + (g.name,)

                    # print(g.name, end=" ")
                    # print(font.groups.findGlyph(g.name), end=" | ")

        font.save()


def generateCalt(glyphNames):
    """
        Generate OpenType calt code
    """

    # print(f"making calt code for:")
    # print(f"{glyphNames}")

    glyphNames = sorted(glyphNames)

    # for 3 alts / 4 versions for glyph
    # calt = f"""\
    # feature calt {{
    #     @randomCycle1 = [{" ".join(name + '     ' for name in glyphNames)}]; # default
    #     @randomCycle2 = [{" ".join(name + '.alt1' for name in glyphNames)}]; # alt1
    #     @randomCycle3 = [{" ".join(name + '.alt2' for name in glyphNames)}]; # alt2
    #     @randomCycle4 = [{" ".join(name + '.alt3' for name in glyphNames)}]; # alt3
        
    #     # avoids setting biggest transformations at the start of words in Irregular/Flux styles
    #     sub @randomCycle1 by @randomCycle4;
    #     sub @randomCycle4 @randomCycle4' by @randomCycle2;
    #     sub @randomCycle2 @randomCycle4' by @randomCycle1;
    #     sub @randomCycle1 @randomCycle4' by @randomCycle3;
    # }} calt;
    # """

    newline = "\n"

    # for 2 alts / 3 versions for glyph
    calt = f"""\
feature calt {{

    @uppercaseMid = [{" ".join(name + '     ' for name in uppercase)}];
    @uppercaseLow = [{" ".join(name + '.alt1' for name in uppercase)}];
    @uppercaseHigh = [{" ".join(name + '.alt2' for name in uppercase)}];

    @lowercaseMid = [{" ".join(name + '     ' for name in lowercase)}];
    @lowercaseLow = [{" ".join(name + '.alt1' for name in lowercase)}];
    @lowercaseHigh = [{" ".join(name + '.alt2' for name in lowercase)}];

    @mid = [{" ".join(name + '     ' for name in glyphNames)}];
    @low = [{" ".join(name + '.alt1' for name in glyphNames)}];
    @high = [{" ".join(name + '.alt2' for name in glyphNames)}];
    
    # avoids setting biggest transformations at the start of words in Irregular/Flux styles
    sub @mid by @high;
    sub @high @high' by @mid;
    sub @mid @high' by @low;

    # basic order: high mid low high mid low - etc

    # prevent alt2 (high) from appearing three after alt2 uppercase
    {f"{newline}    ".join([f"sub {c}.alt2 @uppercaseMid @uppercaseLow {c}.alt2' by {c}.alt3;" for c in uppercase])}
    
    # prevent default (mid) from appearing three after default uppercase
    {f"{newline}    ".join([f"sub {c} @uppercaseLow @uppercaseHigh {c}' by {c}.alt3;" for c in uppercase])}
    
    # prevent alt1 (low) from appearing three after alt1 uppercase
    {f"{newline}    ".join([f"sub {c}.alt1 @uppercaseHigh @uppercaseMid {c}.alt1' by {c}.alt3;" for c in uppercase])}
    
    # prevent alt2 (high) from appearing three after alt2 lowercase
    {f"{newline}    ".join([f"sub {c}.alt2 @lowercaseMid @lowercaseLow {c}.alt2' by {c}.alt3;" for c in lowercase])}
    
    # prevent default (mid) from appearing three after default lowercase
    {f"{newline}    ".join([f"sub {c} @lowercaseLow @lowercaseHigh {c}' by {c}.alt3;" for c in lowercase])}
    
    # prevent alt1 (low) from appearing three after alt1 lowercase
    {f"{newline}    ".join([f"sub {c}.alt1 @lowercaseHigh @lowercaseMid {c}.alt1' by {c}.alt3;" for c in lowercase])}

}} calt;
    """

    with open(f"{prepDir}/cycle-calt.fea", "w") as file:
        file.write(calt)

    # print(calt)



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

    # ONLY DO THE FOLLOWING IF YOU WANT TO COMPLETELY SHIFT BOUNCY STYLES
    # print("🤖 Resetting bounce randomization in sources")
    # resetBounces()

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir()

    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    # The sausage making

    print("🤖 Decomposing digraphs")
    decomposeDigraphs(fonts)

    print("🤖 Making alts")
    altsMadeForList = makeAlts(fonts, numOfAlts=3)

    print("🤖 Making composed alts point to alt components")


    makeComponentsAlts(fonts)

    

    # shift alts in bounce fonts
    print("🤖 Shifting bouncy alts")
    for font in fonts:
        if "bounce" in font.path and "reverse_bounce" not in font.path:
            shiftGlyphs(font, factor=1.5) # factor 1.5 makes moves of up to 150 units
    
    # split into separate loop so reverse sources always go second
    for font in fonts:
        if "reverse_bounce" in font.path:
            print("reverse bounces for ", font.path)
            shiftGlyphs(font, factor=-1.5) # factor -1.5 makes moves of up to -150 units

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
    
    print("🤖 Tying alts to default glyph kerning")
    extendKerning(fonts)

    print("🤖 Generating calt feature")
    generateCalt(altsMadeForList)

    print("🤖 Updating feature code")
    addFeaCode(fonts)

    print("🤖 Copying Designspace file")
    for ds in designspaces:
        shutil.copyfile(ds, prepDir+'/'+os.path.split(ds)[1])

    print("🤖 Sorting fonts")
    sortGlyphOrder(fonts)

if __name__ == "__main__":
    main()
