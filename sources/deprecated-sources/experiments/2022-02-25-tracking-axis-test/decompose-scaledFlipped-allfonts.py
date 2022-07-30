"""
    A quick RoboFont script to try decomposing components for all open fonts, if they are scaled or flipped in any open fonts.
"""

scaledFlipped = []
            
def decomposeScaledFlippedComp(glyph):
    if not glyph.components:
        return
    for component in glyph.components:
        if component.transformation[0] != 1 or component.transformation[3] != 1:
            component.decompose()
            
for f in AllFonts():
    for glyph in f:
        if not glyph.components:
            continue
        for component in glyph.components:
            if component.transformation[0] != 1 or component.transformation[3] != 1:
                #component.decompose()
                if glyph.name not in scaledFlipped:
                    scaledFlipped.append((glyph.name,component.baseGlyph))
    
scaledFlipped = set(scaledFlipped)

print(scaledFlipped)

for f in AllFonts():
    for gname,cname in scaledFlipped:
        print(gname, cname)
        for c in f[gname].components:
            if c.baseGlyph == cname:
                print(c)
                print(c.baseGlyph)
                c.decompose()
            