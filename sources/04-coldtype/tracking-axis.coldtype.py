from coldtype import *

fnt = Font.Cacheable("fonts/Shantell Sans/Desktop/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf")

@animation((1920, 720), timeline=Timeline(100), fmt="png")
def spacing(f):
    background = P(f.a.r.inset(0)).f(hsl(240,0,.94)) #hsl(240,0,.94)
    baseline = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,43)
    capheight = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,195)
    baseline2 = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,-195)
    capheight2 = P().rect(f.a.r.inset(0,358)).f(hsl(208,0.01,.74)).translate(0,-43)
    return (
        background,
        baseline,
        capheight,
        baseline2,
        capheight2,
        # StSt("Variable Bounce", fnt, 180
        StSt("SPACING", fnt, 225
        # StSt("ТИПОГРАФИЯ", fnt, 180
            # , TRAK=0.125
            , wght=f.e("eeio", 1, rng=(1, 0)))
            # , ital=f.e("eeio", 1, rng=(0, 1))
            # , IRGL=f.e("sio", 2, rng=(0, 1))
            # , BNCE=f.e("l", 1, rng=(0, 1)))
            .align(f.a.r)
            .translate(0, 120)
            .f(0),
        # StSt("Variable Bounce", fnt, 180
        StSt("SPACING", fnt, 225
        # StSt("КИНЕТИЧЕСКАЯ", fnt, 180
            # , TRAK=0.125
            # , TRAK=0
            , wght=f.e("eeio", 1, rng=(1, 0))
            # , ital=0
            # , IRGL=f.e("sio", 2, rng=(0, 1))
            , TRAK=f.e("sio", 2, rng=(1, 0)))
            .align(f.a.r)
            .translate(0, -120)
            .f(0)),

def gifski(a:animation, passes):
    from subprocess import run
    root = a.pass_path(f"%4d.{a.fmt}").parent.parent
    gif = root / (a.name + ".gif")
    run(["gifski", "--fps", str(a.timeline.fps), "-o", gif, "-W", "1080", "-Q", "70", *[p.output_path for p in passes if p.render == a]])

def release(passes):
    gifski(spacing, passes)
