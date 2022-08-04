from coldtype import *

fnt = Font.Cacheable("/Users/stephennixon/code/coldtype-test/assets/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")

@animation((1920, 720), timeline=Timeline(25), fmt="png")
def bounce(f):
    background = P(f.a.r.inset(0)).f(hsl(240,0,.94)) #hsl(240,0,.94)
    baseline = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,43)
    capheight = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,195)
    baseline2 = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,-195)
    capheight2 = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,-43)
    return (
        background,
        baseline,
        capheight,
        baseline2,
        capheight2,
        # StSt("Variable Bounce", fnt, 180
        StSt("Fonts Are Cool!", fnt, 225
        # StSt("ТИПОГРАФИЯ", fnt, 180
            # , TRAK=0.125
            , wght=0.75)
            # , ital=f.e("eeio", 1, rng=(0, 1))
            # , IRGL=f.e("sio", 2, rng=(0, 1))
            # , BNCE=f.e("l", 1, rng=(0, 1)))
            .align(f.a.r)
            .translate(0, 120)
            .f(0),
        # StSt("Variable Bounce", fnt, 180
        StSt("Fonts Are Cool!", fnt, 225
        # StSt("КИНЕТИЧЕСКАЯ", fnt, 180
            # , TRAK=0.125
            # , TRAK=0
            , wght=0.75
            # , ital=0
            # , IRGL=f.e("sio", 2, rng=(0, 1))
            , BNCE=f.e("sio", 1, rng=(1, 0)))
            .align(f.a.r)
            .translate(0, -120)
            .f(0)),
