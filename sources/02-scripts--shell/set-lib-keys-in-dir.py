"""
    Script to set ufo2ft lib keys in all UFOs within a directory.

    (Testing code for prep-build.py)
"""

import os
from fontParts.fontshell import RFont as Font

prepDir = 'sources/ital_wght_BNCE_IRGL_TRAK--prepped'

def setLibKeys(font):
    """
        Set lib keys for proper ufo2ft processing during build.
    """

    # set this or it trips up ufoLib
    font.defaultLayer.name = "foreground"

        # un-nest nested components # https://github.com/googlefonts/fontbakery/issues/296
    font.lib["com.github.googlei18n.ufo2ft.filters"] = [
            {
            'name': 'decomposeTransformedComponents', 
            'pre': 1
            },
            {
            'name': 'flattenComponents', 
            'pre': 1
            }
    ]

    font.save()



def main():
    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.ufo' in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    print("🤖 Correcting font lib keys for ufo2ft filters")
    for font in fonts:
        setLibKeys(font)

if __name__ == "__main__":
    main()
