"""
    Removes currently selected glyphs from current font.
    
    Also removes these glyphs from groups, kerning, and components.
    
    Includes template glyphs in selection and removal.
"""

f = CurrentFont()

# copy space-separated glyph names here
#glyphsToRemove = list(f.templateSelectedGlyphNames)
glyphsToRemove = "breveacutecomb brevegravecomb brevehookabovecomb brevetildecomb circumflexacutecomb circumflexgravecomb circumflexhookabovecomb circumflextildecomb ringacutecomb dieresismacroncomb tildemacroncomb dotmacroncomb".split()

try:

    # FONT KEYs -----------------------------------------------

    # clean up the rest of the data
    for glyphName in glyphsToRemove:
        #print(glyphName)
        # remove from keys
        #if glyphName in f:
        if glyphName in f.keys():
            del f[glyphName]
        else:
            continue

    # LAYERS --------------------------------------------------

    for layerName in f.layerOrder:
        layer = f.getLayer(layerName)
        for glyphToRemove in glyphsToRemove:
            if glyphToRemove in layer:
                del layer[glyphToRemove]


    # GLYPH ORDER ---------------------------------------------

    # saving template glyph order
    templateGlyphs = f.templateGlyphOrder

    glyphOrder = f.glyphOrder

    for glyphName in glyphsToRemove:
        if glyphName in glyphOrder:
            glyphOrder.remove(glyphName)
        if glyphName in templateGlyphs:
            templateGlyphs.remove(glyphName) 

    f.glyphOrder = glyphOrder

    # restoring template glyphs
    f.templateGlyphOrder = templateGlyphs

    # KERNING -----------------------------------------------------------

    for glyphName in glyphsToRemove:
        # iterate over all kerning pairs in the font
        for kerningPair in f.kerning.keys():

            # if glyph is in the kerning pair, remove it
            if glyphName in kerningPair:
                del f.kerning[kerningPair]

    # COMPONENTS -------------------------------------------------------

    # iterate over all glyphs in the font
    for glyph in f:

        # skip glyphs which components
        if not glyph.components:
            continue

        # iterate over all components in glyph
        for component in glyph.components:

            # if the base glyph is the glyph to be removed
            if component.baseGlyph in glyphsToRemove:
                # delete the component
                glyph.removeComponent(component)

    # clearing this list so it's not saved...
    glyphsToRemove = []

except ValueError:
    pass