"""
    A script to prep only the wght 300 and 800 sources, for a simple build to proof the core of the typeface.
    
    This script will...
    1. Copy main & organic sources to new folder, along with designspace files
    2. Check for compatibility, and try to remove non-compatible glyphs to make a build work

    USAGE:
    python3 scripts--build/prep-build-basic.py
"""

import os
import shutil
from fontParts.fontshell import RFont as Font
from fontParts.world import *
from random import random

# --------------------------------------------------------
# START configuration

sources = {
    "light": "sources/shantell--light.ufo",
    "extrabold": "sources/shantell--extrabold.ufo",
}

# where prepped UFOs are put
prepDir = 'sources/wght--prepped'

# designspaces copied into prepped folder
designspaces = ["sources/shantell-300_800.designspace", "sources/shantell-300_800--static.designspace"]

# features folder copied into prepped folder
featuresDir = "sources/features/features"

# END configuration
# --------------------------------------------------------

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


def addFeaCode(fonts, feaPath):
    """
        Add feature code to generated UFOs
    """

    with open(feaPath) as features:
        feaCode = features.read()

    for font in fonts:
        font.features.text = feaCode
        font.save()


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

    print("🤖 Updating feature code")
    addFeaCode(fonts, "sources/features/features.fea")

    print("🤖 Copying Designspace file")
    for ds in designspaces:
        shutil.copyfile(ds, prepDir+'/'+os.path.split(ds)[1])

    print("🤖 Copying Features folder")
    shutil.copytree(featuresDir, prepDir + '/' + os.path.split(featuresDir)[1])

    print("🤖 Sorting fonts")
    sortGlyphOrder(fonts)


if __name__ == "__main__":
    main()
