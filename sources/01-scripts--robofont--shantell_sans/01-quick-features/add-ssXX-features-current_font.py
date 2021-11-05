"""
    Go through current font/UFO and make OT features for all suffixed characters, with one click.
    
    WARNING: Makes assumptions specific to the Shantell Sans font project.
"""

f = CurrentFont()

# get feature text
fea = f.features.text

# start new features with removed ss0X features
newFea = "\n".join([line for line in fea.split("\n") if ".ss" not in line and " ss" not in line and line is not ""])
newFea += "\n\n"

# get list of ".ssXX" glyph names in the font
ss0xAlternates = sorted([gname for gname in f.keys() if ".ss" in gname])

# make list of distinct ss0X feature suffixes in font
ss0xFeatures = sorted(list(set([name.split(".")[1] for name in ss0xAlternates])))

# build ss0X feature text

for suffix in ss0xFeatures:
    fea = f"feature {suffix} {'{'}\n"

    for gname in ss0xAlternates:
        if suffix in gname:
            fea += f"    sub {gname.split('.')[0]} by {gname.split('.')[0]}.{suffix};\n"

    fea += f"{'}'} {suffix};\n\n"

    newFea += fea

# add new ss0X features
f.features.text = newFea
