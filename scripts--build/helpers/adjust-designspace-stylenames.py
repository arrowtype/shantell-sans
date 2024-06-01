"""
    Adjust the stylemapfamilyname and stylemapstylename attributes of a designspace.
"""

import sys
from fontTools.designspaceLib import DesignSpaceDocument

# Get designspace path from terminal
dsPath = sys.argv[1]

# open designspace as object
doc = DesignSpaceDocument.fromfile(dsPath)

for i in doc.instances:
    i.styleMapFamilyName = i.familyName + " " + i.styleName.replace("Italic", "")

    i.postScriptFontName = (
        i.familyName.replace(" ", "") + "-" + i.styleName.replace(" ", "")
    )

    if i.styleName == "Regular":
        i.styleMapFamilyName = i.familyName
        i.styleMapStyleName = "regular"

    elif i.styleName == "Italic":
        i.styleMapFamilyName = i.familyName
        i.styleMapStyleName = "italic"

    elif i.styleName == "Bold":
        i.styleMapFamilyName = i.familyName
        i.styleMapStyleName = "bold"

    elif i.styleName == "Bold Italic":
        i.styleMapFamilyName = i.familyName
        i.styleMapStyleName = "bold italic"

    elif "Italic" in i.styleName:
        i.styleMapFamilyName = i.familyName + " " + i.styleName.replace("Italic", "")
        i.styleMapStyleName = "italic"

    else:
        i.styleMapFamilyName = i.familyName + " " + i.styleName
        i.styleMapStyleName = "regular"

doc.write(dsPath)

# save to a new path
# doc.write(dsPath.replace(".designspace", ".stylemapped.designspace"))
