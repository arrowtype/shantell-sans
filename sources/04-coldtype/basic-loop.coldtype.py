from curses import KEY_FIND
from coldtype import *

fnt = Font.Cacheable("fonts/Shantell Sans/Desktop/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")

@animation((1920, 720), timeline=Timeline(50), fmt="png")
def kinetic4(f):
    background = P(f.a.r.inset(0)).f(hsl(240,0,.94)) #hsl(240,0,.94)
    return (
        background,
        StSt("TYPOGRAPHY", fnt, 225
        # StSt("ТИПОГРАФИЯ", fnt, 225
            # , TRAK=0.125
            , TRAK=f.e("eeio", 1, rng=(0, .25))
            , wght=f.e("sio", 1, rng=(0, 1))
            , ital=f.e("eeio", 1, rng=(0, 1))
            , IRGL=f.e("sio", 2, rng=(0, 1))
            , BNCE=f.e("l", 1, rng=(0, 1)))
            .align(f.a.r)
            .translate(0, 120)
            .f(0),
        StSt("IS KINETIC", fnt, 225
        # StSt("КИНЕТИЧЕСКАЯ", fnt, 225
            , TRAK=f.e("eeio", 1, rng=(.4, 0))
            # , TRAK=0
            , wght=f.e("sio", 1, rng=(1, 0))
            , ital=f.e("eeio", 1, rng=(1, 0))
            , IRGL=f.e("sio", 2, rng=(0, 1))
            , BNCE=f.e("l", 1, rng=(1, 0)))
            .align(f.a.r)
            .translate(0, -120)
            .f(0)),

def gifski(a:animation, passes):
    from subprocess import run
    root = a.pass_path(f"%4d.{a.fmt}").parent.parent
    gif = root / (a.name + ".gif")
    run(["gifski", "--fps", str(a.timeline.fps), "-o", gif, "-W", "1080", "-Q", "70", *[p.output_path for p in passes if p.render == a]])

def release(passes):
    print(kinetic4.rect[2])
    gifski(kinetic4, passes)