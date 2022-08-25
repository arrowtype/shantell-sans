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
        # font.groups = coreGroups


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
        print(ungroupedGlyphs_side1)
        
        # exceptions on side1 are glyphs that are named without a group in side1 kern, but ARE also in a group
        exceptions_side1 = [i for i in kerns_side1 if 'public.kern' not in i and i not in ungroupedGlyphs_side1]
        print(exceptions_side1)


        # make a nested list of all glyphs in all groups used in side 1
        groups_side2 = [list(font.groups[groupName]) for groupName in [i for i in kerns_side2 if '.kern1' in i]]

        # flatten the nested list of all grouped side2 glyphs
        groupedGlyphs_side2 = [i for sublist in groups_side2 for i in sublist]

        # make list of glyphs in side2 kerns that are NOT in side2 groups
        ungroupedGlyphs_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i not in groupedGlyphs_side2]
        print(ungroupedGlyphs_side2)
        
        # exceptions on side2 are glyphs that are named without a group in side2 kern, but ARE also in a group
        exceptions_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i not in ungroupedGlyphs_side2]
        print(exceptions_side2)





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
