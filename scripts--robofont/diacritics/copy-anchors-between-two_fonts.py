"""
    Copy anchors from a source font to a destination font.

    Based partly on https://forum.robofont.com/topic/862/how-to-copy-anchors-from-one-font-to-another
"""

from vanilla.dialogs import *

# get source and destination fonts
srcFont = OpenFont(getFile("Select Source Font", allowsMultipleSelection=False, fileTypes=["ufo"])[0], showInterface=False)
dstFont = OpenFont(getFile("Select Destination Font", allowsMultipleSelection=False, fileTypes=["ufo"])[0], showInterface=False)

print(srcFont)

# iterate over selected glyphs in the source font
for glyphName in dstFont.keys():

    # get the source glyph
    try:
        srcGlyph = srcFont[glyphName]
    except:
        print(f"{glyphName} not in source font")
        continue

    # if the glyph doesn't have any anchors, skip it
    if not len(srcGlyph.anchors):
        continue

    # get the destination glyph
    dstGlyph = dstFont[glyphName]

    # iterate over all anchors in the source glyph
    for anchor in srcGlyph.anchors:
        # check whether the anchors are already there to avoid duplicates
        if anchor.name not in [a.name for a in dstGlyph.anchors]:
            # copy anchor to destination glyph
            dstGlyph.appendAnchor(anchor.name, (anchor.x, anchor.y))

dstFont.save()

# done!