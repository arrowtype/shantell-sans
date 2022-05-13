"""
    A script to add suffixes to the family names of a font binary (TTF/OTF).

    For example, this can add a suffix like "Var" to a variable font.

    USAGE:

    python3 src/build-scripts/helpers/add-familyname-suffix.py <font_path> -s <suffix>

    LICENSE:
    MIT. Copyright ArrowType 2022. Feel free to use/adapt this as needed. It may have issues.
"""

from fontTools.ttLib import TTFont

NAME_IDS = {
    1: 'familyName',    # Family Name Style
    3: 'uniqueID',      # 1.005;ARRW;FamilyName-Style
    4: 'fullName',      # Family Name Style
    5: 'version',       # Version 1.005
    6: 'psName',        # FamilyName-Style
    16: 'typeFamily'    # Family Name
}

# GET / SET NAME HELPER FUNCTIONS

def getFontNameID(font, ID, platformID=3, platEncID=1):
    name = str(font['name'].getName(ID, platformID, platEncID))
    return name

def setFontNameID(font, ID, newName):
    print(f"\n\t• name {ID}:")
    macIDs = {"platformID": 3, "platEncID": 1, "langID": 0x409}
    winIDs = {"platformID": 1, "platEncID": 0, "langID": 0x0}

    oldMacName = font['name'].getName(ID, *macIDs.values())
    oldWinName = font['name'].getName(ID, *winIDs.values())

    if oldMacName != newName:
        print(f"\n\t\t Mac name was '{oldMacName}'")
        font['name'].setName(newName, ID, *macIDs.values())
        print(f"\t\t Mac name now '{newName}'")

    if oldWinName != newName:
        print(f"\n\t\t Win name was '{oldWinName}'")
        font['name'].setName(newName, ID, *winIDs.values())
        print(f"\t\t Win name now '{newName}'")

def getStyleNames(font):
    """
        Returns style names as a list for joining into other names.

        E.g. "Bold Italic" becomes ['Bold', 'Italic']
    """
    # GET NAME ID 17, typographic style name, to use in name ID 6
    styleName = getFontNameID(font, 17)

    if styleName == 'None':
        styleName = getFontNameID(font, 2)
        styleNames = styleName.split()
        setFontNameID(font, 17, styleName)
    else:
        styleNames = str(styleName).split(' ')

    return styleNames

def main():
    args = parser.parse_args()
    # open font path as a font object, for manipulation

    fontPath = args.fontPath[0]
    font = TTFont(fontPath)
    suffix = args.suffix

    # get style name(s) as list
    styleNameList = getStyleNames(font)
    styleName = ' '.join(styleNameList)
    setFontNameID(font, 17, styleName)

    # UPDATE NAME ID 16, typographic family name
    famName = getFontNameID(font, 16)
    if famName == 'None':
        famName = getFontNameID(font, 1)
    newFamName = f"{famName} {suffix}"
    setFontNameID(font, 16, newFamName)

    # UPDATE NAME ID 6, postscript name (FamilyName-Style)
    psNameList = getFontNameID(font, 6).split("-")
    newPsName = f"{psNameList[0]}{suffix.replace(' ','')}-{psNameList[1]}"
    setFontNameID(font, 6, newPsName)

    # TODO? update postscript names added by STAT builder

    # UPDATE NAME ID 4, full name
    newFullName = f"{newFamName} {styleName}"
    setFontNameID(font, 4, newFullName)

    # UPDATE NAME ID 3, unique font name (1.005;ARRW;FamilyName-Style)
    uniqueName = getFontNameID(font, 3)
    newUniqueName = uniqueName.replace(psNameList[0], f"{psNameList[0]}{suffix.replace(' ','')}")
    setFontNameID(font, 3, newUniqueName)

    # UPDATE NAME ID 1, basic font name
    setFontNameID(font, 1, newFamName)

    # print info
    print("16:", newFamName)
    print(" 6:", newPsName)
    print(" 4:", newFullName)
    print(" 3:", newUniqueName)
    print(" 1:", newFamName)

    # SAVE FONT
    if args.inplace:
        font.save(fontPath)
    else:
        try:
            font.save(fontPath.replace(".ttf",f"{suffix.replace(' ','')}.ttf"))
        except:
            font.save(fontPath.replace(".otf",f"{suffix.replace(' ','')}.otf"))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Report what Unicode values a font includes *beyond* given Unicode ranges.')
    parser.add_argument('fontPath', 
                        help='Path to a font file',
                        nargs=1)
    parser.add_argument("-s", "--suffix",
                        default="",
                        required=True,
                        help='Suffix to add to the family names of a font. Case-sensitive.')
    parser.add_argument(
        "-i",
        "--inplace",
        action='store_true',
        help="Edit fonts and save under the same filepath, without an added suffix.",
    )  # xprn

    main()