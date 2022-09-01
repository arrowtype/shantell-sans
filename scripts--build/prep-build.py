"""
    This script will...
    1. Copy main & organic sources to new folder, along with designspace files
    2. Duplicate normal sources & run a "bouncy" filter on these, updating file & style names
    3. Make alts of glyphs, interpolating organic & bouncy glyphs with main sources
    4. Add generated alts into kerning groups with their parents, to retain kerning in text
    5. Generate a contextual alternates (calt) feature to rotate through alts in text

    ASSUMPTIONS:
    → kerning groups all match glyph names in them (replacing "." with "_" in .case glyphs)
    → Many more. This is really for the Shantell Sans project only, though it could be adapted for others. 
    → See configuration below.

    USAGE:
    python3 scripts--build/prep-build.py
"""

import os
import shutil
from typing import Type
from fontParts.fontshell import RFont as Font
from ufonormalizer import normalizeUFO
from fontParts.world import *
from random import random
import math
from glyphsLib import GSFont, build_masters
import re

# --------------------------------------------------------
# START configuration

# the single source of truth
glyphsFile = "sources/build-prep/shantellsans-wght_ital_IRGL.glyphs"

releaseGlyphOrder = ".notdef space space.frac uni00A0 A Agrave Aacute Acircumflex Atilde Adieresis Aring Amacron Abreve Aogonek Acaron Aringacute Agravedbl Ainvertedbreve Adotbelow Ahoi Acircumflexacute Acircumflexgrave Acircumflexhoi Acircumflextilde Acircumflexdotbelow Abreveacute Abrevegrave Abrevehoi Abrevetilde Abrevedotbelow B C Ccedilla Cacute Ccircumflex Cdotaccent Ccaron D Dcaron E Egrave Eacute Ecircumflex Edieresis Emacron Ebreve Edotaccent Eogonek Ecaron Egravedbl Einvertedbreve Edotbelow Ehoi Etilde Ecircumflexacute Ecircumflexgrave Ecircumflexhoi Ecircumflextilde Ecircumflexdotbelow F G Gcircumflex Gbreve Gdotaccent uni0122 Gcaron H Hcircumflex I Igrave Iacute Icircumflex Idieresis Itilde Imacron Ibreve Iogonek Idotaccent Igravedbl Iinvertedbreve Ihoi Idotbelow J Jacute Jcircumflex K uni0136 L Lacute uni013B Lcaron M N Ntilde Nacute uni0145 Ncaron O Ograve Oacute Ocircumflex Otilde Odieresis Omacron Obreve Ohungarumlaut Ohorn Oogonek Ogravedbl Oinvertedbreve Odieresismacron Otildemacron Odotmacron Odotbelow Ohoi Ocircumflexacute Ocircumflexgrave Ocircumflexhoi Ocircumflextilde Ocircumflexdotbelow Ohornacute Ohorngrave Ohornhoi Ohorntilde Ohorndotbelow P Q R Racute uni0156 Rcaron Rgravedbl Rinvertedbreve S Sacute Scircumflex Scedilla Scaron Scommaaccent T Tcedilla Tcaron Tcommaaccent U Ugrave Uacute Ucircumflex Udieresis Utilde Umacron Ubreve Uring Uhungarumlaut Uogonek Uhorn Ucaron Ugravedbl Uinvertedbreve Udotbelow Uhoi Uhornacute Uhorngrave Uhornhoi Uhorntilde Uhorndotbelow V W Wcircumflex Wgrave Wacute Wdieresis X Y Yacute Ycircumflex Ydieresis Ymacron Ygrave Ydotbelow Yhoi Ytilde Z Zacute Zdotaccent Zcaron AE AEacute Eth Oslash Oslashacute Thorn Dcroat Hbar IJ IJacute Ldot Lslash Eng OE Tbar Schwa DZcaron LJ NJ Dzcaron Lj Nj Germandbls Omega a agrave aacute acircumflex atilde adieresis aring amacron abreve aogonek acaron aringacute agravedbl ainvertedbreve adotbelow ahoi acircumflexacute acircumflexgrave acircumflexhoi acircumflextilde acircumflexdotbelow abreveacute abrevegrave abrevehoi abrevetilde abrevedotbelow b c ccedilla cacute ccircumflex cdotaccent ccaron d dcaron e egrave eacute ecircumflex edieresis emacron ebreve edotaccent eogonek ecaron egravedbl einvertedbreve edotbelow ehoi etilde ecircumflexacute ecircumflexgrave ecircumflexhoi ecircumflextilde ecircumflexdotbelow f g gcircumflex gbreve gdotaccent uni0123 gcaron h hcircumflex i igrave iacute icircumflex idieresis itilde imacron ibreve iogonek igravedbl iinvertedbreve ihoi idotbelow j jcircumflex k uni0137 l lacute uni013C lcaron m n ntilde nacute uni0146 ncaron o ograve oacute ocircumflex otilde odieresis omacron obreve ohungarumlaut ohorn oogonek ogravedbl oinvertedbreve odieresismacron otildemacron odotmacron odotbelow ohoi ocircumflexacute ocircumflexgrave ocircumflexhoi ocircumflextilde ocircumflexdotbelow ohornacute ohorngrave ohornhoi ohorntilde ohorndotbelow p q r racute uni0157 rcaron rgravedbl rinvertedbreve s sacute scircumflex scedilla scaron scommaaccent t tcedilla tcaron tcommaaccent u ugrave uacute ucircumflex udieresis utilde umacron ubreve uring uhungarumlaut uogonek uhorn ucaron ugravedbl uinvertedbreve udotbelow uhoi uhornacute uhorngrave uhornhoi uhorntilde uhorndotbelow v w wcircumflex wgrave wacute wdieresis x y yacute ydieresis ycircumflex ymacron ygrave ydotbelow yhoi ytilde z zacute zdotaccent zcaron germandbls ae aeacute eth oslash oslashacute thorn dcroat hbar idotless ij ijacute kra ldot lslash eng oe tbar dzcaron lj nj schwa idotaccent jacute jdotless Djecyr Eukrcyr Dzecyr Iukrcyr Yukrcyr Jecyr Ljecyr Njecyr Tshecyr Dzhecyr Acyr Abrevecyr Adieresiscyr Becyr Vecyr Gecyr Gjecyr Decyr Iecyr Iegravecyr Iocyr Iebrevecyr Zhecyr Zhebrevecyr Zhedieresiscyr Zecyr Zedieresiscyr Icyr Igravecyr Ishortcyr Imacroncyr Idieresiscyr Kacyr Kjecyr Elcyr Emcyr Encyr Ocyr Odieresiscyr Pecyr Ercyr Escyr Tecyr Ucyr Ushortcyr Umacroncyr Udieresiscyr Uacutedblcyr Efcyr Hacyr Tsecyr Checyr Chedieresiscyr Shacyr Shchacyr Hardcyr Ylongcyr Ylongdieresiscyr Softcyr Ereversedcyr Yucyr Yacyr Yatcyr Yusbigcyr Fitacyr Izhitsacyr Geupcyr Gestrokecyr Gehookcyr Zhetailcyr Zetailcyr Katailcyr Kaverticalstrokecyr Kabashkcyr Entailcyr Engecyr Estailcyr Ustraightcyr Ustraightstrokecyr Xatailcyr Chetailcyr Chevertcyr Shhacyr Palochkacyr Chekhakascyr Aiecyr Schwacyr Obarcyr Getailcyr Qacyr Wecyr Ef-cy.loclBGR acyr abrevecyr adieresiscyr becyr vecyr gecyr gjecyr decyr iecyr iegravecyr iocyr iebrevecyr zhecyr zhebrevecyr zhedieresiscyr zecyr zedieresiscyr icyr ishortcyr igravecyr imacroncyr idieresiscyr kacyr kjecyr elcyr emcyr encyr ocyr odieresiscyr pecyr ercyr escyr tecyr ucyr ushortcyr umacroncyr udieresiscyr uacutedblcyr efcyr hacyr tsecyr checyr chedieresiscyr shacyr shchacyr hardcyr ylongcyr ylongdieresiscyr softcyr ereversedcyr yucyr yacyr djecyr eukrcyr dzecyr iukrcyr yukrcyr jecyr ljecyr njecyr tshecyr dzhecyr yatcyr yusbigcyr fitacyr izhitsacyr geupcyr gestrokecyr gehookcyr zhetailcyr zetailcyr katailcyr kaverticalstrokecyr kabashkcyr entailcyr engecyr estailcyr ustraightcyr ustraightstrokecyr xatailcyr chetailcyr chevertcyr shhacyr chekhakascyr palochkacyr aiecyr schwacyr obarcyr getailcyr qacyr wecyr yukrcyr_yukrcyr de-cy.loclBGR ge-cy.loclBGR iu-cy.loclBGR ka-cy.loclBGR pe-cy.loclBGR sha-cy.loclBGR shcha-cy.loclBGR te-cy.loclBGR tse-cy.loclBGR ve-cy.loclBGR ze-cy.loclBGR zhe-cy.loclBGR Esdescender-cy.loclBSH Ghestroke-cy.loclBSH Zedescender-cy.loclBSH esdescender-cy.loclBSH ghestroke-cy.loclBSH zedescender-cy.loclBSH be-cy.loclSRB Esdescender-cy.loclCHU esdescender-cy.loclCHU apostrophemod ordfeminine ordmasculine gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcmb dieresiscomb hookabovecmb ringcomb ringcomb.A hungarumlautcmb caroncomb gravedoublecmb invertedbrevecmb commaturnedabovecmb horncmb dotbelowcmb dieresisbelowcmb commaaccentbelowcmb cedillacomb ogonekcmb belowbrevecmb macronbelowcmb breveacutecomb brevecomb-cy brevegravecomb brevehookabovecomb brevetildecomb circumflexacutecomb circumflexgravecomb circumflexhookabovecomb circumflextildecomb dieresismacroncomb dotmacroncomb ringacutecomb tildemacroncomb overlaystrokeshortcmb zero one two three four five six seven eight nine period.tnum comma.tnum colon.tnum slash.tnum zero.dnom one.dnom two.dnom three.dnom four.dnom five.dnom six.dnom seven.dnom eight.dnom nine.dnom zero.numr one.numr two.numr three.numr four.numr five.numr six.numr seven.numr eight.numr nine.numr zero.pnum one.pnum two.pnum three.pnum four.pnum five.pnum six.pnum seven.pnum eight.pnum nine.pnum zero.inferior one.inferior two.inferior three.inferior four.inferior five.inferior six.inferior seven.inferior eight.inferior nine.inferior zero.superior four.superior five.superior six.superior seven.superior eight.superior nine.superior onesuperior twosuperior threesuperior onequarter onehalf threequarters onethird twothirds oneeighth threeeighths fiveeighths seveneighths underscore hyphen uni2010 endash emdash parenleft parenright bracketleft bracketright braceleft braceright bracketangleleft bracketangleright numbersign percent perthousand quotesingle quotedbl quoteleft quoteright quotedblleft quotedblright quotesinglbase quotedblbase guilsinglleft guilsinglright guillemetleft guillemetright asterisk dagger daggerdbl period comma colon semicolon ellipsis exclam exclamdown question questiondown slash backslash fraction bar brokenbar verticalbardbl at ampersand section paragraph litre numero periodcentered bullet openbullet minute second primemod primedblmod plus minus plusminus divide multiply equal less greater lessequal greaterequal approxequal notequal logicalnot emptyset estimated mu.math pi ohm commercialminussign arrowleft arrowup arrowright arrowdown arrowleftright arrowupdown partialdiff increment product summation divisionslash bulletoperator radical infinity integral dollar cent sterling currency yen colonmonetary lira naira won dong Euro fhook kip tugrik peso guarani hryvnia cedi tenge indianrupee turkishlira manat ruble thaibaht rupee newsheqel lari bitcoin asciicircum asciitilde acute grave hungarumlaut circumflex caron breve tilde macron dieresis dotaccent ring cedilla ogonek copyright registered trademark degree arrowNW arrowNE arrowSE arrowSW doublebarvertical gmtrdiamondblack gmtrdiamondwhite circlewhite circleblack squareblack squarewhite squaresmallblack squaresmallwhite triangleupblack triangleupwhite trianglerightblack trianglerightwhite triangledownblack triangledownwhite triangleleftblack triangleleftwhite triangleupsmallblack triangleupsmallwhite trianglerightsmallblack trianglerightsmallwhite triangledownsmallblack triangledownsmallwhite triangleleftsmallblack triangleleftsmallwhite heartwhite heartblack lozenge check checkheavy uni00AD hyphen.case endash.case emdash.case parenleft.case parenright.case bracketleft.case bracketright.case braceleft.case braceright.case bracketangleleft.case bracketangleright.case guilsinglleft.case guilsinglright.case guillemetleft.case guillemetright.case slash.case backslash.case at.case exclamdown.case questiondown.case periodcentered.case bullet.case openbullet.case periodcentered.loclCAT periodcentered.loclCAT_case f_f fi fl f_f_i f_f_l hyphen.line hyphen_line.3 hyphen_line.4 hyphen_line.5 hyphen_line.6 hyphen_line.7 hyphen_line.8 hyphen_line.9 hyphen_line.10 hyphen_line.11 hyphen_line.12 hyphen_line.13 hyphen_line.14 hyphen_line.15 hyphen_line.16 hyphen_line.17 hyphen_line.18 hyphen_line.19 hyphen_line.20 hyphen_line.21 hyphen_line.22 hyphen_line.23 hyphen_line.24 hyphen_line.25 hyphen_line.26 hyphen_line.27 hyphen_line.28 hyphen_line.29 hyphen_line.30 hyphen_line.31 hyphen_line.32 hyphen_line.33 hyphen_line.34 hyphen_line.35 hyphen_line.36 hyphen_line.37 hyphen_line.38 hyphen_line.39 hyphen_line.40 hyphen_line.41 hyphen_line.42 hyphen_line.43 hyphen_line.44 hyphen_line.45 hyphen_line.46 hyphen_line.47 hyphen_line.48 hyphen_line.49 hyphen_line.50".split(" ")

# directory to output UFOs converted from GlyphsApp source
ufosDir = 'sources/build-prep/ital_wght_IRGL--UFOs'

# where prepped UFOs are put
prepDir = 'sources/build-prep/ital_wght_BNCE_IRGL_TRAK--prepped'

# designspaces copied into prepped folder
designspaces = ["sources/shantell_sans-ital_wght_BNCE_IRGL_TRAK.designspace", "sources/shantell_sans-ital_wght_BNCE_IRGL_TRAK--static.designspace"]

# NOTE: if you really want *all* characters to have alts, use this instead. But it makes the font filesize quite a bit bigger. (Would need updating to include Cyrillics)       
# altsToMake = "AÀÁÂÃÄÅĀĂĄǍBCÇĆČDĎEÈÉÊËĒĔĘĚFGĞHIÌÍÎÏĪĬĮİJKLMNÑŃŇOÒÓÔÕÖŌŎŐPQRŔŘSŚŞŠTŤUÙÚÛÜŪŬŮŰŲǓVWXYÝŸZŹŻŽÆØǾĲŁŒΩaàáâãäåāăąǎbcçćčdďeèéêëēĕęěfgğhiìíîïīĭįjklmnñńňoòóôõöōŏőpqrŕřsśşštťuùúûüūŭůűųǔvwxyýÿzźżžßæÞðþẞ"

# letters to make alts for (all letters)
altsToMake = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzßæÞðþẞ"
altsToMake += "ÉéÓóÍíÁáÈèÜüÇçÃãÖöÄäÑñ"
altsToMake += "ЂЄЅІЇЈЉЊЋЏАБВГЃДЕЀЁЖЗИЍЙӢКЌЛМНОПРСТУЎӮФХЦЧШЩЪЫЬЭЮЯѢѲѴҐҒҖҚҢҮҰҲҶҺӀӘӨабвгѓдеѐёжзийѝӣкќлмнопрстуўӯфхцчшщъыьэюяђєѕіїјљњћџѣѳѵґғҗқңүұҳҷһӏәө"

# numbers & basic symbols
altsToMake += "0123456789!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~“”‘’"

# some glyphs just need to stick together or they look broken
glyphsToDecompose = "ij oe".split()

# adding because they trip up cu2qu in the build, likely because they are decomposed only in some generated sources
glyphsToDecompose += "arrowNE arrowNW arrowSW arrowSE invertedbrevecmb bracketangleright dotbelowcmb caroncomb".split()

# fontTools.varLib says these are incompatible, if they aren't decomposed first. See issue 
glyphsToDecompose += "Aring Yukrcyr Iocyr lj nj iocyr iukrcyr jecyr Lj Nj onequarter onehalf threequarters onethird twothirds oneeighth threeeighths fiveeighths seveneighths bulletoperator ijacute fi f_f_i Iigrave Esdescender esdescender periodcentered Iigrave-cy.loclBGR Esdescender-cy.loclBSH esdescender-cy.loclBSH Esdescender-cy.loclCHU esdescender-cy.loclCHU periodcentered.loclCAT_case".split()

glyphsToNotShift ="\
    onesuperior twosuperior threesuperior fraction zero.dnom one.dnom two.dnom three.dnom \
    four.dnom five.dnom six.dnom seven.dnom eight.dnom nine.dnom zero.numr one.numr two.numr \
    three.numr four.numr five.numr six.numr seven.numr eight.numr nine.numr zero.inferior \
    one.inferior two.inferior three.inferior four.inferior five.inferior six.inferior seven.inferior \
    eight.inferior nine.inferior zero.superior four.superior five.superior six.superior \
    seven.superior eight.superior nine.superior \
    gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcmb dieresiscomb \
    ringcomb hungarumlautcmb caroncomb dotbelowcmb cedillacomb acute grave hungarumlaut circumflex \
    caron breve tilde macron dieresis dotaccent ring cedilla ogonek ogonekcmb \
    hyphen.line hyphen_line.3 hyphen_line.4 hyphen_line.5 hyphen_line.6 hyphen_line.7 hyphen_line.8 hyphen_line.9 hyphen_line.10 hyphen_line.11 hyphen_line.12 hyphen_line.13 hyphen_line.14 hyphen_line.15 hyphen_line.16 hyphen_line.17 hyphen_line.18 hyphen_line.19 hyphen_line.20 hyphen_line.21 hyphen_line.22 hyphen_line.23 hyphen_line.24 hyphen_line.25 hyphen_line.26 hyphen_line.27 hyphen_line.28 hyphen_line.29 hyphen_line.30 hyphen_line.31 hyphen_line.32 hyphen_line.33 hyphen_line.34 hyphen_line.35 hyphen_line.36 hyphen_line.37 hyphen_line.38 hyphen_line.39 hyphen_line.40 hyphen_line.41 hyphen_line.42 hyphen_line.43 hyphen_line.44 hyphen_line.45 hyphen_line.46 hyphen_line.47 hyphen_line.48 hyphen_line.49 hyphen_line.50\
".split()

# total to add to TRAK axis
maxTracking = 500
trackedPath = "shantell_tracked--light.ufo"

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


def makeUFOsDir():
    if not os.path.exists(ufosDir):
        os.mkdir(ufosDir)


def convertGlyphs2UFO(glyphs_file, outputDir):

    # build UFOs from Glyphs source, using glyphsLib
    # also gets the output dict of source filenames, ufoLib2 Font objects
    sourceUfos = build_masters(
        glyphs_file,
        outputDir,
        write_skipexportglyphs=True,
        minimal=True,
    )[0]

    return sourceUfos


# make folder 'wght_bnce_dynm' & copy in sources
def makePrepDir(ufosDir, sourceUfos):
    if not os.path.exists(prepDir):
        os.mkdir(prepDir)

    for filename, font in sourceUfos.items():
        try:
            copyTo = prepDir+'/'+filename
            if not os.path.exists(copyTo):
                shutil.copytree(font.path, copyTo)
        except FileNotFoundError:
            pass

        # make bounce UFOs
        if font.info.styleName in ["Light","ExtraBold","Light Italic","ExtraBold Italic"]:
            bounceCopy = prepDir + '/' + filename.replace("shantell--","shantell_bounce--")
            if not os.path.exists(bounceCopy):
                shutil.copytree(font.path, bounceCopy)

        # make bounce-reverse UFOs
        if font.info.styleName in ["Light","ExtraBold","Light Italic","ExtraBold Italic"]:
            # we have to also format the names to find the other paths
            bounceReverseCopy = prepDir + '/' + filename.replace("shantell--","shantell_reverse_bounce--")
            if not os.path.exists(bounceReverseCopy):
                shutil.copytree(font.path, bounceReverseCopy)


def sortGlyphOrder(fonts):
    """
    Sorts all fonts in the list of *fonts* to have a common sort order.

    *fonts* is a `list` of font objects (Defcon or FontParts).
    """
    for font in fonts:
        ## The following works well for WIP fonts, but I’ve added configuration above (as a list) for a more-final build
        # newGlyphOrder = font.naked().unicodeData.sortGlyphNames(font.glyphOrder, sortDescriptors=[dict(type="cannedDesign", ascending=True, allowPseudoUnicode=True)])
        # # Trick here to put the .notdef first, as the cannedDesign sort puts it last, and it must be the first glyph in a font.
        # newGlyphOrder.insert(0, newGlyphOrder.pop())
        # font.glyphOrder = newGlyphOrder

        # setting the order to a list placed above, in the "configuration" area
        font.glyphOrder = releaseGlyphOrder

        font.save()


def decomposeDigraphs(fonts):
    for font in fonts:
        for g in font:
            if g.name in glyphsToDecompose:
                g.decompose()


def removeGlyphs(font, names):
    """
    Removes the glyphs in the list of *names* from the supplied *font*.
    This checks all layers for the glyph, removes the glyph from any
    composite glyphs that use it, removes the glyph from the `glyphOrder`,
    and removes the glyph from the kerning.

    *font* is a font object (Defcon or FontParts)
    *names* is a `list` of glyph names
    """

    for name in names:
        for layer in font.layers:
            if name in layer.keys():
                layer.removeGlyph(name)

    for glyph in font:
        if glyph.components:
            for component in glyph.components:
                if component.baseGlyph in names:
                    glyph.removeComponent(component)

    glyphOrder = font.glyphOrder
    for name in glyphOrder:
        if name in names:
            glyphOrder.remove(name)
    font.glyphOrder = glyphOrder

    for left, right in font.kerning.keys():
        if left in names or right in names:
            del font.kerning[(left, right)]


def clearGuides(font):
    """
    Clears both font level and glyph level guides in a font.

    *font* is a font object (Defcon or FontParts)
    """
    font.clearGuidelines()

    for glyph in font:
        if glyph.guidelines:
            glyph.clearGuidelines()


def makePrepFontsGlyphCompatible(fonts):
    """
    Compares the glyphs of all *fonts* and removes glyphs that are not
    common to all the provided *fonts*.

    *fonts* is a `list` of font objects (Defcon or FontParts).
    """

    # Get a list of all glyphs in each font, skipping "sparse" sources
    glyphSets = [font.keys() for font in fonts if "sparse" not in font.path]

    # Use set intersection to get all common glyph from each list
    commonGlyphs = set.intersection(*map(set, glyphSets))

    for font in fonts:
        clearGuides(font)
        if "sparse" not in font.path:
            removed = []
            for name in font.keys():
                if name not in commonGlyphs:
                    removed.append(name)
            if len(removed) != 0:
                removeGlyphs(font, removed)


def makeCompatible(fonts):
    """
    Checks all glyphs in *fonts* for compatibility. Removes any glyphs that
    aren't compatible from all of the fonts.

    *fonts* is a `list` of font objects (Defcon or FontParts).

    fontsToCheck assumes to "sparse" / support sources are compatible.
    """

    nonCompatible = []

    fontsToCheck = [font for font in fonts if "sparse" not in font.path]

    for glyph in fontsToCheck[0]:
        for font in fontsToCheck[1:]:
            if glyph.name in font.keys():
                compatibility = glyph.isCompatible(font[glyph.name])
                if not compatibility[0]:
                    nonCompatible.append((glyph.name, str(compatibility)))
            else:
                nonCompatible.append((glyph.name, "Missing in font"))

    for font in fontsToCheck:
        removeGlyphs(font, [name for name, _ in nonCompatible])


# make alts in all fonts
def makeAlts(fonts, numOfAlts=2):
    """
        Make alts for all glyphs in fonts.
        Argument 'numOfAlts' is the number of alts. 
        E.g. Default numOfAlts=2 would result in a, a.alt1, a.alt2, b, b.alt1, b.alt2, etc
    """

    altsToMakeGlyphNames = [g.name for g in fonts[0] if g.unicodes and g.unicodes[0] in altsToMakeList]


    for gname in altsToMakeGlyphNames:
        g = fonts[0][gname]
        for c in g.components:
            altsToMakeGlyphNames.append(c.baseGlyph)

    altsToMakeGlyphNames = list(set(altsToMakeGlyphNames))

    for font in fonts:

        layer = font.getLayer(font.defaultLayerName)

        newGlyphs = {}
        for glyph in font:
            # if glyph.unicodes and glyph.unicodes[0] in altsToMakeList:
            if glyph.name in altsToMakeGlyphNames:
                glyph.clearImage()
                # make alts
                for i, alt in enumerate(range(numOfAlts)):
                    glyphAltName = f"{glyph.name}.alt{i+1}"
                    glyphAlt = glyph.copy()
                    newGlyphs[glyphAltName] = layer[glyph.name]

        # mark new glyphs with colors
        for name,glyph in newGlyphs.items():
            layer[name] = glyph.copy()
            font[name].markColor = 0, 0, 1, 0.5
        
        font.save()

    return altsToMakeGlyphNames


def findMainBaseGlyphName(font, glyph):
    return [c.baseGlyph for c in glyph.components if font[c.baseGlyph].width >= 1][0]


def positiveOrNegative():
    return 1 if random() < 0.5 else -1


def italicBounceShift(yShift, font):
    """
        Return necessary x shift for a given y shift and italic angle.
    """

    if font.info.italicAngle == None or font.info.italicAngle == 0:
        return 0

    if abs(font.info.italicAngle) > 0:
        xShift = yShift * math.tan(math.radians(-font.info.italicAngle))

        if xShift is None:
            return 0
        else:
            return xShift


def makeBounce(font, glyph, randomLimit=100, minShift=50, factor=1):
    """
        Determine pseudo-random bounce, then move the glyph.

        Used if the font doesn't yet have a bounce dict to record prior bounce runs.
    """

    moveY=0

    # alt 1 → shift downwards
    if 'alt1' in glyph.name and glyph.name.split(".")[0]:
        moveY = round((randomLimit-minShift) * random() + minShift) * -1 * factor
        glyph.moveBy((italicBounceShift(moveY, font), moveY))

    # alt 2 → shift upwards
    if 'alt2' in glyph.name and glyph.name.split(".")[0]:
        moveY = round((randomLimit-minShift) * random() + minShift) * factor
        glyph.moveBy((italicBounceShift(moveY, font), moveY))

    # alt 3 or more → shift up or down by up to 66% (not necessarily needed)
    if 'alt' in glyph.name and \
        glyph.name.split(".")[0] and\
        'alt1' not in glyph.name and \
        'alt2' not in glyph.name:
        moveY = round((randomLimit-minShift) * random() + (minShift*0.66)) * positiveOrNegative() * factor # reduce shift other alt glyphs

        glyph.moveBy((italicBounceShift(moveY, font), moveY))

    # non-alt glyphs → shift up or down by up to 20%
    if 'alt' not in glyph.name and glyph.name:
        # moveY = round((randomLimit-minShift) * random() + minShift) * positiveOrNegative() * factor
        moveY = round((randomLimit-minShift) * random() + (minShift*0.2)) * positiveOrNegative() * factor # mostly remove minShift for default glyphs, so more are in the middle
        glyph.moveBy((italicBounceShift(moveY, font), moveY))

    if moveY == 0:
        pass

    return moveY


def recordBounceGlyphsApp(gsfont, glyphName, moveY):
    """
        Record generated pseudo-random bounces in GlyphsApp source.
    """

    mainMaster = [master for master in gsfont.masters if master.name == "ExtraBold"][0]
    glyphBounceDict = mainMaster.userData["com.arrowtype.glyphBounces"]

    try:
        glyphBounceDict[glyphName] = moveY
    except KeyError:
        glyphBounceDict = {}
        glyphBounceDict[glyphName] = moveY


def resetBounces(gsfont):
    """
        ONLY USE if you want to blow up the previously-set bounce values.

        Only use during active design, not afterward when repeating the build to refine/fix issues.
    """

    mainMaster = [master for master in gsfont.masters if master.name == "ExtraBold"][0]
    del mainMaster.userData["com.arrowtype.glyphBounces"]

    mainMaster.userData["com.arrowtype.glyphBounces"] = {}


def shiftGlyphs(font,gsfont,randomLimit=100,minShift=50,factor=1):
    """
        Shift glyphs in Bouncy sources.

        gsfont is a Glyphs source opened by glyphsLib.
    """

    glyphsToNotShift ="\
        onesuperior twosuperior threesuperior fraction zero.dnom one.dnom two.dnom three.dnom \
        four.dnom five.dnom six.dnom seven.dnom eight.dnom nine.dnom zero.numr one.numr two.numr \
        three.numr four.numr five.numr six.numr seven.numr eight.numr nine.numr zero.inferior \
        one.inferior two.inferior three.inferior four.inferior five.inferior six.inferior seven.inferior \
        eight.inferior nine.inferior zero.superior four.superior five.superior six.superior \
        seven.superior eight.superior nine.superior \
        gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcmb dieresiscomb \
        ringcomb hungarumlautcmb caroncomb dotbelowcmb cedillacomb acute grave hungarumlaut circumflex \
        caron breve tilde macron dieresis dotaccent ring cedilla ogonek ogonekcmb \
    ".split()

    # get glyphBounces dict from ExtraBold source
    mainMaster = [master for master in gsfont.masters if master.name == "ExtraBold"][0]
    glyphBounceDict = mainMaster.userData["com.arrowtype.glyphBounces"]

    if "bounce" in font.path:

        for g in font:
            if g.name not in glyphsToNotShift and len(g.components) == 0:

                moveY = 0

                try:
                    # try: look up bounce dict in the core extrabold master userData, use in this font
                    moveY = glyphBounceDict[g.name] * factor
                    g.moveBy((italicBounceShift(moveY, font),moveY))

                # y bounce not yet generated
                except KeyError:
                    # except KeyError: generate bounce value and add to the core extrabold master userData
                    moveY = makeBounce(font, g, randomLimit, minShift, factor)
                    recordBounceGlyphsApp(gsfont, g.name, moveY)

                # record shift in the glyph’s lib for later use
                g.lib['com.arrowtype.yShift'] = moveY

        # correct positioning of base glyphs in composed glyphs
        for g in font:

            if len(g.components) >= 1 and g.name.split(".")[0] not in glyphsToNotShift and g.name not in glyphsToNotShift:

                try:
                    try:
                        # look up Yshift of main baseGlyph
                        mainBase = findMainBaseGlyphName(font, g)
                    except IndexError:
                        # if base glyph is simply a zero-width combining accent, pass
                        # e.g. was failing on /belowbrevecmb
                        # TODO: check if /belowbrevecmb is causing or getting any problems
                        pass
                    baseShift = font[mainBase].lib['com.arrowtype.yShift']

                    # in multi-component glyphs, shift accents to match bases
                    if len(g.components) > 1:
                        for c in g.components:
                            if c.baseGlyph is not mainBase:
                                c.moveBy((0,baseShift))
                        # move glyph to normal position to "reset" it
                        g.moveBy((italicBounceShift(moveY, font),-baseShift))

                    #  correct single-component glyphs like oslash, lslash
                    else:
                        for c in g.components:
                            if c.baseGlyph is mainBase:
                                c.moveBy((0,-baseShift))
                except KeyError:
                    # if base glyph isn’t shifted, lib['com.arrowtype.yShift'] will fail
                    pass


                # move full glyph again # BUT WAIT, this just breaks it? ... does it need all components moved separately, rather than the whole thing moved?
                try:
                    moveY = glyphBounceDict[g.name] * factor
                    g.moveBy((italicBounceShift(moveY, font),moveY))
                except KeyError:
                    moveY = makeBounce(font, g, randomLimit, minShift, factor)
                    recordBounceGlyphsApp(gsfont, g.name, moveY)

                g.lib['com.arrowtype.yShift'] = moveY

        font.save()


def makeComponentsAlts(fonts, numOfAlts=2):
    """
       Set components to alt baseGlyphs – important for composed glyphs like i & j
    """
    for font in fonts:
        for glyph in font:
            if ".alt" in glyph.name and glyph.components:
                suffix = glyph.name.split(".")[-1]
                for c in glyph.components:
                    if ".alt" not in c.baseGlyph:
                        c.baseGlyph = c.baseGlyph + "." + suffix
                glyph.update()

        font.save()


def interpolateAlts(normalFont, organicFont, altsMadeForList):
    """
        Make partially-irregular glyphs in "organic" sources.
    """
    for g in organicFont:
        # if g.unicodes and g.unicodes[0] in altsToMakeList and 'alt' not in g.name:
        if g.name in altsMadeForList and '.alt' not in g.name:
            # interpolate alt1 10% towards organicFont glyph
            factor = 0.1
            organicFont[f'{g.name}.alt1'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            # interpolate alt2 66% towards organicFont glyph
            factor = 0.66
            organicFont[f'{g.name}.alt2'].interpolate(factor, normalFont[g.name], organicFont[g.name])

            try:
                # IF USING 3 alts (4 total versions of each glyph)
                # interpolate alt2 33% towards organicFont glyph
                factor = 0.33
                organicFont[f'{g.name}.alt3'].interpolate(factor, normalFont[g.name], organicFont[g.name])
            except:
                pass

    organicFont.save()


def removeAltUnicodes(fonts):
    """
        Make sure alts don’t have unicode values, which would be duplicates and probably cause problems.
    """
    for font in fonts:
        for g in font:
            if ".alt" in g.name:
                g.unicodes = []
        font.save()


def correctAccents(fonts):
    """
        In composed glyphs, fix alignment between accents and bases, using anchor positions & shift records
    """

    for font in fonts:
        for g in font:
            if len(g.components) >= 2:
                mainBase = findMainBaseGlyphName(font, g)
                accents = [c for c in g.components if c.baseGlyph != mainBase]

                # dict of anchors in main base, name:(x,y)
                mainBaseAnchors = {anchor.name:anchor.position for anchor in font[mainBase].anchors}

                for c in accents:
                    accentAnchors = font[c.baseGlyph].anchors
                    # dict of anchors in accent, but exlude non-underscored anchors
                    accentAnchors = {anchor.name.replace("_",""):anchor.position for anchor in font[c.baseGlyph].anchors if "_" in anchor.name}

                    commonAnchors = set(mainBaseAnchors.keys()).intersection(accentAnchors.keys())

                    if len(commonAnchors) == 0:
                        # if no common anchors, skip
                        pass
                    elif len(commonAnchors) == 1:

                        transformBefore = c.offset

                        commonAnchor = list(commonAnchors)[0]

                        mainBaseAnchorPos = mainBaseAnchors[commonAnchor]
                        accentBaseAnchorPos = accentAnchors[commonAnchor]

                        shiftX = mainBaseAnchorPos[0] - accentBaseAnchorPos[0]
                        
                        try:
                            # add bounce Y-shift in base & composed glyphs, if applicable
                            shiftY = mainBaseAnchorPos[1] - accentBaseAnchorPos[1] - font[mainBase].lib['com.arrowtype.yShift'] + g.lib['com.arrowtype.yShift']
                        except:
                            shiftY = mainBaseAnchorPos[1] - accentBaseAnchorPos[1]

                        
                        c.transformation = [1,0,0,1,shiftX,shiftY]

                        g.update()

                    else:
                        pass
                        # TODO check if this needs special handling; it probably does

        font.save()

    print()


def extendKerning(fonts):
    """
        Add .alt1 and .alt2 glyphs to kerning groups with defaults.

        Also handle kerning exceptions.
    """

    for font in fonts:

        alts = [g.name for g in font if '.alt' in g.name]
        altsMadeFor = sorted(list(set([name.split(".alt")[0] for name in alts])))

        # determine number of alts in font
        altSuffixes = set([altName.split('.alt')[1] for altName in alts])
        numOfAlts = len(altSuffixes)

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
        
        # # exceptions on side1 are glyphs that are named without a group in side1 kern, but ARE also in a group
        # exceptions_side1 = [i for i in kerns_side1 if 'public.kern' not in i and i in groupedGlyphs_side1]

        # make a nested list of all glyphs in all groups used in side 1
        groups_side2 = [list(font.groups[groupName]) for groupName in [i for i in kerns_side2 if '.kern2' in i]]

        # flatten the nested list of all grouped side2 glyphs
        groupedGlyphs_side2 = [i for sublist in groups_side2 for i in sublist]

        # make list of glyphs in side2 kerns that are NOT in side2 groups
        ungroupedGlyphs_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i not in groupedGlyphs_side2]
        
        # # exceptions on side2 are glyphs that are named without a group in side2 kern, but ARE also in a group
        # exceptions_side2 = [i for i in kerns_side2 if 'public.kern' not in i and i in groupedGlyphs_side2]

        # -------------------------------------------------------------------------
        # start duplicating kerns

        # go through kerning in font
        for kern in font.kerning.items():
            
            # each kern looks like (("A", "W"), -10) or (("public.kern1.y", "public.kern2.guillemetright"), 20), etc
            
            name = kern[0][0]
            if name in altsMadeFor:
                # make a new kern for each alt of the side1 glyph
                for i in range(1, numOfAlts+1):
                    newKern1 = ((f'{kern[0][0]}.alt{i}', kern[0][1]), kern[1])
                    font.kerning[newKern1[0]] = newKern1[1]

        # go through kerning in font a second time, once side1 is already duplicated
        for kern in font.kerning.items():
            
            # now extend the side 2 kerns
            name = kern[0][1]
            if name in altsMadeFor:
                # make a new kern for each alt of the side1 glyph
                for i in range(1, numOfAlts+1):
                    newKern2 = ((kern[0][0],f'{kern[0][1]}.alt{i}'), kern[1])
                    font.kerning[newKern2[0]] = newKern2[1]

        # next, add alt glyphs to parent groups

        # go through side1 kern glyphs that are in groups
        for glyphName in groupedGlyphs_side1:
            # if the glyphName has alts...
            if glyphName in altsMadeFor:
                # get its side1 group
                kernGroup = [groupName for groupName in font.groups.findGlyph(glyphName) if "kern1" in groupName][0]

                # then add each of its alts to that
                for i in range(1, numOfAlts+1):
                    font.groups[kernGroup] = font.groups[kernGroup] + (f'{glyphName}.alt{i}',)

        # go through side1 kern glyphs that are in groups
        for glyphName in groupedGlyphs_side2:
            # if the glyphName has alts...
            if glyphName in altsMadeFor:
                # get its side2 group
                kernGroup = [groupName for groupName in font.groups.findGlyph(glyphName) if "kern2" in groupName][0]

                # then add each of its alts to that
                for i in range(1, numOfAlts+1):
                    font.groups[kernGroup] = font.groups[kernGroup] + (f'{glyphName}.alt{i}',)

        # finally, make groups for glyphs that never had them
        
        # for side 1
        for glyphName in ungroupedGlyphs_side1:
            if glyphName in altsMadeFor:
                # make list of glyphnames for glyph plus alts
                glyphVersionNames = [glyphName] + [f"{glyphName}.alt{i}" for i in range(1, numOfAlts+1)]
                # make new group with glyph and alts in it
                font.groups[f'public.kern1.{glyphName.replace(".","_")}'] = [name for name in glyphVersionNames]

        # new groups for side 2
        for glyphName in ungroupedGlyphs_side2:
            if glyphName in altsMadeFor:
                # make list of glyphnames for glyph plus alts
                glyphVersionNames = [glyphName] + [f"{glyphName}.alt{i}" for i in range(1, numOfAlts+1)]
                # make new group with glyph and alts in it
                font.groups[f'public.kern2.{glyphName.replace(".","_")}'] = [name for name in glyphVersionNames]

        # go through kerning in font again, this time to update ungrouped glyphs with group names
        for kern in font.kerning.items():
            # start with side 1 kerns
            name = kern[0][0]
            if name in altsMadeFor and name in ungroupedGlyphs_side1:
                groupName = f'public.kern1.{name.replace(".","_")}'
                newKern1 = ((groupName, kern[0][1]), kern[1])
                del font.kerning[kern[0]]

                font.kerning[newKern1[0]] = newKern1[1]

        # repeat to make new group kerns for ungrouped side 2 kerns
        for kern in font.kerning.items():
            # now do side 2 kerns
            name = kern[0][1]
            if name in altsMadeFor and name in ungroupedGlyphs_side2:
                groupName = f'public.kern2.{name.replace(".","_")}'
                newKern2 = ((newKern1[0][0], groupName), newKern1[1])
                del font.kerning[kern[0]]

                font.kerning[newKern2[0]] = newKern2[1]

        font.save()


def generateCaltIntoFea(mainFont, glyphNames):
    """
        Generate OpenType calt code
    """

    glyphNames = sorted(glyphNames)

    # get feature code text from the  main UFO, passed in
    feaCode = mainFont.features.text

    # use regex to find whatever the existing calt code is, from the GlyphsApp source
    existingCaltFea = re.search(r"feature calt {(.+)} calt;", feaCode, re.DOTALL)
    existingCaltFeaFull = existingCaltFea.group()
    existingCaltFeaInside = existingCaltFea.group(1)

    newline = "\n"

    newCalt = "feature calt {"

    newCalt += existingCaltFeaInside

    # avoids setting biggest transformations at the start of words in Irregular/Flux styles
    # paradoxically, it tends to look *more* random to usually rotate through 3 versions per glyph than 4
    # then, the 4th version comes in handy to disrupt potentially repetition in a word like "EXPERIENCE"
    
    newCalt += f"""\

    @uppercaseMid = [{" ".join(name + '     ' for name in uppercase)}];
    @uppercaseLow = [{" ".join(name + '.alt1' for name in uppercase)}];
    @uppercaseHigh = [{" ".join(name + '.alt2' for name in uppercase)}];

    @lowercaseMid = [{" ".join(name + '     ' for name in lowercase)}];
    @lowercaseLow = [{" ".join(name + '.alt1' for name in lowercase)}];
    @lowercaseHigh = [{" ".join(name + '.alt2' for name in lowercase)}];

    @mid = [{" ".join(name + '     ' for name in glyphNames)}];
    @low = [{" ".join(name + '.alt1' for name in glyphNames)}];
    @high = [{" ".join(name + '.alt2' for name in glyphNames)}];

    sub @mid by @high;
    sub @high @high' by @mid;
    sub @mid @high' by @low;

    # basic order: high mid low high mid low - etc

    # prevent alt2 (high) from appearing three after alt2 uppercase
    {f"{newline}    ".join([f"sub {c}.alt2 @uppercaseMid @uppercaseLow {c}.alt2' by {c}.alt3;" for c in uppercase])}
    
    # prevent default (mid) from appearing three after default uppercase
    {f"{newline}    ".join([f"sub {c} @uppercaseLow @uppercaseHigh {c}' by {c}.alt3;" for c in uppercase])}
    
    # prevent alt1 (low) from appearing three after alt1 uppercase
    {f"{newline}    ".join([f"sub {c}.alt1 @uppercaseHigh @uppercaseMid {c}.alt1' by {c}.alt3;" for c in uppercase])}
    
    # prevent alt2 (high) from appearing three after alt2 lowercase
    {f"{newline}    ".join([f"sub {c}.alt2 @lowercaseMid @lowercaseLow {c}.alt2' by {c}.alt3;" for c in lowercase])}
    
    # prevent default (mid) from appearing three after default lowercase
    {f"{newline}    ".join([f"sub {c} @lowercaseLow @lowercaseHigh {c}' by {c}.alt3;" for c in lowercase])}
    
    # prevent alt1 (low) from appearing three after alt1 lowercase
    {f"{newline}    ".join([f"sub {c}.alt1 @lowercaseHigh @lowercaseMid {c}.alt1' by {c}.alt3;" for c in lowercase])}
    """

    newCalt += "} calt;"

    newFeaCode = feaCode.replace(existingCaltFeaFull, newCalt)

    return newFeaCode


def addFeaCode(fonts, newFeatures):
    """
        Add updated, extended feature code to generated UFOs
    """

    for font in fonts:
        font.features.text = newFeatures
        font.save()

# ------------------------------------------
# begin creating tracked UFO below

def decomposeScaledFlippedComp(font):
    """
        Just in case this isn’t already done, decompose any scaled or flipped components.
    """

    for glyph in font:

        if not glyph.components:
            return
        for component in glyph.components:
            if component.transformation[0] != 1 or component.transformation[3] != 1:
                component.decompose()
    
    font.save()


def addEqualMargin(glyph, margin):
    """
        Add equal margin to a given Rglyph object.
    """
    if glyph.width == 0:
        return
    try:
        glyph.leftMargin = glyph.leftMargin + margin
        glyph.rightMargin = glyph.rightMargin + margin
    except TypeError:
        glyph.width = glyph.width + (margin*2)


def correctComponents(font,glyph, margin):
    """
        Corrects components for a given margin
    """
    if not glyph.components:
        return
    for component in glyph.components:
        if font[component.baseGlyph].width != 0:
            component.moveBy((-margin, 0))


def makeTrackedUFO(font, tracking):
    """
        Take in a font object and add tracking to all glyphs.
    """

    for glyph in font:

        margin = tracking/2

        addEqualMargin(glyph, margin)

        # move component left by margin amount
        correctComponents(font,glyph, margin)
    
    font.save(prepDir + '/' + trackedPath)

# end creating tracked UFO
# ------------------------------------------

def setLibKeys(font):
    """
        Set lib keys for proper ufo2ft processing during build.
    """

    # set this or it trips up ufoLib
    font.defaultLayer.name = "foreground"

    # un-nest nested components # https://github.com/googlefonts/fontbakery/issues/296
    font.lib["com.github.googlei18n.ufo2ft.filters"] = [
            {
            'name': 'decomposeTransformedComponents', 
            'pre': 1
            },
            {
            'name': 'flattenComponents', 
            'pre': 1
            }
    ]

    font.save()


def main():

    # opening glyphs source in memory
    gsfont =  GSFont(glyphsFile)
    
    # clean up previous run
    if os.path.exists(ufosDir):
        shutil.rmtree(ufosDir,ignore_errors=True)

    # convert UFOs from glyphs source
    print(f"🤖 Generating UFO fonts to {ufosDir}")
    sourceUfos = convertGlyphs2UFO(glyphsFile, ufosDir)

    # The setup
    if os.path.exists(prepDir):
        shutil.rmtree(prepDir,ignore_errors=True)

    # ONLY DO THE FOLLOWING IF YOU WANT TO COMPLETELY SHIFT/CHANGE BOUNCY STYLES
    # print("🤖 Resetting bounce randomization in sources")
    # resetBounces(gsfont)

    print(f"🤖 Copying fonts to {prepDir}")
    makePrepDir(ufosDir, sourceUfos)
    newFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.ufo' in path]

    print("🤖 Opening fonts")
    fonts = [Font(path) for path in newFontPaths]

    # The sausage making

    print("🤖 Making source fonts compatible (removing unique glyphs, etc)")
    makePrepFontsGlyphCompatible(fonts) # makes glyph sets the same in prepped fonts
    makeCompatible(fonts)               # basic check for glyphs that aren’t compatible (useful but imperfect for VFs, as it relies on FontParts .isCompatible method)

    print("🤖 Decomposing digraphs")
    decomposeDigraphs(fonts)

    print("🤖 Making alts")
    altsMadeForList = makeAlts(fonts, numOfAlts=3)

    print("🤖 Making composed alts point to alt components")
    makeComponentsAlts(fonts)

    # shift alts in bounce fonts
    print("🤖 Shifting bouncy alts")
    for font in fonts:
        if "bounce" in font.path and "reverse_bounce" not in font.path:
            shiftGlyphs(font, gsfont, factor=1) # factor 1 makes moves of up to 100 units
    
    # split into separate loop so reverse sources always go second
    for font in fonts:
        if "reverse_bounce" in font.path:
            print("reverse bounces for ", font.path)
            shiftGlyphs(font, gsfont, factor=-1) # factor -1 makes moves of up to -100 units

    # save any bounce values recorded into Glyphs source
    gsfont.save(glyphsFile)

    # interpolate alts in irregular fonts
    print("🤖 Interpolating organic alts")

    # Dumb setup. Will it work?
    # TODO: interpolate alts in italics
    interpolateAlts([f for f in fonts if "shantell--light.ufo" in f.path][0], [f for f in fonts if "organic--light.ufo" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--extrabold.ufo" in f.path][0], [f for f in fonts if "organic--extrabold.ufo" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--light_italic.ufo" in f.path][0], [f for f in fonts if "organic--light_italic.ufo" in f.path][0], altsMadeForList)
    interpolateAlts([f for f in fonts if "shantell--extrabold_italic.ufo" in f.path][0], [f for f in fonts if "organic--extrabold_italic.ufo" in f.path][0], altsMadeForList)


    # yes, this is needed twice. Once to make shifting work well, then again to make irregular sources compatible again after interpolation
    print("🤖 Making composed alts point to alt components – repeating to fix irregular sources")
    makeComponentsAlts(fonts)

    print("🤖 Removing unicodes from alt glyphs")
    removeAltUnicodes(fonts)

    print("🤖 Fixing accent positions")
    correctAccents(fonts)
    
    print("🤖 Tying alts to default glyph kerning")
    extendKerning(fonts)

    print("🤖 Generating calt feature")
    # the Light source contains features from the GlyphsApp source
    mainFont = [font for font in fonts if "shantell--light.ufo" in font.path][0]
    # let’s add newly-generated calt code to it!
    newFeatures = generateCaltIntoFea(mainFont,altsMadeForList)

    print("🤖 Updating feature code")
    addFeaCode(fonts, newFeatures)

    print("🤖 Copying Designspace file")
    for ds in designspaces:
        shutil.copyfile(ds, prepDir+'/'+os.path.split(ds)[1])

    print("🤖 Sorting fonts")
    sortGlyphOrder(fonts)

    print("🤖 Decompose scaled or flipped components")
    for font in fonts:
        decomposeScaledFlippedComp(font)

    print("🤖 Making tracked font")
    for font in fonts:
        if "light" in font.path and "bounce" not in font.path:
            makeTrackedUFO(font, maxTracking)

    # grabbing the new list of prepped fonts to set ufo2ft lib keys as needed
    preppedFontPaths = [os.path.join(prepDir, path) for path in os.listdir(prepDir) if '.ufo' in path]
    preppedFonts = [Font(path) for path in preppedFontPaths]

    print("🤖 Correcting font lib keys for ufo2ft filters")
    for font in preppedFonts:
        setLibKeys(font)



if __name__ == "__main__":
    main()
