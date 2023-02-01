from coldtype import *

fnt = Font.Find(r"ShantellSans\[.*\]\.ttf", regex_dir="fonts")

txt = """
Informality is most visible in longer text,
where the reader’s eye is sensitive to irregularity
""".upper()

@animation((1920, 720), timeline=50, bg=hsl(240,0,.94), release=lambda a: a.gifski())
def irregularity(f):
    def text(infm):
        return (StSt(txt, fnt, 55
            , SPAC=0.05
            , wght=f.e("eeio", 1, rng=(1, 0))
            , INFM=f.e("sio", 2, rng=(1, 0)) if infm else None
            , leading=30)
            .xalign(f.a.r))
    
    return (P(text(False), text(True))
        .stack(100)
        .align(f.a.r)
        .f(0))


release = irregularity.gifski()