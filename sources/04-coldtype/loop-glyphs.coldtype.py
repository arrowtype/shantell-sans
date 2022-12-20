from coldtype import *

ttf = Font.Find("ShantellSans-Normal-Bold", "sources")

os2 = ttf.font.ttFont["OS/2"]
glyphSet = ttf.font.ttFont.getGlyphSet()
glyphs = list(glyphSet.keys())

@animation((1920, 1080), tl=Timeline(len(glyphs), 10), bg=0)
def loopGlyphs(f):
    glyphKey = glyphs[f.i]
    glyph = glyphSet[glyphKey]
    
    return (P(
        P().glyph(glyph, glyphSet)
            .data(frame=Rect(0, 0, glyph.width, os2.sCapHeight))
            .f(1)
            .align(f.a.r)
            .scale(0.5)
            .scaleToRect(f.a.r.inset(100), shrink_only=True, preserveAspect=True),
        StSt("{:04d}".format(f.i), ttf, 60)
            .f(1)
            .align(f.a.r.inset(100), "SW", tx=0)))