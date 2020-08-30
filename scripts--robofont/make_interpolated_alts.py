"""
    Given two compatible fonts, f1 & f2:
    - both fonts get two alts for each glyph
    - f2 keeps default of each main glyph
    - f2’s alts are interpolated to f1 at 33% & 66%

    See https://robofont.com/documentation/building-tools/toolspace/scripts/scripts-interpolation/#interpolating-between-two-masters
"""

# get main font, which will remain normal
mainFontPath = getFile("Select UFOs", allowsMultipleSelection=False, fileTypes=["ufo"])
f1 = OpenFont(mainFontPath, showInterface=True)

# get secondary font, which will get interpolations
secondaryFontPath = getFile("Select UFOs", allowsMultipleSelection=False, fileTypes=["ufo"])
f2 = OpenFont(secondaryFontPath, showInterface=True)

# start by making all the alts
def makeAlts(font):
    constructionTxt = ''

    for g in font:

        constructionTxt += f'''
            {g.name}.alt1 = {g.name}
            {g.name}.alt2 = {g.name}\
        '''

    constructions = ParseGlyphConstructionListFromString(constructionTxt)

    for construction in constructions:

        # build a construction glyph
        constructionGlyph = GlyphConstructionBuilder(construction, font)

        # if the construction for this glyph was preceded by `?`
        # and the glyph already exists in the font, skip it
        if constructionGlyph.name in font and constructionGlyph.name in ignoreExisting:
            continue

        # get the destination glyph in the font
        glyph = font.newGlyph(constructionGlyph.name, clear=True)

        # draw the construction glyph into the destination glyph
        constructionGlyph.draw(glyph.getPen())

        # copy construction glyph attributes to the destination glyph
        glyph.name = constructionGlyph.name
        glyph.unicode = constructionGlyph.unicode
        glyph.width = constructionGlyph.width
        glyph.markColor = 0, 0, 0, 0.5

makeAlts(f1)
makeAlts(f2)

for g in f2:
    if 'alt' not in g.name:
        f1g = f1[g.name]

        # interpolate gOneThird and move to f2[f'{g.name}.alt1']
        factor = 0.33
        print(f'interpolating {g.name}…')
        f2[f'{g.name}.alt1'].interpolate(factor, f1[g.name], f2[g.name])

        # interpolate gTwoThirds and move to f2[f'{g.name}.alt2']
        factor = 0.66
        print(f'interpolating {g.name}…')
        f2[f'{g.name}.alt2'].interpolate(factor, f1[g.name], f2[g.name])







