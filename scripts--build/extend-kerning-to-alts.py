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
        kernedGlyphs = set([glyphName for pair in kerning for glyphName in pair])

        # then, add alt glyphs into the groups of default glyphs
        for g in font:
            # get glyph’s base name pre-suffix if it is a generated "alt", but otherwise use the whole name
            # get base name if glyph has suffix .alt1, etc
            if "." in g.name and "alt" in g.name.split(".")[1]:
                glyphBaseName = g.name.split(".")[0] 
            else:
                glyphBaseName = g.name


            # check what kern groups font[glyphBaseName] is in
            kernGroups = [groupName for groupName in font.groups.findGlyph(glyphBaseName) if "kern" in groupName]
            
            for kernGroup in kernGroups:
                if g.name not in font.groups[kernGroup]:
                    font.groups[kernGroup] = font.groups[kernGroup] + (g.name,)

            # handle case if glyph is *not* in a kerning group already

            # if glyph is in no kerning groups yet
            if kernGroups == []:
                # check if glyphBaseName has any kerning
                if glyphBaseName in kernedGlyphs:
                    # make group names, handling .case suffixes
                    kern1 = f'public.kern1.{glyphBaseName.replace(".","_")}'
                    kern2 = f'public.kern2.{glyphBaseName.replace(".","_")}'

                    # make list of glyph plus alts
                    glyphVersionNames = [glyphBaseName] + [glyphBaseName + f".alt{i+1}" for i in range(numOfAlts)]

                    # make list of glyphBaseName plus glyphBaseName.alt1, alt2, etc
                    font.groups[kern1] = [name for name in glyphVersionNames]
                    font.groups[kern2] = [name for name in glyphVersionNames]

        for kern in font.kerning.items():
            newKern = ()
            newKern1 = ()
            newKern2 = ()
            
            # this goes through the glyphs in each item, which each look like (("A", "W"), -10) or (("public.kern1.y", "public.kern2.guillemetright"), 20), etc
            for i, name in enumerate(kern[0]):
                side = i+1

                # if side kern is not a group already...
                if "public.kern" not in name:
                    # if the glyph is not in group(s)...
                    if kernGroups != []:
                        # make new kern with side1 set to group
                        if side == 1:
                            # make new group name, dealing with suffixed glyph names like /slash.case
                            groupName = f'public.kern1.{name.replace(".","_")}'
                            newKern1 = ((groupName, kern[0][1]), kern[1])

                            del font.kerning[kern[0]]

                            font.kerning[newKern1[0]] = newKern1[1]
                        
                        # make new kern with side2 set to group
                        if side == 2:

                            groupName = f'public.kern2.{name.replace(".","_")}'

                            # if a newKern1 was not made
                            try:
                                newKern2 = ((kern[0][0], groupName), kern[1])
                                del font.kerning[kern[0]]

                            # if a newKern1 was made for side 1
                            except (KeyError, IndexError):
                                newKern2 = ((newKern1[0][0], groupName), newKern1[1])
                                del font.kerning[newKern1[0]]

                            font.kerning[newKern2[0]] = newKern2[1]

        # TODO: limit kern extensions to only glyphs that get alternates

        # TODO: check if base glyph has exceptions, then give the alt glyphs the same exceptions. Issue #111.
        # exceptions can be on one or both sides: https://unifiedfontobject.org/versions/ufo3/kerning.plist/#exceptions
        # (it seems) the side1 of an exception is just a glyphname, e.g.      <key>T</key>
        # (it seems) the side2 of an exception is also just a glyphname, e.g. <key>y</key>
        # so, maybe...?:
            # start by making a dict of all exceptions
            # for each key that *doesn't* include kern1 or kern2
                # duplicate each key within it, for each alt
                # then, duplicate the top-level key
            # then add these extended exceptions back into the data
        # but first, figure out: why


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
