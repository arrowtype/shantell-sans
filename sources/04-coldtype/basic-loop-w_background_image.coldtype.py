"""
    Attempting to place a background image (i.e. for a border), then have an animation over top of it.

    Not sure what might be the best way to do so... drawbot? An img() function? 
    If so... where and how? I’ve experimented a bit, but haven’t yet had success.
"""



from coldtype import *
from coldtype.drawbot import *
from drawBot import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

VERSIONS = [
    # dict(script="latin", text="TYPOGRAPHY\nIS KINETIC", fontSize=225),
    dict(script="latin", text="~HAND~\nWRITING", fontSize=250),
    dict(script="cyrillic", text="ТИПОГРАФИЯ\nКИНЕТИЧЕСКАЯ", fontSize=180),
] #/VERSIONS


# @animation((1920, 720)
@animation((1920, 1080)
    , timeline=Timeline(50)
    , bg=hsl(240,0,.94)
    , release=lambda x: x.gifski()
    # , release=lambda a: a.export("h264", open=0)
    , name="handwriting_" + __VERSION__["script"]
    )

def kinetic4(f):
    def styler(g):

        # Trying to add a test image to the background... not yet working
        # img(src="/Users/stephennixon/type-repos/shantell-sans/specimens/shantell_sans-hero_16x9.png", rect=Rect(0, 0, 500, 500), pattern=False, opacity=0.5)


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