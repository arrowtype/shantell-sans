from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

txts = [
    "TYPOGRAPHY\nIS KINETIC",
    "ТИПОГРАФИЯ\nКИНЕТИЧЕСКАЯ",
    "BIỂU TƯỢNG\nLÀ KINETIC",
    "LETURFRÆÐI\nER HREYFIMYND",
]

at = AsciiTimeline(2, 24, """
                                                                 <  
0               1               2               3
""").inflate(lines=[1])

@animation((1400, 540), timeline=at, bg=1, render_bg=1, release=lambda x: x.gifski())
def languages(f):
    current = at.current()
    txt = txts[int(current.name)]

    return (StSt(txt, fnt, 120
        , SPAC=current.e("eeo", 1, rng=(0,0.35))
        , wght=current.e("seo", 1, rng=(0, 1))
        , ital=current.e("qeo", 1, rng=(0, 1))
        , INFM=current.e("seo", 1, rng=(0, 1))
        , BNCE=current.e("l", 0, rng=(0, 1)))
        .lead(50)
        .xalign(f.a.r)
        .align(f.a.r)
        .f(0))