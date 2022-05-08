"""
    Track out a UFO by adding margin to all glyphs.
"""

from fontParts.world import OpenFont

# the generated "tracked" source must match the other axis defaults
font = OpenFont("sources/experiments/2022-02-25-tracking-axis-test/shantell--light.ufo")

def decomposeScaledFlippedComp(glyph):
    if not glyph.components:
        return
    for component in glyph.components:
        if component.transformation[0] != 1 or component.transformation[3] != 1:
            component.decompose()

def addEqualMargin(glyph, margin):
    if glyph.width == 0:
        return
    try:
        glyph.leftMargin = glyph.leftMargin + margin
        glyph.rightMargin = glyph.rightMargin + margin
    except TypeError:
        glyph.width = glyph.width + (margin*2)
    # except Exception as e: 
    #     print(glyph.name, "\t\t", repr(e))

def correctComponents(font,glyph, margin):
    if not glyph.components:
        return
    for component in glyph.components:
        if font[component.baseGlyph].width != 0:
            component.moveBy((-margin, 0))

for glyph in font:

    margin = 500

    decomposeScaledFlippedComp(glyph)

    addEqualMargin(glyph, margin)

    # move component left by margin amount
    correctComponents(font,glyph, margin)

font.save("sources/experiments/2022-02-25-tracking-axis-test/shantell_tracked--light.ufo")
