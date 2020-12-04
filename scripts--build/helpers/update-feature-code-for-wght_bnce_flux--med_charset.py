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
    @randomCycle1 = [Emacron      Ucircumflex      ograve      umacron      racute      Ebreve      dcaron      colon      Uacute      A      ydieresis      eight      H      Omacron      L      IJ      OE      Ucaron      Atilde      zdotaccent      Ccaron      T      n      gbreve      uogonek      Ecircumflex      Icircumflex      rcaron      Odieresis      ohungarumlaut      r      W      j      Idieresis      germandbls      at      tcaron      acaron      Zcaron      Acaron      braceright      amacron      AE      cedillacomb      ringcomb      D      quotedbl      s      Nacute      Ecaron      Yacute      G      q      Z      Abreve      x      otilde      ae      endash      ccaron      Iacute      egrave      O      period      Amacron      Obreve      seven      e      Ntilde      semicolon      comma      jdotless      icircumflex      ucircumflex      iogonek      dotaccentcmb      ebreve      Egrave      Aogonek      four      Ohungarumlaut      aacute      uring      braceleft      dieresiscomb      nine      adieresis      Adieresis      aogonek      quotesingle      igrave      gravecomb      oacute      Q      ogonekcmb      o      one      zero      less      underscore      ugrave      Cacute      b      tildecomb      two      parenleft      Eogonek      Dcaron      v      y      edieresis      Uogonek      S      Aacute      f      t      idieresis      E      Ocircumflex      Ccedilla      bracketleft      N      Edieresis      Y      i      scedilla      Zdotaccent      Ydieresis      Ubreve      ecircumflex      asciicircum      ampersand      slash      zacute      ccedilla      Ibreve      h      ecaron      Otilde      acutecomb      Udieresis      B      question      Idotaccent      Imacron      Lslash      Oslashacute      six      Umacron      u      k      w      obreve      acircumflex      p      J      yacute      bar      l      Ograve      agrave      K      Oacute      Iogonek      Ncaron      percent      grave      omacron      Aring      abreve      m      atilde      uhungarumlaut      brevecomb      Acircumflex      numbersign      dollar      uacute      ucaron      Ugrave      ocircumflex      hyphen      Tcaron      Scedilla      g      hungarumlautcmb      Eacute      P      udieresis      I      zcaron      X      greater      Scaron      bracketright      Uring      ubreve      F      ncaron      sacute      ntilde      plus      iacute      odieresis      Agrave      z      Sacute      Igrave      caroncomb      nacute      five      M      d      Gbreve      emacron      eacute      a      C      ibreve      cacute      asciitilde      aring      macroncomb      asterisk      eogonek      circumflexcomb      backslash      Rcaron      Omega      c      imacron      U      scaron      three      exclam      Oslash      R      Racute      V      parenright      Uhungarumlaut      equal      Zacute      ];
    @randomCycle2 = [Emacron.alt1 Ucircumflex.alt1 ograve.alt1 umacron.alt1 racute.alt1 Ebreve.alt1 dcaron.alt1 colon.alt1 Uacute.alt1 A.alt1 ydieresis.alt1 eight.alt1 H.alt1 Omacron.alt1 L.alt1 IJ.alt1 OE.alt1 Ucaron.alt1 Atilde.alt1 zdotaccent.alt1 Ccaron.alt1 T.alt1 n.alt1 gbreve.alt1 uogonek.alt1 Ecircumflex.alt1 Icircumflex.alt1 rcaron.alt1 Odieresis.alt1 ohungarumlaut.alt1 r.alt1 W.alt1 j.alt1 Idieresis.alt1 germandbls.alt1 at.alt1 tcaron.alt1 acaron.alt1 Zcaron.alt1 Acaron.alt1 braceright.alt1 amacron.alt1 AE.alt1 cedillacomb.alt1 ringcomb.alt1 D.alt1 quotedbl.alt1 s.alt1 Nacute.alt1 Ecaron.alt1 Yacute.alt1 G.alt1 q.alt1 Z.alt1 Abreve.alt1 x.alt1 otilde.alt1 ae.alt1 endash.alt1 ccaron.alt1 Iacute.alt1 egrave.alt1 O.alt1 period.alt1 Amacron.alt1 Obreve.alt1 seven.alt1 e.alt1 Ntilde.alt1 semicolon.alt1 comma.alt1 jdotless.alt1 icircumflex.alt1 ucircumflex.alt1 iogonek.alt1 dotaccentcmb.alt1 ebreve.alt1 Egrave.alt1 Aogonek.alt1 four.alt1 Ohungarumlaut.alt1 aacute.alt1 uring.alt1 braceleft.alt1 dieresiscomb.alt1 nine.alt1 adieresis.alt1 Adieresis.alt1 aogonek.alt1 quotesingle.alt1 igrave.alt1 gravecomb.alt1 oacute.alt1 Q.alt1 ogonekcmb.alt1 o.alt1 one.alt1 zero.alt1 less.alt1 underscore.alt1 ugrave.alt1 Cacute.alt1 b.alt1 tildecomb.alt1 two.alt1 parenleft.alt1 Eogonek.alt1 Dcaron.alt1 v.alt1 y.alt1 edieresis.alt1 Uogonek.alt1 S.alt1 Aacute.alt1 f.alt1 t.alt1 idieresis.alt1 E.alt1 Ocircumflex.alt1 Ccedilla.alt1 bracketleft.alt1 N.alt1 Edieresis.alt1 Y.alt1 i.alt1 scedilla.alt1 Zdotaccent.alt1 Ydieresis.alt1 Ubreve.alt1 ecircumflex.alt1 asciicircum.alt1 ampersand.alt1 slash.alt1 zacute.alt1 ccedilla.alt1 Ibreve.alt1 h.alt1 ecaron.alt1 Otilde.alt1 acutecomb.alt1 Udieresis.alt1 B.alt1 question.alt1 Idotaccent.alt1 Imacron.alt1 Lslash.alt1 Oslashacute.alt1 six.alt1 Umacron.alt1 u.alt1 k.alt1 w.alt1 obreve.alt1 acircumflex.alt1 p.alt1 J.alt1 yacute.alt1 bar.alt1 l.alt1 Ograve.alt1 agrave.alt1 K.alt1 Oacute.alt1 Iogonek.alt1 Ncaron.alt1 percent.alt1 grave.alt1 omacron.alt1 Aring.alt1 abreve.alt1 m.alt1 atilde.alt1 uhungarumlaut.alt1 brevecomb.alt1 Acircumflex.alt1 numbersign.alt1 dollar.alt1 uacute.alt1 ucaron.alt1 Ugrave.alt1 ocircumflex.alt1 hyphen.alt1 Tcaron.alt1 Scedilla.alt1 g.alt1 hungarumlautcmb.alt1 Eacute.alt1 P.alt1 udieresis.alt1 I.alt1 zcaron.alt1 X.alt1 greater.alt1 Scaron.alt1 bracketright.alt1 Uring.alt1 ubreve.alt1 F.alt1 ncaron.alt1 sacute.alt1 ntilde.alt1 plus.alt1 iacute.alt1 odieresis.alt1 Agrave.alt1 z.alt1 Sacute.alt1 Igrave.alt1 caroncomb.alt1 nacute.alt1 five.alt1 M.alt1 d.alt1 Gbreve.alt1 emacron.alt1 eacute.alt1 a.alt1 C.alt1 ibreve.alt1 cacute.alt1 asciitilde.alt1 aring.alt1 macroncomb.alt1 asterisk.alt1 eogonek.alt1 circumflexcomb.alt1 backslash.alt1 Rcaron.alt1 Omega.alt1 c.alt1 imacron.alt1 U.alt1 scaron.alt1 three.alt1 exclam.alt1 Oslash.alt1 R.alt1 Racute.alt1 V.alt1 parenright.alt1 Uhungarumlaut.alt1 equal.alt1 Zacute.alt1 ];
    @randomCycle3 = [Emacron.alt2 Ucircumflex.alt2 ograve.alt2 umacron.alt2 racute.alt2 Ebreve.alt2 dcaron.alt2 colon.alt2 Uacute.alt2 A.alt2 ydieresis.alt2 eight.alt2 H.alt2 Omacron.alt2 L.alt2 IJ.alt2 OE.alt2 Ucaron.alt2 Atilde.alt2 zdotaccent.alt2 Ccaron.alt2 T.alt2 n.alt2 gbreve.alt2 uogonek.alt2 Ecircumflex.alt2 Icircumflex.alt2 rcaron.alt2 Odieresis.alt2 ohungarumlaut.alt2 r.alt2 W.alt2 j.alt2 Idieresis.alt2 germandbls.alt2 at.alt2 tcaron.alt2 acaron.alt2 Zcaron.alt2 Acaron.alt2 braceright.alt2 amacron.alt2 AE.alt2 cedillacomb.alt2 ringcomb.alt2 D.alt2 quotedbl.alt2 s.alt2 Nacute.alt2 Ecaron.alt2 Yacute.alt2 G.alt2 q.alt2 Z.alt2 Abreve.alt2 x.alt2 otilde.alt2 ae.alt2 endash.alt2 ccaron.alt2 Iacute.alt2 egrave.alt2 O.alt2 period.alt2 Amacron.alt2 Obreve.alt2 seven.alt2 e.alt2 Ntilde.alt2 semicolon.alt2 comma.alt2 jdotless.alt2 icircumflex.alt2 ucircumflex.alt2 iogonek.alt2 dotaccentcmb.alt2 ebreve.alt2 Egrave.alt2 Aogonek.alt2 four.alt2 Ohungarumlaut.alt2 aacute.alt2 uring.alt2 braceleft.alt2 dieresiscomb.alt2 nine.alt2 adieresis.alt2 Adieresis.alt2 aogonek.alt2 quotesingle.alt2 igrave.alt2 gravecomb.alt2 oacute.alt2 Q.alt2 ogonekcmb.alt2 o.alt2 one.alt2 zero.alt2 less.alt2 underscore.alt2 ugrave.alt2 Cacute.alt2 b.alt2 tildecomb.alt2 two.alt2 parenleft.alt2 Eogonek.alt2 Dcaron.alt2 v.alt2 y.alt2 edieresis.alt2 Uogonek.alt2 S.alt2 Aacute.alt2 f.alt2 t.alt2 idieresis.alt2 E.alt2 Ocircumflex.alt2 Ccedilla.alt2 bracketleft.alt2 N.alt2 Edieresis.alt2 Y.alt2 i.alt2 scedilla.alt2 Zdotaccent.alt2 Ydieresis.alt2 Ubreve.alt2 ecircumflex.alt2 asciicircum.alt2 ampersand.alt2 slash.alt2 zacute.alt2 ccedilla.alt2 Ibreve.alt2 h.alt2 ecaron.alt2 Otilde.alt2 acutecomb.alt2 Udieresis.alt2 B.alt2 question.alt2 Idotaccent.alt2 Imacron.alt2 Lslash.alt2 Oslashacute.alt2 six.alt2 Umacron.alt2 u.alt2 k.alt2 w.alt2 obreve.alt2 acircumflex.alt2 p.alt2 J.alt2 yacute.alt2 bar.alt2 l.alt2 Ograve.alt2 agrave.alt2 K.alt2 Oacute.alt2 Iogonek.alt2 Ncaron.alt2 percent.alt2 grave.alt2 omacron.alt2 Aring.alt2 abreve.alt2 m.alt2 atilde.alt2 uhungarumlaut.alt2 brevecomb.alt2 Acircumflex.alt2 numbersign.alt2 dollar.alt2 uacute.alt2 ucaron.alt2 Ugrave.alt2 ocircumflex.alt2 hyphen.alt2 Tcaron.alt2 Scedilla.alt2 g.alt2 hungarumlautcmb.alt2 Eacute.alt2 P.alt2 udieresis.alt2 I.alt2 zcaron.alt2 X.alt2 greater.alt2 Scaron.alt2 bracketright.alt2 Uring.alt2 ubreve.alt2 F.alt2 ncaron.alt2 sacute.alt2 ntilde.alt2 plus.alt2 iacute.alt2 odieresis.alt2 Agrave.alt2 z.alt2 Sacute.alt2 Igrave.alt2 caroncomb.alt2 nacute.alt2 five.alt2 M.alt2 d.alt2 Gbreve.alt2 emacron.alt2 eacute.alt2 a.alt2 C.alt2 ibreve.alt2 cacute.alt2 asciitilde.alt2 aring.alt2 macroncomb.alt2 asterisk.alt2 eogonek.alt2 circumflexcomb.alt2 backslash.alt2 Rcaron.alt2 Omega.alt2 c.alt2 imacron.alt2 U.alt2 scaron.alt2 three.alt2 exclam.alt2 Oslash.alt2 R.alt2 Racute.alt2 V.alt2 parenright.alt2 Uhungarumlaut.alt2 equal.alt2 Zacute.alt2 ];

    sub @randomCycle1 @randomCycle1' by @randomCycle2;
    sub @randomCycle2 @randomCycle1' by @randomCycle3;
} calt;

    """
    
    print("feature code is now:")
    print(font.features.text)
    print()


font.save()
font.close()
