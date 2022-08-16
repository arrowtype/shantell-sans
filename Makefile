BASE_R = shantellsans-wght_ital_IRGL

PREPDIR = sources/ital_wght_BNCE_IRGL_TRAK--prepped
GLYPHS = sources/$(BASE_R).glyphs
GLYPHSPKG = $(GLYPHS)package
VF = "fonts/Shantell Sans/Desktop/ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf"
STATICS = "fonts/Shantell Sans/Desktop/Static"

# most of the time, it’s best to just build the variable font
.PHONY: all
all: $(VF)

# if you really want all the fonts (variable and static), run 'make full'
.PHONY: full
full: $(VF) $(STATICS)

# also just builds variable font
.PHONY: vf
vf: $(VF)

# only build the statics, e.g. after you have already built the VF
.PHONY: static
static: $(STATICS)

$(STATICS): $(PREPDIR)
	scripts--build/build-static.sh

$(VF): $(PREPDIR)
	scripts--build/build-vf.sh

$(PREPDIR): $(GLYPHS)
	python scripts--build/prep-build.py

$(GLYPHS): $(GLYPHSPKG)
	echo $(GLYPHSPKG)
	glyphspkg $(GLYPHSPKG)

$(GLYPHSPKG):
	$(GLYPHSPKG)


.PHONY: clean
clean:
	rm -rf $(GLYPHS)
	rm -rf $(PREPDIR)
