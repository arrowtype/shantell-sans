from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

txt, fontSize = "SPACING", 225
#txt, fontSize = "ТИПОГРАФИЯ", 180

@animation((1920, 720), timeline=Timeline(100), fmt="png", bg=0.94)
def spacing(f):
    def showMetrics(p:P):
        guide = (P()
            .rect(f.a.r.take(p.ambit().h, "CY").inset(-10, 0))
            .outline(4)
            .f(.74))
        
        return P(guide, p)

    return (
        StSt(txt, fnt, fontSize
            , wght=f.e("eeio", 1, rng=(1, 0)))
            .align(f.a.r)
            .f(0)
            .ch(showMetrics)
            .t(0, 120),
        StSt(txt, fnt, fontSize
            , wght=f.e("eeio", 1, rng=(1, 0))
            , SPAC=f.e("sio", 2, rng=(1, 0)))
            .align(f.a.r)
            .f(0)
            .ch(showMetrics)
            .t(0, -120))

release = spacing.gifski()