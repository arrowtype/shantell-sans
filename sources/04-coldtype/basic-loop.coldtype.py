from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

VERSIONS = [
    dict(script="latin", text="TYPOGRAPHY\nIS KINETIC", fontSize=225),
    dict(script="cyrillic", text="ТИПОГРАФИЯ\nКИНЕТИЧЕСКАЯ", fontSize=180),
] #/VERSIONS

@animation((1920, 720)
    , timeline=Timeline(50)
    , bg=hsl(240,0,.94)
    , release=lambda x: x.gifski()
    , name="kinetic4_" + __VERSION__["script"]
    )
def kinetic4(f):
    def styler(g):
        if g.l == 0:
            return Style(fnt
                , fontSize=__VERSION__["fontSize"]
                , SPAC=f.e("eeio", 1, rng=(0, .25))
                , wght=f.adj(-g.i*2).e("sio", 1, rng=(0, 1))
                , ital=f.e("eeio", 1, rng=(0, 1))
                , INFM=f.e("sio", 2, rng=(0, 1))
                , BNCE=f.e("l", 1, rng=(0, 1)))
        else:
            return Style(fnt, __VERSION__["fontSize"]
                , SPAC=f.e("eeio", 1, rng=(.4, 0))
                , wght=f.adj(g.i*2).e("sio", 1, rng=(1, 0))
                , ital=f.e("eeio", 1, rng=(1, 0))
                , INFM=f.e("sio", 2, rng=(0, 1))
                , BNCE=f.e("l", 1, rng=(1, 0)))

    return (Glyphwise(__VERSION__["text"], styler)
        .xalign(f.a.r, tx=0)
        .lead(60)
        .align(f.a.r, tx=0)
        .f(0))