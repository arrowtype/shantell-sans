"""
    Script by @yanone

    Simplified by using the arg `--update-name-table` in the build-vf `fonttools varLib.instancer` command.

    USAGE:
    python3 scripts--build/helpers/convert-to-italic.py <input-font-path> <output-font-path>

"""

import sys
import math
from fontTools.ttLib import TTFont

font = TTFont(sys.argv[-2])

# Italic angle
font["post"].italicAngle = -11

# Caret slope
font["hhea"].caretSlopeRise = font["head"].unitsPerEm
font["hhea"].caretSlopeRun = round(
    math.atan(math.radians(abs(font["post"].italicAngle))) * font["head"].unitsPerEm
)

font.save(sys.argv[-1])
