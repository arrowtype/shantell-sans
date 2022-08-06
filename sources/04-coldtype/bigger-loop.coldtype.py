from coldtype import *

fnt = Font.Cacheable("fonts/Shantell Sans/Desktop/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")


txts = [
    "TYPOGRAPHY\nIS KINETIC",
    "ТИПОГРАФИЯ\nКИНЕТИЧЕСКАЯ",
    "BIỂU TƯỢNG\nLÀ KINETIC",
    "LETURFRÆÐI\nER HREYFIMYND",
]

at = AsciiTimeline(1, 10, """
                                                                 <  
0               1               2               3
""").inflate(lines=[1])

@animation((1400, 540), timeline=at, bg=1, render_bg=1)
def languages(f):
    current = at.current()
    txt = txts[int(current.name)]

    return (StSt(txt, fnt, 120
        , TRAK=current.e("eeio", 1, rng=(0,0.25))
        , wght=current.e("sio", 1, rng=(0, 1))
        , ital=current.e("eeio", 1, rng=(0, 1))
        , IRGL=current.e("sio", 1, rng=(0, 1))
        , BNCE=current.e("l", 1, rng=(0, 1))
        )
        .lead(50)
        .xalign(f.a.r)
        .align(f.a.r)
        # .f=current.e(rng=(0,1))
        .f(0)
        )

# def release(passes):
#     FFMPEGExport(languages, passes).gif().write()

def gifski(a:animation, passes):
    from subprocess import run
    root = a.pass_path(f"%4d.{a.fmt}").parent.parent
    gif = root / (a.name + ".gif")
    run(["gifski", "--fps", str(a.timeline.fps), "-o", gif, *[p.output_path for p in passes if p.render == a]])

def release(passes):
    gifski(languages, passes)
