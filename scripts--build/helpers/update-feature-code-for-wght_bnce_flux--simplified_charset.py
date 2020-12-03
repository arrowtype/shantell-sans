"""
	Update feature code for static build
"""

import sys
from fontParts.world import *

fontPath = sys.argv[1]

font = OpenFont(fontPath, showInterface=False)


if "sparse" not in fontPath:
    print()
    print(font.info.familyName, font.info.styleName)
    print("feature code was:")
    print(font.features.text)
    
    font.features.text = """\
languagesystem DFLT dflt;
languagesystem latn dflt;

include(../features/features/common.fea);
include(../features/features/frac.fea);
include(../features/features/numr_dnom_supr_infr.fea);

feature calt {
    @randomCycle1 = [A      B      C      D      E      F      G      H      I      J      K      L      M      N      O      P      Q      R      S      T      U      V      W      X      Y      Z      a      ampersand      asciicircum      asciitilde      asterisk      at      b      backslash      bar      braceleft      braceright      bracketleft      bracketright      c      colon      comma      d      dollar      e      eight      equal      exclam      f      five      four      g      grave      greater      h      hyphen      i      j      k      l      less      m      n      nine      numbersign      o      one      p      parenleft      parenright      percent      period      plus      q      question      quotedbl      quotesingle      r      s      semicolon      seven      six      slash      t      three      two      u      underscore      v      w      x      y      z      zero eacute      ntilde      ];
    @randomCycle2 = [A.alt1 B.alt1 C.alt1 D.alt1 E.alt1 F.alt1 G.alt1 H.alt1 I.alt1 J.alt1 K.alt1 L.alt1 M.alt1 N.alt1 O.alt1 P.alt1 Q.alt1 R.alt1 S.alt1 T.alt1 U.alt1 V.alt1 W.alt1 X.alt1 Y.alt1 Z.alt1 a.alt1 ampersand.alt1 asciicircum.alt1 asciitilde.alt1 asterisk.alt1 at.alt1 b.alt1 backslash.alt1 bar.alt1 braceleft.alt1 braceright.alt1 bracketleft.alt1 bracketright.alt1 c.alt1 colon.alt1 comma.alt1 d.alt1 dollar.alt1 e.alt1 eight.alt1 equal.alt1 exclam.alt1 f.alt1 five.alt1 four.alt1 g.alt1 grave.alt1 greater.alt1 h.alt1 hyphen.alt1 i.alt1 j.alt1 k.alt1 l.alt1 less.alt1 m.alt1 n.alt1 nine.alt1 numbersign.alt1 o.alt1 one.alt1 p.alt1 parenleft.alt1 parenright.alt1 percent.alt1 period.alt1 plus.alt1 q.alt1 question.alt1 quotedbl.alt1 quotesingle.alt1 r.alt1 s.alt1 semicolon.alt1 seven.alt1 six.alt1 slash.alt1 t.alt1 three.alt1 two.alt1 u.alt1 underscore.alt1 v.alt1 w.alt1 x.alt1 y.alt1 z.alt1 zero eacute.alt1 ntilde.alt1 ];
    @randomCycle3 = [A.alt2 B.alt2 C.alt2 D.alt2 E.alt2 F.alt2 G.alt2 H.alt2 I.alt2 J.alt2 K.alt2 L.alt2 M.alt2 N.alt2 O.alt2 P.alt2 Q.alt2 R.alt2 S.alt2 T.alt2 U.alt2 V.alt2 W.alt2 X.alt2 Y.alt2 Z.alt2 a.alt2 ampersand.alt2 asciicircum.alt2 asciitilde.alt2 asterisk.alt2 at.alt2 b.alt2 backslash.alt2 bar.alt2 braceleft.alt2 braceright.alt2 bracketleft.alt2 bracketright.alt2 c.alt2 colon.alt2 comma.alt2 d.alt2 dollar.alt2 e.alt2 eight.alt2 equal.alt2 exclam.alt2 f.alt2 five.alt2 four.alt2 g.alt2 grave.alt2 greater.alt2 h.alt2 hyphen.alt2 i.alt2 j.alt2 k.alt2 l.alt2 less.alt2 m.alt2 n.alt2 nine.alt2 numbersign.alt2 o.alt2 one.alt2 p.alt2 parenleft.alt2 parenright.alt2 percent.alt2 period.alt2 plus.alt2 q.alt2 question.alt2 quotedbl.alt2 quotesingle.alt2 r.alt2 s.alt2 semicolon.alt2 seven.alt2 six.alt2 slash.alt2 t.alt2 three.alt2 two.alt2 u.alt2 underscore.alt2 v.alt2 w.alt2 x.alt2 y.alt2 z.alt2 zero eacute.alt2 ntilde.alt2 ];

    sub @randomCycle1 @randomCycle1' by @randomCycle2;
    sub @randomCycle2 @randomCycle1' by @randomCycle3;
} calt;

    """
    
    print("feature code is now:")
    print(font.features.text)
    print()


font.save()
font.close()
