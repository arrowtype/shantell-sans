"""
	Update feature code for static build
"""

import sys
from fontParts.world import *

fontPath = sys.argv[1]

font = OpenFont(fontPath, showInterface=False)


if "sparse" not in fontPath:
    print()
    print(font.info.familyName, font.info.styleName)
    print("feature code was:")
    print(font.features.text)

    with open("sources/features/features.fea") as features:
        feaCode = features.read()

    font.features.text = feaCode.replace("(./features", "(../features/features")
    
    print("feature code is now:")
    print(font.features.text)
    print()


font.save()
