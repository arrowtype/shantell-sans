BASE_R = shantellsans-wght_ital_INFM

GLYPHSPKG = sources/shantellsans-wght_ital_INFM.glyphspackage

PREPDIR = sources/build-prep
GLYPHS = $(PREPDIR)/shantellsans-wght_ital_INFM.glyphs
UFOPREPDIR = $(PREPDIR)/ital_wght_BNCE_INFM_SPAC--prepped

VF = fonts/Shantell\ Sans/Desktop/ShantellSans\[BNCE,INFM,SPAC,ital,wght\].ttf
STATICS = fonts/Shantell\ Sans/Desktop/Static/TTF


# ------------------------------------
# phony commands

# most of the time, it’s best to just build the variable font
.PHONY: all
all: $(VF) $(GF)

# if you really want all the fonts (variable and static), run 'make full'
.PHONY: full
full: $(VF) $(STATICS) $(GF)

# just builds variable font (including special version for google fonts)
.PHONY: vf
vf: $(VF)

# only build the statics, e.g. after you have already built the VF
.PHONY: statics
statics: $(STATICS)

# only make the prepped dir
.PHONY: prep
prep: $(UFOPREPDIR)

# just change to a glyphs file
.PHONY: glyphs
glyphs: $(GLYPHS)


# ------------------------------------
# commands

$(STATICS): $(UFOPREPDIR)
	scripts--build/build-static.sh
	scripts--build/make-release.sh

$(VF): $(UFOPREPDIR)
	scripts--build/build-vf.sh

$(UFOPREPDIR): $(GLYPHS)
	python scripts--build/prep-build.py

$(GLYPHS): $(PREPDIR)
	glyphspkg $(GLYPHSPKG)
	mv sources/shantellsans-wght_ital_INFM.glyphs $(GLYPHS)

$(PREPDIR): $(GLYPHSPKG)
	mkdir -p $(PREPDIR)

.PHONY: clean
clean:
	rm -rf $(PREPDIR)
	rm -rf fonts/Shantell\ Sans
