"""
    Add a dummy/linear AVAR table to a variable font.
"""

import sys
from fontTools.ttLib import TTFont, newTable
from fontTools.ttLib.tables._a_v_a_r import table__a_v_a_r

def main():
    filepath = sys.argv[1]
    font = TTFont(filepath)

    avar = newTable("avar")

    for axis in font["fvar"].axes:
        avar.segments[axis.axisTag] = {-1.0: -1.0, 0.0: 0.0, 1.0: 1.0}
        print(f"Added dummy AVAR segment for {axis.axisTag}")

    font.tables["avar"] = avar

    font.save(filepath)
    print(f"Added AVAR table to {filepath}")


if __name__ == "__main__":
    main()
