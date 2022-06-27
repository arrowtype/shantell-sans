"""
    Run UFO Normalizer on UFOs within specified directory.

    Run from command line. Example:

    python <path>/ufonormalize-sel_fonts.py "sources/italics"
"""

import sys
import os
import subprocess

dirToEdit = sys.argv[1]

pathsInDir = next(os.walk(dirToEdit))[1]

# for path in pathsInDir
for ufoName in pathsInDir:
    if ".ufo" in ufoName:
        ufoPath = os.path.join(dirToEdit, ufoName)
        print(ufoPath)

        subprocess.run(['ufonormalizer',ufoPath,'-m'])
