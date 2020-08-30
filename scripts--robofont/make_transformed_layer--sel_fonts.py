"""
    Script to transform glyphs by amounts specified in YAML, 
    and place these transformed glyphs into a background layer as drawing guides.

    Run from the base directory of the Shantell Sans font project.
"""

import yaml
from vanilla.dialogs import *

# open fonts


# if you provide a custom config path, this picks it up
try:
    configPath = '/Users/stephennixon/type-repos/shantell/sources/organic_experiment_04-alts-shift-shaping/transforms.yaml'
except IndexError:
    print("Sorry, the YAML path needs to be updated in this script.")

# read yaml config
with open(configPath) as file:
    transforms = yaml.load(file, Loader=yaml.FullLoader)

# import pprint
# pprint.pprint(transforms)


files = getFile("Select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])

for file in files:
    f = OpenFont(file, showInterface=False)

    for g in f:
        if g.name in transforms.keys():
            print(g.name, transforms[g.name])


    f.save()
    f.close()

