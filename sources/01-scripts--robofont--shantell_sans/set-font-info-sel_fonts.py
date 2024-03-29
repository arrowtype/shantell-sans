from vanilla.dialogs import *

inputFonts = getFile("select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])

for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)

    # for other font info attributes, see
    # http://unifiedfontobject.org/versions/ufo3/fontinfo.plist/

    f.info.openTypeOS2VendorID = "@"

    f.info.copyright = "Copyright 2022 The Shantell Sans Project Authors (https://github.com/arrowtype/shantell-sans)"

    f.info.unitsPerEm = 1000

    # setting metrics
    ascent = 1020
    descent = -320

    f.info.openTypeOS2TypoAscender = ascent
    f.info.openTypeOS2TypoDescender = descent
    f.info.openTypeOS2TypoLineGap = 0
    
    f.info.openTypeOS2WinAscent = ascent
    f.info.openTypeOS2WinDescent = abs(descent)

    f.info.openTypeHheaAscender = ascent
    f.info.openTypeHheaDescender = descent
    f.info.openTypeHheaLineGap = 0

    # un-nest nested components # https://github.com/googlefonts/fontbakery/issues/296
    f.lib["com.github.googlei18n.ufo2ft.filters"] = [
            {
            'name': 'decomposeTransformedComponents', 
            'pre': 1
            },
            {
            'name': 'flattenComponents', 
            'pre': 1
            },
            {
            'name': 'EraseOpenCorners', 
            'pre': 0
            },
    ]

    f.info.familyName = "Shantell Sans"

    print("Updated info for: ", f.info.familyName, " ", f.info.styleName)

    f.save()
    f.close()