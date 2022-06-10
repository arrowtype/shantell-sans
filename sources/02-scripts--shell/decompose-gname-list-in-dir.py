"""
    Script to decompose glyphs to test an italic VF build.
"""

toDecompose=['arrowNE', 'arrowNW', 'arrowSE', 'arrowSW', 'bracketangleright', 'caroncomb', 'dotbelowcmb', 'invertedbrevecmb']


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

        for name in toDecompose:
            font[name].decompose()

        font.save()


