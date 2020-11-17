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
    
    font.features.text = """\
    languagesystem DFLT dflt;
    languagesystem latn dflt;

    include(./features/features/common.fea);
    include(./features/features/frac.fea);
    include(./features/features/numr_dnom_supr_infr.fea);

    """
    
    print("feature code is now:")
    print(font.features.text)
    print()


font.save()
