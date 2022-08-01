"""
    Script to empty the public.postscriptNames dict in the font.lib of all UFOs in a Dir.

    Relavent to https://github.com/arrowtype/shantell-sans/issues/87
"""

import sys
import os
from fontParts.fontshell import RFont as Font

dirToEdit = sys.argv[1]

ufosToEdit = next(os.walk(dirToEdit))[1]

print(ufosToEdit)

# for path in ufosToEdit
for ufoName in ufosToEdit:
    if ".ufo" in ufoName:
        ufoPath = os.path.join(dirToEdit, ufoName)

        # open font
        font = Font(ufoPath)

        font.kerning.clear()
        font.groups.clear()

        font.save()


