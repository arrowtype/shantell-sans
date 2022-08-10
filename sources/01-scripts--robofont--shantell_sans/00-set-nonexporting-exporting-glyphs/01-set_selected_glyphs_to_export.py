"""
    Set all selected glyphs in current font to export.
"""

f = CurrentFont()

# clean up any duplicate references
f.lib["public.skipExportGlyphs"] = list(set(f.lib["public.skipExportGlyphs"]))

# go through selected glyphs and remove them from skip-export list in font lib
for glyphname in f.selection:
    if glyphname in f.lib["public.skipExportGlyphs"]:
        f.lib["public.skipExportGlyphs"].remove(glyphname)
        print(f"{glyphname} now set to export")
        
f.update()