from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

VERSIONS = {
    "latin": dict(script="latin", txt="Fonts are Cool!", fontSize=450),
    "cyrillic": dict(script="cyrillic", txt="ТИПОГРАФИЯ", fontSize=180),
} #/VERSIONS

# @animation(rect=(1920, 720) # HD
@animation((3840, 2160) # 4K
    , timeline=100
    , bg=hsl(240,0,.94)
    # , release=lambda a: a.gifski()
    , release=lambda a: a.export("h264", open=0)
    )
def bounce_ƒVERSION(f):
    def buildText(bounce:bool):
        p = (StSt(__VERSION__["txt"], fnt, __VERSION__["fontSize"]
            , wght=f.e("sio", 1, rng=(1, 0))
            , BNCE=f.e("seio", 2, rng=(1, 0)) if bounce else None)
            .align(f.a.r, tx=0)
            .f(0))

        guide = (P()
            .rect(f.a.r.take(p.ambit().h, "CY").inset(-10, 0))
            .outline(2)
            .f(.74))
        
        return P(guide, p)

    return (P(buildText(False), buildText(True))
        .stack(80)
        .lead(80)
        .align(f.a.r))
