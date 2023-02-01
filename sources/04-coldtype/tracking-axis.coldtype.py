from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

VERSIONS = {
    "latin": dict(text="SPACING", fontSize=225),
    "cyrillic": dict(text="ТИПОГРАФИЯ", fontSize=160)
} #/VERSIONS

@animation((1920, 720), timeline=Timeline(100), fmt="png", bg=0.94, release=lambda a: a.export("h264", open=0))
def spacing_ƒVERSION(f):
    def showMetrics(p:P):
        guide = (P()
            .rect(f.a.r.take(p.ambit().h, "CY").inset(-10, 0))
            .outline(4)
            .f(.74))
        
        return P(guide, p)

    return (
        StSt(__VERSION__["text"], fnt, __VERSION__["fontSize"]
            , wght=f.e("eeio", 1, rng=(1, 0)))
            .align(f.a.r)
            .f(0)
            .ch(showMetrics)
            .t(0, 120),
        StSt(__VERSION__["text"], fnt, __VERSION__["fontSize"]
            , wght=f.e("eeio", 1, rng=(1, 0))
            , SPAC=f.e("sio", 2, rng=(1, 0)))
            .align(f.a.r)
            .f(0)
            .ch(showMetrics)
            .t(0, -120))
