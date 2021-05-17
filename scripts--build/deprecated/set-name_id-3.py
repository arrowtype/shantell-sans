# coding=utf8

'''

    Name table ID 3 is a "Unique Font Name." When built in FontMake, it looks something like this:
        
        1.001;ARRW;ShantellSans-Regular

    This script will set the first part to the current project version, which font-v doesn’t currently do.

    Note: it is specific to Arrow Type, and will add "ARRW" as the vendor prefix. This can be easily edited.

    0. You must have FontTools installed
    1. In your terminal, go to the base of the font project. Run this script, and add a path or paths to fonts as an argument, e.g.:

        python <path>/set-name_id-3.py <path>/<font>.ttf

'''

import os
import argparse
from fontTools.ttLib import TTFont


def getVersion():
    with open("version.txt") as f:
        currentVersion = f.read().replace("\n","")
        return currentVersion

def getFontNameID(font, ID, platformID=3, platEncID=1):
    name = str(font['name'].getName(ID, platformID, platEncID))
    return name

def setFontNameID(font, ID, newName, platformID=3, platEncID=1, langID=0x409):
    print(f"\n\t• name {ID}:")
    oldName = font['name'].getName(ID, platformID, platEncID)
    print(f"\n\t\t was '{oldName}'")
    font['name'].setName(newName, ID, platformID, platEncID, langID)
    print(f"\n\t\t now '{newName}'")


# PARSE ARGUMENTS

parser = argparse.ArgumentParser(description='Add version numbering to font name IDs')

parser.add_argument('fonts', nargs="+")

parser.add_argument(
        "-i",
        "--inplace",
        action='store_true',
        help="Edit fonts and save under the same filepath, without an added suffix.",
    )


def main():
    args = parser.parse_args()
    projectVersion = getVersion()

    for font_path in args.fonts:
        # open font path as a font object, for manipulation
        ttfont = TTFont(font_path)

        psName = str(getFontNameID(ttfont, 6))

        newUniqueID = f"{projectVersion};ARRW;{psName}"
        setFontNameID(ttfont, 3, newUniqueID)

        # SAVE FONT
        if args.inplace:
            ttfont.save(font_path)
        else:
            ttfont.save(font_path.replace(".ttf",f"-{projectVersion}.ttf").replace(".otf",f"-{projectVersion}.otf"))


if __name__ == '__main__':
    main()
