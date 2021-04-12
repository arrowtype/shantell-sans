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
    transformsPath = '/Users/stephennixon/type-repos/shantell/sources/organic_experiment_04-alts-shift-shaping/transforms.yaml'
except IndexError:
    print("Sorry, the YAML path needs to be updated in this script.")

# read yaml config
with open(transformsPath, 'r', encoding='utf8') as yml:
    transforms = yaml.load(yml, Loader=yaml.FullLoader)

# import pprint
# pprint.pprint(transforms)


files = getFile("Select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])

newLayer = "transformed"

for file in files:
    f = OpenFont(file, showInterface=False)

    for g in f:
        if g.name in transforms.keys():

            g.layers[0].copyToLayer(newLayer, clear=True)

            # apparently, better than matching `width`
            g.getLayer(newLayer).leftMargin = g.layers[0].leftMargin
            g.getLayer(newLayer).rightMargin = g.layers[0].rightMargin

            transX, transY = transforms[g.name].split()[0].replace(",",""), transforms[g.name].split()[1]
            transX, transY = int(transX)/100, int(transY)/100

            g.getLayer(newLayer).transformBy((transX, 0, 0, transY, 0, 0), origin=(g.width/2, f.info.xHeight/2))

            # # if you don’t want things duplexed....
            # g.getLayer(newLayer).leftMargin = g.layers[0].leftMargin * transX
            # g.getLayer(newLayer).rightMargin = g.layers[0].rightMargin * transX

            # transform the layer width

            g.markColor = (0,0.5,1,0.25)

    # show 'transform' layer stroke, hide others


    f.save()
    f.close()

