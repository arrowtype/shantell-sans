# coding=utf8

'''
    TODO: set versioning:
    - `name 5`, like: "Version 1.000;[cf8dc25]"
    - `head.fontRevision`

    Name table ID 3 is a "Unique Font Name." When built in FontMake, it looks something like this:
        
        1.001;ARRW;FamilyName-Regular

    This script will set the first part to the current project version, which font-v doesn’t currently do.


    0. You must have FontTools installed
    1. In your terminal, go to the base of the font project. Run this script, and add a path or paths to fonts as an argument, e.g.:

        python <path>/set-version-data.py <path>/<font>.ttf

'''

import os
import argparse
from fontTools.ttLib import TTFont


def getFontNameID(font, ID, platformID=3, platEncID=1):
    name = str(font['name'].getName(ID, platformID, platEncID))
    return name


def setFontNameID(font, ID, newName, platformID=3, platEncID=1, langID=0x409):
    print(f"\n\t• name {ID}:")
    oldName = font['name'].getName(ID, platformID, platEncID)
    print(f"\n\t\t was '{oldName}'")

    # set Windows name
    font['name'].setName(newName, ID, platformID, platEncID, langID)
    # set Mac name – does this need a try/except block?
    font['name'].setName(newName, ID, 1, 0, 0x0)

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

parser.add_argument(
        "-v",
        "--version",
        type=str,
        help="The numeric version of the font, e.g. 1.001",
    )

parser.add_argument(
        "-s",
        "--sha1",
        type=str,
        help="The sha1 has for the latest Git commit, e.g. cf8dc25",
    )


def main():
    args = parser.parse_args()
    projectVersion = args.version.replace("\n","")

    for font_path in args.fonts:
        # open font path as a font object, for manipulation
        ttfont = TTFont(font_path)

        # set head.fontRevision
        oldFontRevision = ttfont["head"].fontRevision
        ttfont["head"].fontRevision =float(projectVersion)
        print(f"head.fontRevision was {oldFontRevision}, is now {ttfont['head'].fontRevision}")

        # Set nameID 5
        gitHash = args.sha1.replace("\n","")
        versionName=f"Version {projectVersion};[{args.sha1}]"
        setFontNameID(ttfont, 5, versionName)

        # Set nameID 3
        psName = str(getFontNameID(ttfont, 6))
        vendor = str(getFontNameID(ttfont, 3)).split(";")[1]
        newUniqueID = f"{projectVersion};{vendor};{psName}"
        setFontNameID(ttfont, 3, newUniqueID)

        # SAVE FONT
        print(font_path)
        if args.inplace:
            ttfont.save(font_path)
        else:
            ttfont.save(font_path.replace(".ttf",f"-{projectVersion}.ttf").replace(".otf",f"-{projectVersion}.otf"))


if __name__ == '__main__':
    main()
