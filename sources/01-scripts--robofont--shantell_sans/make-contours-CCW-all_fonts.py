for f in AllFonts():
    for g in f:
        try:
            for c in g.contours:
                if c.clockwise == True:
                    c.reverse()
        except:
            print(f"{g.name} couldn’t be wound counter-clockwise")
            pass