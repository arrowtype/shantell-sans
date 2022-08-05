from coldtype import *

fnt = Font.MutatorSans()

@animation((1920, 540), timeline=Timeline(40), fmt="png")
def with_glyphwise(f):
    def styler(x):
        if x.l == 0:
            wght = f.e("qeio", 1, rng=(0, 1))
        else:
            wght = f.e("seio", 1, rng=(1, 0))
        
        return Style(fnt, 225, wght=wght)

    return (Glyphwise("TYPOGRAPHY\nIS KINETIC", styler)
        .xalign(f.a.r)
        .lead(30)
        .align(f.a.r)
        .f(0))

@animation((1920, 540), timeline=Timeline(40), fmt="png")
def with_stst(f):
    return (P(
            StSt("TYPOGRAPHY", fnt, 225, wght=f.e("eio", 1, rng=(0, 1))),
            StSt("IS KINETIC", fnt, 225, wght=f.e("eio", 1, rng=(1, 0))))
        .stack()
        .lead(30)
        .xalign(f.a.r)
        .align(f.a.r)
        .f(0))