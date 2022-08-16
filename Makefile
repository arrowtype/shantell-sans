BASE_R = shantellsans-wght_ital_IRGL

GLYPHSPKG = sources/shantellsans-wght_ital_IRGL.glyphspackage

PREPDIR = "sources/build-prep"
GLYPHS = $(PREPDIR)/shantellsans-wght_ital_IRGL.glyphs
UFOPREPDIR = $(PREPDIR)/ital_wght_BNCE_IRGL_TRAK--prepped

VF = "fonts/Shantell Sans/Desktop/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf"
STATICS = "fonts/Shantell Sans/Desktop/Static"

# most of the time, it’s best to just build the variable font
.PHONY: all
all: $(VF)

.PHONY: glyphs
glyphs: $(GLYPHS)

# if you really want all the fonts (variable and static), run 'make full'
.PHONY: full
full: $(VF) $(STATICS)

# also just builds variable font
.PHONY: vf
vf: $(VF)

# only build the statics, e.g. after you have already built the VF
.PHONY: statics
statics: $(STATICS)

$(STATICS): $(PREPDIR)
	scripts--build/build-static.sh

$(VF): $(UFOPREPDIR)
	scripts--build/build-vf.sh

$(UFOPREPDIR): $(GLYPHS)
	python scripts--build/prep-build.py

$(GLYPHS): $(PREPDIR)
	glyphspkg $(GLYPHSPKG)
	mv sources/shantellsans-wght_ital_IRGL.glyphs $(GLYPHS)

$(PREPDIR): $(GLYPHSPKG)
	mkdir -p $(PREPDIR)


.PHONY: clean
clean:
	rm -rf $(PREPDIR)
