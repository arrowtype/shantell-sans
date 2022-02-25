"""
    Track out a UFO by adding margin to all glyphs.
"""

from fontParts.world import OpenFont

font = OpenFont("sources/experiments/2022-02-25-tracking-axis-test/shantell--extrabold-tracked.ufo")

for glyph in font:
   glyph.leftMargin = glyph.leftMargin + 10
   glyph.rightMargin = glyph.rightMargin + 10

font.save()