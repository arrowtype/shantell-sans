"""
    Very simple script to add guidelines to currently-selected glyphs.
"""

f = CurrentFont()

for gname in f.selection:
    g = f[gname]
    g.clearGuidelines()
    g.appendGuideline((0,780), 0)
    g.appendGuideline((0,-80), 0)
    