"""
    Mark selected glyphs bright green
    (e.g. to indicate they have been corrected as italics)
"""

f = CurrentFont()

for name in f.selection:
    f[name].markColor = (0.67, 0.95, 0.38, 1.0) # bright green from Glyphs3