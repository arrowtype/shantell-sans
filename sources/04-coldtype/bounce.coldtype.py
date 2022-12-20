from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

def bounce(f, txt, fontSize):
    def buildText(bounce:bool):
        p = (StSt(txt, fnt, fontSize
            , wght=f.e("eeio", 1, rng=(1, 0))
            , BNCE=f.e("sio", 2, rng=(1, 0)) if bounce else None)
            .align(f.a.r, tx=0)
            .f(0))

        guide = (P()
            .rect(f.a.r.take(p.ambit().h, "CY").inset(-10, 0))
            .outline(2)
            .f(.74))
        
        return P(guide, p)

    return (P(buildText(False), buildText(True))
        .stack(80)
        .align(f.a.r))


args = dict(rect=(1920, 720), timeline=50, bg=hsl(240,0,.94))

@animation(**args)
def bounce1(f):
    return bounce(f, "Fonts are Cool!", 225)

@animation(**args)
def bounce2(f):
    return bounce(f, "ТИПОГРАФИЯ", 180)


def release(passes):
    bounce1.gifski()(passes)
    bounce2.gifski(open=True)(passes)