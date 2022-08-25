"""
    A script made to figure out how to extend kerning properly for alts generated in the Shantell Sans build prep process.

    Will ultimately be worked back into the main build-prep.py script.
"""

import shutil
from fontParts.fontshell import RFont as Font
from fontParts.world import *

# --------------------------------------------------------
# START configuration

# directory to output UFOs converted from GlyphsApp source
ufoToEdit = 'sources/build-prep/ital_wght_BNCE_IRGL_TRAK--prepped/shantell--light.ufo'
ufoToMake = 'sources/build-prep/ital_wght_BNCE_IRGL_TRAK--prepped/shantell--light-extended_kerning.ufo'

# letters to make alts for (all letters)
altsToMake = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzßæÞðþẞ"
altsToMake += "ÉéÓóÍíÁáÈèÜüÇçÃãÖöÄäÑñ"
altsToMake += "ЂЄЅІЇЈЉЊЋЏАБВГЃДЕЀЁЖЗИЍЙӢКЌЛМНОПРСТУЎӮФХЦЧШЩЪЫЬЭЮЯѢѲѴҐҒҖҚҢҮҰҲҶҺӀӘӨабвгѓдеѐёжзийѝӣкќлмнопрстуўӯфхцчшщъыьэюяђєѕіїјљњћџѣѳѵґғҗқңүұҳҷһӏәө"

# numbers & basic symbols
altsToMake += "0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”‘’"

# END configuration
# --------------------------------------------------------

# add just the basic upper & lowercase (used later in the calt code generator)
uppercase = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" ")
lowercase = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")

# add Cyrillic basic upper & lowercase
uppercase += "Djecyr Eukrcyr Dzecyr Iukrcyr Yukrcyr Jecyr Ljecyr Njecyr Tshecyr Dzhecyr Acyr Becyr Vecyr Gecyr Gjecyr Decyr Iecyr Iegravecyr Iocyr Zhecyr Zecyr Icyr Igravecyr Ishortcyr Imacroncyr Kacyr Kjecyr Elcyr Emcyr Encyr Ocyr Pecyr Ercyr Escyr Tecyr Ucyr Ushortcyr Umacroncyr Efcyr Hacyr Tsecyr Checyr Shacyr Shchacyr Hardcyr Ylongcyr Softcyr Ereversedcyr Yucyr Yacyr Yatcyr Fitacyr Izhitsacyr Geupcyr Gestrokecyr Zhetailcyr Katailcyr Entailcyr Ustraightcyr Ustraightstrokecyr Xatailcyr Chetailcyr Shhacyr Palochkacyr Schwacyr Obarcyr".split(" ")
lowercase += "acyr becyr vecyr gecyr gjecyr decyr iecyr iegravecyr iocyr zhecyr zecyr icyr ishortcyr igravecyr imacroncyr kacyr kjecyr elcyr emcyr encyr ocyr pecyr ercyr escyr tecyr ucyr ushortcyr umacroncyr efcyr hacyr tsecyr checyr shacyr shchacyr hardcyr ylongcyr softcyr ereversedcyr yucyr yacyr djecyr eukrcyr dzecyr iukrcyr yukrcyr jecyr ljecyr njecyr tshecyr dzhecyr yatcyr fitacyr izhitsacyr geupcyr gestrokecyr zhetailcyr katailcyr entailcyr ustraightcyr ustraightstrokecyr xatailcyr chetailcyr shhacyr palochkacyr schwacyr obarcyr".split(" ")

# get integer unicode values for string of characters from above
altsToMakeList = [ord(char) for char in altsToMake]



def extendKerning(fonts,numOfAlts=2):
    """
        Add .alt1 and .alt2 glyphs to kerning groups with defaults.
    """

    # first, copy groups from main font
    # coreGroups = Font(sources["extrabold"]).groups

    for font in fonts:

        # ? replace this variable with an arg in the main build prep script
        alts = [g.name for g in font if '.alt' in g.name]
        altsMadeFor = sorted(list(set([name.split(".alt")[0] for name in alts])))

        # -------------------------------------------------------------------------
        # parse out lists of side1 and side2 grouped kerns vs exception kerns

        # make list of all glyphs with any kerning
        kerning = font.kerning.keys()
        kerns_side1 = set([pair[0] for pair in kerning])
        kerns_side2 = set([pair[1] for pair in kerning])

        # make a nested list of all glyphs in all groups used in side 1
        groups_side1 = [list(font.groups[groupName]) for groupName in [i for i in kerns_side1 if '.kern1' in i]]

        # flatten the nested list of all grouped side1 glyphs
        groupedGlyphs_side1 = [i for sublist in groups_side1 for i in sublist]

        # make list of glyphs in side1 kerns that are NOT in side1 groups
        ungroupedGlyphs_side1 = [i for i in kerns_side1 if 'public.kern' not in i and i not in groupedGlyphs_side1]
        # print(ungroupedGlyphs_side1)
        
        # exceptions on side1 are glyphs that are named without a group in side1 kern, but ARE also in a group
        exceptions_side1 = [i for i in kerns_side1 if 'public.kern' not in i and i in groupedGlyphs_side1]
        # print(exceptions_side1)

        # make a nested list of all glyphs in all groups used in side 1
        groups_side2 = [list(font.groups[groupName]) for groupName in [i for i in kerns_side2 if '.kern2' in i]]
        # print(groups_side2)
        # print()

        # flatten the nested list of all grouped side2 glyphs
        groupedGlyphs_side2 = [i for sublist in groups_side2 for i in sublist]
        # print(groupedGlyphs_side2)
        # print()

        # make list of glyphs in side2 kerns that are NOT in side2 groups
        ungroupedGlyphs_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i not in groupedGlyphs_side2]
        # print(ungroupedGlyphs_side2)
        # print()
        
        # exceptions on side2 are glyphs that are named without a group in side2 kern, but ARE also in a group
        exceptions_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i in groupedGlyphs_side2]
        # print(exceptions_side2)

        # -------------------------------------------------------------------------
        # start duplicating kerns
        
        counterBoth = 0
        counterSide1Only = 0
        counterSide2Only = 0

        # go through kerning in font
        for kern in font.kerning.items():
            
            # this goes through the glyphs in each item, which each look like (("A", "W"), -10) or (("public.kern1.y", "public.kern2.guillemetright"), 20), etc
            for side, name in enumerate(kern[0], start=1):

                if side == 1:
                    if name in altsMadeFor:
                        # make a new kern for each alt of the side1 glyph
                        for i in range(1, numOfAlts+1):
                            newKern1 = ((f'{kern[0][0]}.alt{i}', kern[0][1]), kern[1])
                            font.kerning[newKern1[0]] = newKern1[1]

        # go through kerning in font a second time, once side1 is already duplicated
        for kern in font.kerning.items():
            
            # this goes through the glyphs in each item, which each look like (("A", "W"), -10) or (("public.kern1.y", "public.kern2.guillemetright"), 20), etc
            for side, name in enumerate(kern[0], start=1):
                if side == 2:
                    if name in altsMadeFor:
                        # make a new kern for each alt of the side1 glyph
                        for i in range(1, numOfAlts+1):
                            newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                            font.kerning[newKern2[0]] = newKern2[1]


                    # if side == 2:
                    #     # make a new kern for each alt of the side1 glyph
                    #     for i in range(1, numOfAlts+1):
                    #         newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                    #         font.kerning[newKern2[0]] = newKern2[1]

                # # if both sides are an exception and have alts
                # if name in exceptions_side2 and name in exceptions_side1 and name in altsMadeFor:
                #     counterBoth += 1 # for debugging

                #     if side == 1:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern1 = ((f'{kern[0][0]}.alt{i}', kern[0][1]), kern[1])
                #             font.kerning[newKern1[0]] = newKern1[1]

                #     if side == 2:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                #             font.kerning[newKern2[0]] = newKern2[1]

                # # if right side only is an exception (should this be first, before both side exceptions?)
                # elif name in exceptions_side2 and name in altsMadeFor:
                #     counterSide2Only += 1 # for debugging
                #     if side == 1:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern1 = ((f'{kern[0][0]}.alt{i}', kern[0][1]), kern[1])
                #             font.kerning[newKern1[0]] = newKern1[1]

                #     if side == 2:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                #             font.kerning[newKern2[0]] = newKern2[1]


                # # if left side only is an exception
                # elif name in exceptions_side1 and name in altsMadeFor:
                #     counterSide1Only += 1 # for debugging
                #     if side == 1:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern1 = ((f'{kern[0][0]}.alt{i}', kern[0][1]), kern[1])
                #             font.kerning[newKern1[0]] = newKern1[1]

                #     if side == 2:
                #         # make a new kern for each alt of the side1 glyph
                #         for i in range(1, numOfAlts+1):
                #             newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                #             font.kerning[newKern2[0]] = newKern2[1]

        print('counterBoth', counterBoth)
        print('counterSide1Only', counterSide1Only)
        print('counterSide2Only', counterSide2Only)

        # TODO: WHAT IF an exception is an exception on both sides? You don't want to dulicate the logic...

        # probably, make a list of both-sided exceptions, then lists of side1 or side2-only exceptions?
        # or check for unique items in lists?

        # OR... you could assume that exceptions will always be both-sided... but maybe that is a last-resort, as it will break eventually






        # for glyphName in altsMadeForList:
        #     glyphBaseName = glyphName.split(".alt")[0]

        #     if glyphBaseName in exceptions_side2:
                
                # look up kerning on non-alt
                # baseKern = 

                # newKern2 = ((THING, glyphName), kern[1])






        font.save()


def main():

    print("🤖 Clear previous run and duplicate starter font again")
    shutil.rmtree(ufoToMake)
    shutil.copytree(ufoToEdit, ufoToMake)

    print("🤖 Opening new font")
    newFont = Font(ufoToMake)

    newFont.save()

    # just making a single-item list to simulate this part
    fonts = [newFont]
    
    print("🤖 Tying alts to default glyph kerning")
    extendKerning(fonts, numOfAlts=3) 




if __name__ == "__main__":
    main()
