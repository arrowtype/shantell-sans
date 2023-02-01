from coldtype import *

ttf = Font.Cacheable("fonts/Shantell Sans/Desktop/Static/TTF/Shantell_Sans-Normal-SemiBold.ttf")

os2 = ttf.font.ttFont["OS/2"]
glyphSet = ttf.font.ttFont.getGlyphSet()
glyphs = list(glyphSet.keys())

@animation((1080, 1080)
    , tl=Timeline(len(glyphs), fps=12)
    , bg=0
    , release=lambda a: a.export("h264", open=0)
    )
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
