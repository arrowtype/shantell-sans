"""
    Set all selected glyphs in current font to be non-exporting.
"""

f = CurrentFont()

if "public.skipExportGlyphs" not in f.lib.keys():
    f.lib["public.skipExportGlyphs"] = [f.selection[0]]

# clean up any duplicate references
f.lib["public.skipExportGlyphs"] = list(set(f.lib["public.skipExportGlyphs"]))

# go through selected glyphs and add them to skip-export list in font lib
for glyphname in f.selection:
    if glyphname not in f.lib["public.skipExportGlyphs"]:
        f.lib["public.skipExportGlyphs"].append(glyphname)
        print(f"{glyphname} now set to non-exporting")
        
f.update()