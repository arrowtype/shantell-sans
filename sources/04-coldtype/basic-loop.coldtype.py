from coldtype import *

fnt = Font.Cacheable("/Users/stephennixon/code/coldtype-test/assets/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")

@animation((1920, 720), timeline=Timeline(50), fmt="png")
def kinetic4(f):
    background = P(f.a.r.inset(0)).f(hsl(240,0,.94)) #hsl(240,0,.94)
    return (
        background,
        StSt("TYPOGRAPHY", fnt, 225
        # StSt("ТИПОГРАФИЯ", fnt, 225
            , TRAK=0.125
            , wght=f.e("sio", 1, rng=(0, 1))
            , ital=f.e("eeio", 1, rng=(0, 1))
            , IRGL=f.e("sio", 2, rng=(0, 1))
            , BNCE=f.e("l", 1, rng=(0, 1)))
            .align(f.a.r)
            .translate(0, 120)
            .f(0),
        StSt("IS KINETIC", fnt, 225
        # StSt("КИНЕТИЧЕСКАЯ", fnt, 225
            , TRAK=0.125
            # , TRAK=0
            , wght=f.e("sio", 1, rng=(1, 0))
            , ital=f.e("eeio", 1, rng=(1, 0))
            , IRGL=f.e("sio", 2, rng=(0, 1))
            , BNCE=f.e("l", 1, rng=(1, 0)))
            .align(f.a.r)
            .translate(0, -120)
            .f(0)),
