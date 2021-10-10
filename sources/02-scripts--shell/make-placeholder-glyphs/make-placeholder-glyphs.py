"""
    Goal: add all required glyphs to Shantell Sans now, with placeholder glyphs, to allow simpler collaboration via GitHub (with fewer conflicts due to added glyphs).

    1. Takes in GF GlyphSet files as data: Latin Core, Latin Plus, Cyrillic Plus, and Cyrillic Locl
    2. Makes a list of unicodes for Latin, and one for Cyrillic (so we can mark it with another color), one for Latin without Unicodes, and one for Cyrillic without Unicodes
    3. Converts Unicode values, if needed
    4. Adds glyphs to font with unicodes, if not yet in the font
    5. Copies (and scales) glyphs from another font, to make things simpler to see & draw. Maybe Roboto Thin? (Check licensing first).
    6. Sets AGL-compatible glyph names, borrowing code from this script

    QUESTIONS:
    - Are smallcaps any more used in Cyrillic than Latin? If not, we should probably not add them. They won’t be added in the Latin. 
        - NOTE: I’m excluding them for now.
        - NOTE: I’m also excluding ".lf" numbers for now, as the fonts already have lining figures by default.
"""

import os
from fontParts.fontshell import RFont as Font
from glyphNameFormatter.reader import uni2name
import subprocess

directory = '/Users/stephennixon/type-repos/shantell-sans/sources/02-scripts--shell/make-placeholder-glyphs/glyphSets'

# go through glyphset files, make a dict of all unicodes required
glyphsRequired = {}
for subpath in os.listdir(directory):
    if subpath.endswith(".nam"):
        path = os.path.join(directory, subpath)
        # print(path)

        glyphsRequired[subpath] = []

        with open(path) as f:
            lines = f.readlines()

            for line in lines:
                if line.startswith("#"):
                    continue
                if line.startswith("0x"):
                    unicodeInt = int(line[0:6],0)
                    glyphsRequired[subpath].append(unicodeInt)

                else:
                    if ".sc" not in line and ".lf" not in line:
                        glyphsRequired[subpath].append(line.replace(" ","").replace("\n",""))


# open fonts
sources = '/Users/stephennixon/type-repos/shantell-sans/sources'
fonts= []
for subpath in os.listdir(sources):
    if subpath.endswith('.ufo'):
        path = os.path.join(sources, subpath)
        fonts.append(Font(path))

# path of a font to copy placeholder glyphs from
fontToCopy = Font("/Users/stephennixon/type-repos/shantell-sans/sources/02-scripts--shell/make-placeholder-glyphs/RobotoFlex-opsz8-wght100.ufo")

# build dict of names to unicodes, so you can copy glyph by unicodes later
fontToCopyUnicodes = {}
for g in fontToCopy:
    try:
        fontToCopyUnicodes[g.unicodes[0]] = g.name
    except IndexError:
        continue

# get scale if fontToCopy has different UPM (it does)
relativeScale = fonts[0].info.capHeight / fontToCopy.info.capHeight

# check if unicodes exist; if not, add them
for font in fonts:
    print(font)
    unicodesInFont = [font[name].unicodes[0] for name in font.keys() if font[name].unicodes is not ()]

    unicodesToAdd = []
    nonUnicodesToAdd = []

    # assigning mark colors to each glyphSet
    markColors = {
            "GF-cyrillic-plus_unique-glyphs.nam": (.5,0,1,0.15),
            "GF-cyrillic-plus-locl_unique-glyphs.nam": (.5,0,1,0.3),
            "GF-latin-core_unique-glyphs.nam": (1,.8,0,0.15),
            "GF-latin-plus_unique-glyphs.nam": (1,.8,0,0.3)
            }

    for glyphSet in glyphsRequired:
        for requiredGlyph in glyphsRequired[glyphSet]:
            # print(requiredGlyph)
            if type(requiredGlyph) is int:
                if requiredGlyph not in unicodesInFont:

                    glyphName = uni2name.get(requiredGlyph)
                    # print(glyphName)
                    if glyphName == None:
                        glyphName = "uni"+str(f'{requiredGlyph:0>4X}')

                    if glyphName not in font.keys():
                        glyph = font.defaultLayer.newGlyph(glyphName)
                        glyph.unicodes = (requiredGlyph,)

            if type(requiredGlyph) is str:
                if requiredGlyph not in font.keys():
                    glyph = font.defaultLayer.newGlyph(requiredGlyph)
                    # mark with color per glyphSet

            glyph.mark = markColors[glyphSet]

            # set glyph to non-exporting, so it doesn’t save into font builds until we actually draw it
            font.lib["public.skipExportGlyphs"].append(glyph.name)

            # ----------------------------------------------
            # copy in placeholder glyphs where possible

            layer = font.getLayer(font.defaultLayerName)

            try:
                glyphToCopy = fontToCopy[fontToCopyUnicodes[glyph.unicodes[0]]]

            except (IndexError, KeyError):
                try:
                    glyphToCopy = fontToCopy[glyph.name]
                except KeyError:
                    print(f"Can’t find glyph {glyph.name} in font to copy")

                    layer[glyph.name] = font["periodcentered"]
                    continue

            # edit this so our font’s glyph name doesn’t break
            glyphToCopy.name = glyph.name

            # prevent it carrying over components for the placeholder, which look weird
            glyphToCopy.decompose()

            glyphName = glyph.name

            layer[glyph.name] = glyphToCopy.copy()

            # scale glyph to fit new UPM
            try:
                layer[glyph.name].scaleBy(relativeScale)
                layer[glyph.name].width = layer[glyph.name].width * relativeScale
                # repeat again, if mark from roboto is copying over?
                layer[glyph.name].mark = markColors[glyphSet]
            except KeyError:
                pass
    
    


    font.save()

    # normalize UFO to avoid git noise
    subprocess.run(['ufonormalizer',font.path,'-m'])

