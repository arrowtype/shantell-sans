from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

txt = """
Irregularity is most visible in longer text,
where the reader’s eye is sensitive to disruption
""".upper()

@animation((1920, 720), timeline=50, bg=hsl(240,0,.94))
def irregularity(f):
    return (P(
        StSt(txt, fnt, 55
            , SPAC=0.05
            , wght=f.e("eeio", 1, rng=(1, 0))
            , leading=30),
        StSt(txt, fnt, 55
            , SPAC=0.05
            , wght=f.e("eeio", 1, rng=(1, 0))
            , INFM=f.e("sio", 2, rng=(1, 0))
            , leading=30))
        .stack(100)
        .map(lambda p: p.xalign(f.a.r))
        .align(f.a.r)
        .f(0))


release = irregularity.gifski()