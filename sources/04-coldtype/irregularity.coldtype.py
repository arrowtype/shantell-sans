from coldtype import *

fnt = Font.Cacheable("/Users/stephennixon/code/coldtype-test/assets/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")

@animation((1920, 720), timeline=Timeline(50), fmt="png")
def irregularity(f):
    background = P(f.a.r.inset(0)).f(hsl(240,0,.94))
    return (
        background,
        P(
            StSt("Irregularity is most visible in longer text,".upper(), fnt, 55, TRAK=0.05, wght=f.e("eeio", 1, rng=(1, 0))),
            StSt("where the reader’s eye is sensitive to disruption".upper(), fnt, 55, TRAK=0.05, wght=f.e("eeio", 1, rng=(1, 0))))
        .stack()
        .lead(30)
        .xalign(f.a.r)
        .align(f.a.r)
        .f(0)
        .translate(0, 120),
        P(
            StSt("Irregularity is most visible in longer text,".upper(), fnt, 55, TRAK=0.05, wght=f.e("eeio", 1, rng=(1, 0)), IRGL=f.e("sio", 2, rng=(1, 0))),
            StSt("where the reader’s eye is sensitive to disruption".upper(), fnt, 55, TRAK=0.05, wght=f.e("eeio", 1, rng=(1, 0)), IRGL=f.e("sio", 2, rng=(1, 0))))
        .stack()
        .lead(30)
        .xalign(f.a.r)
        .align(f.a.r)
        .f(0)
        .translate(0, -120)
        )
        

    # return (P(
    #         StSt("TYPOGRAPHY", fnt, 225, wght=f.e("eio", 1, rng=(0, 1))),
    #         StSt("IS KINETIC", fnt, 225, wght=f.e("eio", 1, rng=(1, 0))))
    #     .stack()
    #     .lead(70)
    #     .xalign(f.a.r)
    #     .align(f.a.r)
    #     .f(0)
    #     )

        # StSt("Irregularity is most visible in longer text,\nwhere the human eye is sensitive to disruption".upper(), fnt, 60
        #     , TRAK=0.05
        #     , wght=0.75
        #     , IRGL=f.e("sio", 1, rng=(1, 0)))
        #     .align(f.a.r)
        #     .translate(0, -120)
        #     .f(0)),
