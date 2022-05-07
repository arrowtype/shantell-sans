f = CurrentFont()

for gname in f.selection:
    if "_top" not in [a.name for a in f[gname].anchors]:
        f[gname].appendAnchor("_top", (0, f.info.xHeight))