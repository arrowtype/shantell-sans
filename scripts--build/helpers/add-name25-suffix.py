"""
    A script to add a suffix to name ID 25, re:
    https://github.com/fonttools/fontbakery/issues/3024
    https://typo.social/@arrowtype/110430680157544757

    USAGE:

    python3 scripts--build/helpers/add-name25-suffix.py <font_path> -s <suffix>

    LICENSE:
    MIT. Copyright ArrowType 2024. Feel free to use/adapt this as needed. It may have issues.
"""

from fontTools.ttLib import TTFont

# GET / SET NAME HELPER FUNCTIONS


def getFontNameID(font, ID, platformID=3, platEncID=1):
    name = str(font["name"].getName(ID, platformID, platEncID))
    return name


def setFontNameID(font, ID, newName):
    print(f"\n\t• name {ID}:")
    macIDs = {"platformID": 3, "platEncID": 1, "langID": 0x409}
    winIDs = {"platformID": 1, "platEncID": 0, "langID": 0x0}

    oldMacName = font["name"].getName(ID, *macIDs.values())
    oldWinName = font["name"].getName(ID, *winIDs.values())

    if oldMacName != newName:
        print(f"\n\t\t Mac name was '{oldMacName}'")
        font["name"].setName(newName, ID, *macIDs.values())
        print(f"\t\t Mac name now '{newName}'")

    if oldWinName != newName:
        print(f"\n\t\t Win name was '{oldWinName}'")
        font["name"].setName(newName, ID, *winIDs.values())
        print(f"\t\t Win name now '{newName}'")


def main():
    args = parser.parse_args()
    # open font path as a font object, for manipulation

    fontPath = args.fontPath[0]
    font = TTFont(fontPath)
    suffix = args.suffix

    if "fvar" not in font.keys():
        print("Font is not variable. Should not have NameID 25.")
        return

    familyName = font["name"].getBestFamilyName()

    oldPsVarPrefix = getFontNameID(font, 25)
    if oldPsVarPrefix == "None":
        oldPsVarPrefix = familyName.replace(" ", "")

    newPsVarPrefix = oldPsVarPrefix + suffix

    # UPDATE NAME ID 1, basic font name
    setFontNameID(font, 25, newPsVarPrefix)

    # print info
    print("25:", newPsVarPrefix)

    # SAVE FONT
    if args.inplace:
        font.save(fontPath)
    else:
        try:
            font.save(fontPath.replace(".ttf", f".{suffix.replace(' ','')}.ttf"))
        except:
            font.save(fontPath.replace(".otf", f".{suffix.replace(' ','')}.otf"))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Add a suffix to name ID 25.")
    parser.add_argument("fontPath", help="Path to a font file", nargs=1)
    parser.add_argument(
        "-s",
        "--suffix",
        default="",
        required=True,
        help="Suffix to add to the family names of a font. Case-sensitive.",
    )
    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Edit fonts and save under the same filepath, without an added suffix.",
    )  # xprn

    main()
