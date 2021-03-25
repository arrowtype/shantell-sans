'''
    Check for DesignSpaceProblems

    python scripts--shell/check-ds-problems.py <designspacePath>
'''

from designspaceProblems import DesignSpaceChecker
from pprint import pprint
import sys

# designspacePath = sys.argv[1]
designspacePath = "sources/shantell-300_800.designspace"


print(designspacePath)

dc = DesignSpaceChecker(designspacePath)
dc.checkEverything()

# # now all problems are stored in dc.problems
pprint(dc.problems)

# for problem in dc.problems:
#     problem