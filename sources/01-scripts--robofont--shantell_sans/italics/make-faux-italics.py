"""
    [WORK IN PROGRESS – works pretty well, but could use a few more improvements.]

    A script to take the sources of Shantell Sans and output slanted versions of these, 
    for the purposes of A) prototyping & B) jumpstarting the italic drawings.

    Copies selected UFOs to an italic path, then:

    1. Slants glyphs at a selected angle
    2. Slant round glyphs by less – maybe 7 degrees
    3. Adds extreme points only if you want (or any points)

    Suggested angles (calculated with tangent, but really with http://www.carbidedepot.com/formulas-trigright.asp):
    -  9.46  (up 6, over 1)
    - 11.31 (up 5, over 1)
    - 14.04 (up 4, over 1)
    
    Based largely on the Slanter extension:
    https://github.com/roboDocs/slanterRoboFontExtension/blob/57d7ac8ad9c91b0dce480cccb5a5dc2d4d4c51c4/Slanter.roboFontExt/lib/slanter.py

"""

from vanilla import *
from vanilla.dialogs import getFile
from math import radians
from fontTools.misc.transform import Transform
from mojo.roboFont import CurrentGlyph, CurrentFont, RGlyph, RPoint
import os
import shutil
import math
from mojo.UI import OutputWindow

# ------------------------------
# set preferences below

openNewFonts = True
saveNewFonts = True
addExtremesToNewFonts = False

outputFolder = "italics--generated"

italicAngle = 11.31 # (Clockwise is positive, here.) this will be flipped to negative when entered into font info
setSkew = italicAngle
setRotation = 0
# ucRounds = "B C D G J O P R S U OE Ohorn Omega IJ zero two three five six eight nine zero.onum two.onum three.onum five.onum six.onum eight.onum nine.onum percent perthousand at ampersand section dollar cent sterling Euro copyright degree dollar.open cent.open question questiondown C.RECT D.RECT G.RECT O.RECT P.RECT R.RECT U.RECT OE.RECT Ohorn.RECT Germandbls.RECT R.grot two.tnum three.tnum five.tnum two.onum_tnum D.sups G.sups O.sups R.sups S.sups a.sups d.sups e.sups g.sups h.sups m.sups n.sups o.sups s.sups u.sups U.sups brevecomb ringcomb partialdiff infinity registered two.onum_tnum three.onum_tnum five.onum_tnum asterisk".split(" ")
# lcRounds = "a b c d e g m n o p q s u ohorn a.italic g.text germandbls ae eth oe germandbls.alt zero.dnom two.dnom three.dnom five.dnom six.dnom eight.dnom nine.dnom".split(" ")
ucRounds = "".split(" ")
lcRounds = "".split(" ")
# TODO: check on whether to add additional category for small, high-up glyphs: "D.sups G.sups O.sups R.sups S.sups a.sups d.sups e.sups g.sups h.sups m.sups n.sups o.sups s.sups u.sups U.sups"
rounds = ucRounds + lcRounds
roundRotatation = 0
roundSkew = italicAngle - roundRotatation

# TODO: translate rounds to keep proper sidebearings/spacing

dialogMessage = f"Select UFOs to generate as faux italics in {outputFolder}"

# ------------------------------

# Open output window to show user that work is being done
OutputWindow().show()

print("\n---------------------------------\n\n🤖 Beep boop, I’m 'make-faux-italics.py'\n")
print("🤖 Please select some upright UFOs to get started!\n")

# Function mostly copied from the Slanter extension
def getGlyph(glyph, font, skew, rotation, addComponents=False, skipComponents=False, addExtremes=False):
    skew = radians(skew)
    rotation = radians(-rotation)

    # To solve: "ValueError: Guideline names must be at least one character long."
    for guideline in glyph.guidelines:
        try:
            if guideline.name != "":
                pass
        except ValueError:
            glyph.clearGuidelines()


    dest = glyph.copy()

    if not addComponents:
        for component in dest.components:
            pointPen = DecomposePointPen(glyph.layer, dest.getPointPen(), component.transformation)
            component.drawPoints(pointPen)
            dest.removeComponent(component)

    for contour in list(dest):
        if contour.open:
            dest.removeContour(contour)

    if skew == 0 and rotation == 0:
        return dest

    for contour in dest:
        for bPoint in contour.bPoints:
            bcpIn = bPoint.bcpIn
            bcpOut = bPoint.bcpOut
            if bcpIn == (0, 0):
                continue
            if bcpOut == (0, 0):
                continue
            if bcpIn[0] == bcpOut[0] and bcpIn[1] != bcpOut[1]:
                bPoint.anchorLabels = ["extremePoint"]
            if rotation and bcpIn[0] != bcpOut[0] and bcpIn[1] == bcpOut[1]:
                bPoint.anchorLabels = ["extremePoint"]

    cx, cy = 0, 0
    box = glyph.bounds
    if box:
        cx = box[0] + (box[2] - box[0]) * .5
        cy = box[1] + (box[3] - box[1]) * .5
        # cy = font.info.xHeight * 0.5

    t = Transform()
    t = t.skew(skew)
    t = t.translate(cx, cy).rotate(rotation).translate(-cx, -cy)

    if not skipComponents:
        dest.transformBy(tuple(t))
    else:
        for contour in dest.contours:
            contour.transformBy(tuple(t))

        # this seems to work !!!
        for component in dest.components:
            # get component center
            _box = glyph.layer[component.baseGlyph].bounds
            if not _box:
                continue
            _cx = _box[0] + (_box[2] - _box[0]) * .5
            _cy = _box[1] + (_box[3] - _box[1]) * .5
            # calculate origin in relation to base glyph
            dx = cx - _cx
            dy = cy - _cy
            # create transformation matrix
            tt = Transform()
            tt = tt.skew(skew)
            tt = tt.translate(dx, dy).rotate(rotation).translate(-dx, -dy)
            # apply transformation matrix to component offset
            P = RPoint()
            P.position = component.offset
            P.transformBy(tuple(tt))
            # set component offset position
            component.offset = P.position

    # check if "add extremes" is set to True
    if addExtremes:
        dest.extremePoints(round=0)
        for contour in dest:
            for point in contour.points:
                if "extremePoint" in point.labels:
                    point.selected = True
                    point.smooth = True
                else:
                    point.selected = False

    dest.removeSelection()
    dest.round()
    return dest


# Function adapted from the Slanter extension
def generateFont(fontToCopy):

    outFont = RFont(showInterface=False)
    outFont.info.update(fontToCopy.info.asDict())
    outFont.features.text = fontToCopy.features.text

    outFont.info.italicAngle = -italicAngle

    for glyph in fontToCopy:
        outFont.newGlyph(glyph.name)
        outGlyph = outFont[glyph.name]
        outGlyph.width = glyph.width
        outGlyph.unicodes = glyph.unicodes

        if glyph.name not in rounds:
            resultGlyph = getGlyph(glyph, font, setSkew, setRotation, addComponents=True, skipComponents=True, addExtremes=addExtremesToNewFonts)
        else:
            resultGlyph = getGlyph(glyph, font, roundSkew, roundRotatation, addComponents=True, skipComponents=True, addExtremes=addExtremesToNewFonts)

        outGlyph.appendGlyph(resultGlyph)

    # copy glyph order
    outFont.templateGlyphOrder = fontToCopy.templateGlyphOrder

    # copy groups & kerning
    outFont.groups.update(fontToCopy.groups.asDict())
    outFont.kerning.update(fontToCopy.kerning.asDict())

    # quick/lazy update to relative feature link
    if "sparse" not in fontToCopy.path:
        outFont.features.text = "include(../../features/features.fea);"

    outFont.info.styleName = outFont.info.styleName + " Italic"



    return outFont


def fixRoundOffset(font, ucRoundBasis="O", lcRoundBasis="o", roundOffset=False):
    """
        Fix horizontal position of rounded glyphs, based on centering O and o.
    """

    try:
        # calculate offset value with baseGlyph
        ucBaseLeftMargin = (font[ucRoundBasis].angledLeftMargin + font[ucRoundBasis].angledRightMargin) / 2.0
        ucOffset = -font[ucRoundBasis].angledLeftMargin + ucBaseLeftMargin
    # if there’s no "O" / ucRoundBasis glyph
    except KeyError:
        try:
            ucRoundBasis = "at"
            ucBaseLeftMargin = (font[ucRoundBasis].angledLeftMargin + font[ucRoundBasis].angledRightMargin) / 2.0
            ucOffset = -font[ucRoundBasis].angledLeftMargin + ucBaseLeftMargin
        except:
            print(f"🤖 Warning: can’t correct x position of uppercase rounds in {font} because it contains neither /O nor /at")
            pass
    
    try:
        # calculate offset value with baseGlyph
        lcBaseLeftMargin = (font[lcRoundBasis].angledLeftMargin + font[lcRoundBasis].angledRightMargin) / 2.0
        lcOffset = -font[lcRoundBasis].angledLeftMargin + lcBaseLeftMargin
    except KeyError:
        try:
            lcRoundBasis = "e"
            lcBaseLeftMargin = (font[ucRoundBasis].angledLeftMargin + font[ucRoundBasis].angledRightMargin) / 2.0
            lcOffset = -font[ucRoundBasis].angledLeftMargin + ucBaseLeftMargin
        except:
            print(f"🤖 Warning: can’t correct x position of lowercase rounds in {font} because it contains no /e")
            pass

    try:
        # round offset value
        if roundOffset:
            ucOffset = round(ucOffset)
            lcOffset = round(lcOffset)

        for glyph in font:
            if glyph.name in ucRounds:
                glyph.moveBy((ucOffset, 0))
            if glyph.name in lcRounds:
                glyph.moveBy((lcOffset, 0))

            # also offset anchors, which will be further corrected for slanting, below, in correctAnchors()
            for anchor in glyph.anchors:
                if glyph.name in ucRounds:
                    anchor.x -= ucOffset
                if glyph.name in lcRounds:
                    anchor.x -= lcOffset

    except UnboundLocalError:

        print("🤖 Skipping circular glyph offset")
        pass


def addOvershootGuidelines(font):
    """
        Add guidelines to assist in making overshoots exactly vertically aligned, which is helpful to autohinting results.
    """

    font.appendGuideline((0, font.info.capHeight + 20), 0, name="overshoot")
    font.appendGuideline((0, font.info.ascender + 20), 0, name="overshoot")
    font.appendGuideline((0, font.info.xHeight + 20), 0, name="overshoot")

    font.appendGuideline((0, font.info.descender - 20), 0, name="overshoot")
    font.appendGuideline((0, -20), 0, name="overshoot")


def getFlippedComponents(font):
    flippedComponents = []
    for g in font:
        for component in g.components:
            if component.naked().transformation:
                # flipped horizontal
                if component.naked().transformation[0] == -1:
                    flippedComponents.append(g.name)
                # flipped vertical
                if component.naked().transformation[3] == -1:
                    flippedComponents.append(g.name)
    return list(set(flippedComponents))


def correctItalicOffset(font, offsetBasisGlyph="H", roundOffset=False):
    """
        https://robofont.com/RF4.1/documentation/tutorials/making-italic-fonts/#applying-the-italic-slant-offset-after-drawing
    """

    if offsetBasisGlyph not in font.keys():
        if "e" in font.keys():
            offsetBasisGlyph = "e"
        elif "o" in font.keys():
            offsetBasisGlyph = "o"
        elif "A" in font.keys():
            offsetBasisGlyph = "A"
        else:
            print("🤖 Can't correct italic offset because font excludes glyphs /H, /e, /o, and /A")
            return

     # calculate offset value with offsetBasisGlyph
    baseLeftMargin = (font[offsetBasisGlyph].angledLeftMargin + font[offsetBasisGlyph].angledRightMargin) / 2.0
    offset = -font[offsetBasisGlyph].angledLeftMargin + baseLeftMargin

    # round offset value
    if roundOffset and offset != 0:
        offset = round(offset)

    # get flipped components
    flippedComponents = getFlippedComponents(font)

    # apply offset to all glyphs in font
    if offset and font[offsetBasisGlyph].angledLeftMargin and len(font.keys()):

        # get reverse components dict
        componentMap = font.getReverseComponentMapping()

        # apply offset to all glyphs in font
        for glyphName in font.keys():
            with font[glyphName].undo():
                font[glyphName].moveBy((offset, 0))

            # if the glyph is used as a component, revert component offset
            for composedGlyph in componentMap.get(glyphName, []):
                for component in font[composedGlyph].components:
                    if component.baseGlyph == glyphName:
                        # make sure it's not a flipped component
                        if glyphName not in flippedComponents:
                            component.moveBy((-offset, 0))

            # done with glyph
            font[glyphName].update()

        # fix flipped components
        for glyphName in flippedComponents:
            for component in font[glyphName].components:
                # offset flipped components twice:
                # baseGlyph offset + offset in the wrong direction
                component.moveBy((offset*2, 0))

                # fix glyphs which use the flipped component as a component
                for composedGlyph in componentMap.get(glyphName, []):
                    for component in font[composedGlyph].components:
                        if component.baseGlyph == glyphName:
                            component.moveBy((-offset, 0))

            # done with glyph
            font[glyphName].update()

def correctAnchors(font):
    """
        Correct anchor x position for italic slant.
    """

    for glyph in font:
        if len(glyph.anchors) > 0:
            for anchor in glyph.anchors:
                anchor.x += math.tan(math.radians(-font.info.italicAngle)) * anchor.y


def copySpacing(originalFont, slantedFont):
    """
        We want to easily correct the positioning and spacing of slanted glyphs, 
        so this just copies the spacing from the original font.

        TODO: determine whether it is better to copy the left margin and glyph width, or the left and right margins...

    """

    for g in slantedFont:
        try:
            g.angledLeftMargin = originalFont[g.name].leftMargin
            # g.angledRightMargin = originalFont[g.name].rightMargin
            g.width = originalFont[g.name].width
        except (KeyError, TypeError) as e:
            # you can't copy a left margin if there is nothing in a glyph (e.g. the /space glyph)
            g.width = originalFont[g.name].width

fonts = []
newFonts = []

# Get input font paths
inputFontsPaths = getFile(dialogMessage, allowsMultipleSelection=True, fileTypes=["ufo"])
print("---------------------------------\n\n🤖 Generating faux italics, please hold...\n")

for fontPath in inputFontsPaths:
    font = OpenFont(fontPath, showInterface=True)
    fonts.append(font)


# Go through input paths & use to generate slanted fonts
for font in fonts:

    print(f"\n🤖 Generating faux italic from\n🤖 {font.path}")

    # set up paths, clear existing UFOs

    fontDir, fontFile = os.path.split(fontPath)
    italicDir = fontDir + "/" + outputFolder

    if not os.path.exists(italicDir):
        os.makedirs(italicDir)

    slantedFontPath = italicDir + "/" + f"{fontFile.replace('.ufo','_italic_generated.ufo')}"

    # delete faux-italic UFO if it already exists, to avoid filesystem clashes
    if os.path.exists(slantedFontPath):
        shutil.rmtree(slantedFontPath)

    # Generate faux italic font

    slantedFont = generateFont(font)

    # fix x positioning of round glyphs
    fixRoundOffset(slantedFont)

    # added guidelines for overshoots
    addOvershootGuidelines(slantedFont)

    # add italic offset
    italicSlantOffset = math.tan(slantedFont.info.italicAngle * math.pi / 180) * (slantedFont.info.xHeight * 0.5)
    slantedFont.lib["com.typemytype.robofont.italicSlantOffset"] = italicSlantOffset

    # correct for italic offset
    correctItalicOffset(slantedFont)
    correctAnchors(slantedFont)

    copySpacing(font, slantedFont)

    # TODO? correct for anchor alignment
    # TODO? correct for accent alignment

    newFonts.append(slantedFont)

    if saveNewFonts:
        slantedFont.save(slantedFontPath)

    if openNewFonts:
        slantedFont.openInterface()
    else:
        slantedFont.close()

class ClosingUI:

    def __init__(self):
        self.w = Window((400, 160), "Italics Generated!")
        yPos = 10
        self.w.myTextBox = TextBox((10, yPos, -10, 17), "Italics generated at:")
        yPos += 20
        self.w.italicPath =  TextBox((10, yPos, -10, 17), f"📁 {'/'.join([path for path in italicDir.split('/')][3:])}", selectable=True, sizeStyle="small")
        yPos += 30
        self.w.closeOriginals = Button((10, yPos, -10, 20), "Close original UFOs", callback=self.closeOriginals)
        yPos += 30
        self.w.closeOriginalsAndNew = Button((10, yPos, -10, 20), "Close original and generated UFOs", callback=self.closeOriginalsAndNew)
        yPos += 30
        self.w.leaveOriginals = Button((10, yPos, -10, 20), "Leave all UFOs open", callback=self.leaveOriginals)
        self.w.open()
    
    def closeOriginals(self, sender):
        print("🤖 Closing original UFOs")
        self.w.close()
        for font in fonts:
            font.close()

    def closeOriginalsAndNew(self, sender):
        print("🤖 Closing original and new UFOs")
        self.w.close()
        for font in fonts:
            font.close()
        for font in newFonts:
            font.close()
    
    def leaveOriginals(self, sender):
        print("🤖 Leaving all UFOs open")
        self.w.close()

ClosingUI()
