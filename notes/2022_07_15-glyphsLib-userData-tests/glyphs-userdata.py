# from glyphsLib import GSFont, classes
import glyphsLib
from glyphsLib import GSFont

# print(glyphsLib.__version__)

# print(GSFont)

glyphs_file = "sources/shantellsans-wght_ital_IRGL.glyphs"
gsfont =  GSFont(glyphs_file)

# print(gsfont)

# userData = gsfont.userData

# # userData["bounces"] = {}
# # userData["bounces"]["A"] = 36

# del userData["bounces"] # reverse the test

# gsfont.save(glyphs_file)

# converts to UFO and returns namedtuple
sourceUfos = glyphsLib.build_masters(
    glyphs_file,
    "notes/2022_07_15-glyphsLib-userData-tests/UFO"
    # designspace_path=options.designspace_path,
    # minimize_glyphs_diffs=options.no_preserve_glyphsapp_metadata,
    # propagate_anchors=options.propagate_anchors,
    # normalize_ufos=options.normalize_ufos,
    # create_background_layers=options.create_background_layers,
    # generate_GDEF=options.generate_GDEF,
    # store_editor_state=not options.no_store_editor_state,
    # write_skipexportglyphs=options.write_public_skip_export_glyphs,
    # ufo_module=__import__(options.ufo_module),
)[0]


print()
print()
print()

# mainUFOpath = [font.path for font in sourceUfos.values() if font.info.styleName == "ExtraBold"][0]

glyphBounceDict = [master for master in gsfont.masters if master.name == "ExtraBold"][0].userData["com.arrowtype.glyphBounces"]

print(glyphBounceDict["g"])
