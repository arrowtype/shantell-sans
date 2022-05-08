"""
    This script will...
    1. Copy main & organic sources to new folder, along with designspace files
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources
    4. Add generated alts into kerning groups with their parents, to retain kerning in text
    5. Generate a contextual alternates (calt) feature to rotate through alts in text

    ASSUMPTIONS:
    → kerning groups all match glyph names in them (replacing "." with "_" in .case glyphs)
    → Many more. This is really for the Shantell Sans project only, though it could be adapted for others. 
    → See configuration below.

    USAGE:
    python3 scripts--build/prep-build.py
"""

import os
import shutil
from fontParts.fontshell import RFont as Font
from fontParts.world import *
from random import random

# --------------------------------------------------------
# START configuration

# could do: optimize later (?)
sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
    "irregularLight": "sources/shantell_organic--light.ufo",
    "irregularExtrabold": "sources/shantell_organic--extrabold.ufo",
    "bounceLight": "sources/shantell_bounce--light.ufo",
    "bounceExtrabold": "sources/shantell_bounce--extrabold.ufo",
    "bounceReverseLight": "sources/shantell_reverse_bounce--light.ufo",
    "bounceReverseExtrabold": "sources/shantell_reverse_bounce--extrabold.ufo",
}

# where prepped UFOs are put
prepDir = 'sources/wght_BNCE_IRGL_TRAK--prepped'

# designspaces copied into prepped folder
designspaces = ["sources/shantell_sans-wght_BNCE_IRGL_TRAK.designspace", "sources/shantell_sans-wght_BNCE_IRGL_TRAK--static.designspace"]

# features folder copied into prepped folder
featuresDir = "sources/features/features"

# NOTE: if you really want *all* characters to have alts, use this instead. But it makes the font filesize quite a bit bigger.
# altsToMake = "AÀÁÂÃÄÅĀĂĄǍBCÇĆČDĎEÈÉÊËĒĔĘĚFGĞHIÌÍÎÏĪĬĮİJKLMNÑŃŇOÒÓÔÕÖŌŎŐPQRŔŘSŚŞŠTŤUÙÚÛÜŪŬŮŰŲǓVWXYÝŸZŹŻŽÆØǾĲŁŒΩaàáâãäåāăąǎbcçćčdďeèéêëēĕęěfgğhiìíîïīĭįjklmnñńňoòóôõöōŏőpqrŕřsśşštťuùúûüūŭůűųǔvwxyýÿzźżžßæÞðþẞ"

# letters to make alts for (all letters)
altsToMake = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzßæÞðþẞ"
altsToMake += "ÉéÓóÍíÁáÈèÜüÇçÃãÖöÄäÑñ"
altsToMake += "ЂЄЉЊЋЏБГДЖЗИЛМПУФЦЧШЩЪЫЬЭЮЯѢѪѴҐҔҖҚҜҠҢҤҮҲҶҸҺӀӋӘӶбвгджзиклмнптфцчшщъыьэюяђєљњћџѣѫѵґҕҗқҝҡңҥүұҳҷҹӌӏәөӷ"

# numbers & basic symbols
altsToMake += "0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”‘’"

# some glyphs just need to stick together or they look broken
glyphsToDecompose = "ij oe".split()

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

# total to add to TRAK axis
maxTracking = 500
trackedPath = "shantell_tracked--light.ufo"

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


def removeGlyphs(font, names):
    """
    Removes the glyphs in the list of *names* from the supplied *font*.
    This checks all layers for the glyph, removes the glyph from any
    composite glyphs that use it, removes the glyph from the `glyphOrder`,
    and removes the glyph from the kerning.

    *font* is a font object (Defcon or FontParts)
    *names* is a `list` of glyph names
    """

    for name in names:
        for layer in font.layers:
            if name in layer.keys():
                layer.removeGlyph(name)

    for glyph in font:
        if glyph.components:
            for component in glyph.components:
                if component.baseGlyph in names:
                    glyph.removeComponent(component)

    glyphOrder = font.glyphOrder
    for name in glyphOrder:
        if name in names:
            glyphOrder.remove(name)
    font.glyphOrder = glyphOrder

    for left, right in font.kerning.keys():
        if left in names or right in names:
            del font.kerning[(left, right)]

def clearGuides(font):
    """
    Clears both font level and glyph level guides in a font.

    *font* is a font object (Defcon or FontParts)
    """
    font.clearGuidelines()

    for glyph in font:
        if glyph.guidelines:
            glyph.clearGuidelines()


def makeSourceFontsGlyphCompatible(fonts):
    """
    Compares the glyphs of all *fonts* and removes glyphs that are not
    common to all the provided *fonts*.

    *fonts* is a `list` of font objects (Defcon or FontParts).
    """

    # Get a list of all glyphs in each font, skipping "sparse" sources
    glyphSets = [font.keys() for font in fonts if "sparse" not in font.path]

    # Use set intersection to get all common glyph from each list
    commonGlyphs = set.intersection(*map(set, glyphSets))

    for font in fonts:
        clearGuides(font)
        if "sparse" not in font.path:
            removed = []
            for name in font.keys():
                if name not in commonGlyphs:
                    removed.append(name)
            if len(removed) != 0:
                removeGlyphs(font, removed)

def makeCompatible(fonts):
    """
    Checks all glyphs in *fonts* for compatibility. Removes any glyphs that
    aren't compatible from all of the fonts.

    *fonts* is a `list` of font objects (Defcon or FontParts).

    fontsToCheck assumes to "sparse" / support sources are compatible.
    """

    nonCompatible = []

    fontsToCheck = [font for font in fonts if "sparse" not in font.path]

    for glyph in fontsToCheck[0]:
        for font in fontsToCheck[1:]:
            if glyph.name in font.keys():
                compatibility = glyph.isCompatible(font[glyph.name])
                if not compatibility[0]:
                    nonCompatible.append((glyph.name, str(compatibility)))
            else:
                nonCompatible.append((glyph.name, "Missing in font"))

    for font in fontsToCheck:
        removeGlyphs(font, [name for name, _ in nonCompatible])


# make alts in all fonts
def makeAlts(fonts, numOfAlts=2):
    """
        Make alts for all glyphs in fonts.
        Argument 'numOfAlts' is the number of alts. 
        E.g. Default numOfAlts=2 would result in a, a.alt1, a.alt2, b, b.alt1, b.alt2, etc
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
    print(font) # DEBUGGING
    print(glyph) # DEBUGGING
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
                    try:
                        # look up Yshift of main baseGlyph
                        mainBase = findMainBaseGlyphName(font, g)
                    except IndexError:
                        # if base glyph is simply a zero-width combining accent, pass
                        # e.g. was failing on /belowbrevecmb
                        # TODO: check if /belowbrevecmb is causing or getting any problems
                        pass
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


def extendKerning(fonts,numOfAlts=2):
    """
        Add .alt1 and .alt2 glyphs to kerning groups with defaults.
    """

    # first, copy groups from main font
    # coreGroups = Font(sources["extrabold"]).groups

    for font in fonts:
        # font.groups = coreGroups

        print("\n\n", font.path)

        # make list of all glyphs with any kerning
        kerning = font.kerning.keys()
        kernedGlyphs = set([glyphName for pair in kerning for glyphName in pair])

        # then, add alt glyphs into the groups of default glyphs
        for g in font:
            # get glyph’s base name pre-suffix if it is a generated "alt", but otherwise use the whole name
            # get base name if glyph has suffix .alt1, etc
            if "." in g.name and "alt" in g.name.split(".")[1]:
                glyphBaseName = g.name.split(".")[0] 
            else:
                glyphBaseName = g.name


            # check what kern groups font[glyphBaseName] is in
            kernGroups = [groupName for groupName in font.groups.findGlyph(glyphBaseName) if "kern" in groupName]
            
            for kernGroup in kernGroups:
                if g.name not in font.groups[kernGroup]:
                    font.groups[kernGroup] = font.groups[kernGroup] + (g.name,)

            # handle case if glyph is *not* in a kerning group already

            # if glyph is in no kerning groups yet
            if kernGroups == []:
                # check if glyphBaseName has any kerning
                if glyphBaseName in kernedGlyphs:
                    # make group names, handling .case suffixes
                    kern1 = f'public.kern1.{glyphBaseName.replace(".","_")}'
                    kern2 = f'public.kern2.{glyphBaseName.replace(".","_")}'

                    # make list of glyph plus alts
                    glyphVersionNames = [glyphBaseName] + [glyphBaseName + f".alt{i+1}" for i in range(numOfAlts)]

                    # make list of glyphBaseName plus glyphBaseName.alt1, alt2, etc
                    font.groups[kern1] = [name for name in glyphVersionNames]
                    font.groups[kern2] = [name for name in glyphVersionNames]

        for kern in font.kerning.items():
            newKern = ()
            newKern1 = ()
            newKern2 = ()
            
            # this goes through the glyphs in each item, which each look like (("A", "W"), -10) or (("public.kern1.y", "public.kern2.guillemetright"), 20), etc
            for i, name in enumerate(kern[0]):
                side = i+1

                # if side kern is not a group already...
                if "public.kern" not in name:
                    # if the glyph is not in group(s)...
                    if kernGroups != []:
                        # make new kern with side1 set to group
                        if side == 1:
                            # make new group name, dealing with suffixed glyph names like /slash.case
                            groupName = f'public.kern1.{name.replace(".","_")}'
                            newKern1 = ((groupName, kern[0][1]), kern[1])

                            del font.kerning[kern[0]]

                            font.kerning[newKern1[0]] = newKern1[1]
                        
                        # make new kern with side2 set to group
                        if side == 2:

                            groupName = f'public.kern2.{name.replace(".","_")}'

                            # if a newKern1 was not made
                            try:
                                newKern2 = ((kern[0][0], groupName), kern[1])
                                del font.kerning[kern[0]]

                            # if a newKern1 was made for side 1
                            except (KeyError, IndexError):
                                newKern2 = ((newKern1[0][0], groupName), newKern1[1])
                                del font.kerning[newKern1[0]]

                            font.kerning[newKern2[0]] = newKern2[1]

        font.save()


def generateCalt(glyphNames):
    """
        Generate OpenType calt code
    """

    glyphNames = sorted(glyphNames)

    newline = "\n"

    # avoids setting biggest transformations at the start of words in Irregular/Flux styles
    # paradoxically, it tends to look *more* random to usually rotate through 3 versions per glyph than 4
    # then, the 4th version comes in handy to disrupt potentially repetition in a word like "EXPERIENCE"
    
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



def addFeaCode(fonts, feaPath):
    """
        Add feature code to generated UFOs
    """

    with open(feaPath) as features:
        feaCode = features.read()

    for font in fonts:
        font.features.text = feaCode
        font.save()

# ------------------------------------------
# begin creating tracked UFO below

def decomposeScaledFlippedComp(font):
    """
        Just in case this isn’t already done, decompose any scaled or flipped components.
    """

    for glyph in font:

        if not glyph.components:
            return
        for component in glyph.components:
            if component.transformation[0] != 1 or component.transformation[3] != 1:
                component.decompose()
    
    font.save()


def addEqualMargin(glyph, margin):
    """
        Add equal margin to a given Rglyph object.
    """
    if glyph.width == 0:
        return
    try:
        glyph.leftMargin = glyph.leftMargin + margin
        glyph.rightMargin = glyph.rightMargin + margin
    except TypeError:
        glyph.width = glyph.width + (margin*2)


def correctComponents(font,glyph, margin):
    """
        Corrects components for a given margin
    """
    if not glyph.components:
        return
    for component in glyph.components:
        if font[component.baseGlyph].width != 0:
            component.moveBy((-margin, 0))


def makeTrackedUFO(font, tracking):
    """
        Take in a font object and add tracking to all glyphs.
    """

    for glyph in font:

        margin = tracking/2

        addEqualMargin(glyph, margin)

        # move component left by margin amount
        correctComponents(font,glyph, margin)
    
    font.save(prepDir + '/' + trackedPath)


# end creating tracked UFO
# ------------------------------------------


def main():

    # The setup

    if os.path.exists(prepDir):
        shutil.rmtree(prepDir,ignore_errors=True)

    # ONLY DO THE FOLLOWING IF YOU WANT TO COMPLETELY SHIFT/CHANGE BOUNCY STYLES
    # print("🤖 Resetting bounce randomization in sources")
    # resetBounces()

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir() 
    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.DS_Store' not in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    # The sausage making

    print("🤖 Making source fonts compatible (removing unique glyphs, etc)")
    makeSourceFontsGlyphCompatible(fonts)
    makeCompatible(fonts)

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
            shiftGlyphs(font, factor=0.75) # factor 0.75 makes moves of up to 75 units
    
    # split into separate loop so reverse sources always go second
    for font in fonts:
        if "reverse_bounce" in font.path:
            print("reverse bounces for ", font.path)
            shiftGlyphs(font, factor=-0.75) # factor -0.75 makes moves of up to -75 units

    # interpolate alts in irregular fonts
    print("🤖 Interpolating organic alts")

    # Dumb setup. Will it work?
    interpolateAlts([f for f in fonts if "shantell--light" in f.path][0], [f for f in fonts if "organic--light" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--extrabold" in f.path][0], [f for f in fonts if "organic--extrabold" in f.path][0], altsMadeForList)

    # yes, this is needed twice. Once to make shifting work well, then again to make irregular sources compatible again after interpolation
    print("🤖 Making composed alts point to alt components – repeating to fix irregular sources")
    makeComponentsAlts(fonts)

    print("🤖 Removing unicodes from alt glyphs")
    removeAltUnicodes(fonts)

    print("🤖 Fixing accent positions")
    correctAccents(fonts)
    
    print("🤖 Tying alts to default glyph kerning")
    extendKerning(fonts)

    print("🤖 Generating calt feature")
    generateCalt(altsMadeForList)

    print("🤖 Updating feature code")
    addFeaCode(fonts, "sources/features/features.fea")

    print("🤖 Copying Designspace file")
    for ds in designspaces:
        shutil.copyfile(ds, prepDir+'/'+os.path.split(ds)[1])

    print("🤖 Copying Features folder")
    shutil.copytree(featuresDir, prepDir + '/' + os.path.split(featuresDir)[1])

    print("🤖 Sorting fonts")
    sortGlyphOrder(fonts)

    print("🤖 Decompose scaled or flipped components")
    for font in fonts:
        decomposeScaledFlippedComp(font)

    print("🤖 Making tracked font")
    for font in fonts:
        if "light" in font.path and "bounce" not in font.path:
            makeTrackedUFO(font, maxTracking)


if __name__ == "__main__":
    main()
