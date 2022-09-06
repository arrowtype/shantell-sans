# !/bin/bash

set -e

DS="sources/build-prep/ital_wght_BNCE_IRGL_TRAK--prepped/shantell_sans-ital_wght_BNCE_IRGL_TRAK-simplified.designspace"
outputDir="fonts/Shantell Sans/Desktop"
webDir="fonts/Shantell Sans/Web"
vfName="Shantell_Sans-Variable.ttf"
finalVfName="ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf"

mkdir -p "$outputDir"

vfPath="$outputDir/$vfName"

fontmake -o variable -m $DS --output-path "$vfPath" 

# add STAT table
python3 "./scripts--build/helpers/add-STAT.py" "$vfPath"

# ----------------------------------------------------------------------------------------------
# fixes

# fix nonhinting
gftools fix-nonhinting "$vfPath" "$vfPath"
rm "${vfPath/.ttf/-backup-fonttools-prep-gasp.ttf}"

# # remove MVAR (custom underline values, which mess up line heights on older versions of Windows)
gftools fix-unwanted-tables "$vfPath" -t MVAR

# set fsType to allow editable embedding
gftools fix-fstype "$vfPath"
mv "$vfPath.fix" "$vfPath"

# add a dummy AVAR table to pass FontBakery check (linear axes will allow for easier VF animations)
python scripts--build/helpers/add-AVAR.py "$vfPath"

# set version data
version=$(cat "version.txt")
sha1=$(git log -1 --format="%h") # get latest git commit hash
python scripts--build/helpers/set-version-data.py "$vfPath" --version "$version" --sha1 "$sha1" --inplace

# change to official filename
mv "$vfPath" "$outputDir/$finalVfName"

# opens the font in whatever the default app is for .ttf files – FontGoggles recommended
open "$outputDir/$finalVfName"

# ----------------------------------------------------------------------------------------------
# make web fonts

webVfName=${finalVfName/'.ttf'/'.woff2'}

mkdir -p "$webDir"

woff2_compress "$outputDir/$finalVfName"

mv "$outputDir/$webVfName" "$webDir/$webVfName"


# ----------------------------------------------------------------------------------------------
# make google fonts fonts

outputDirGF="fonts/shantell_sans-for-googlefonts"
finalVfNameRoman="ShantellSans[BNCE,IRGL,TRAK,wght].ttf"
finalVfNameItalic="ShantellSans-Italic[BNCE,IRGL,TRAK,wght].ttf"

mkdir -p $outputDirGF

# split roman/italic VFs for googlefonts
fonttools varLib.instancer "$outputDir/$finalVfName" ital=0 --output "$outputDirGF/$finalVfNameRoman"
fonttools varLib.instancer "$outputDir/$finalVfName" ital=1 --output "$outputDirGF/$finalVfNameItalic"

# reduce set of instances for GF standards
gftools fix-font "$outputDirGF/$finalVfNameRoman" -o "$outputDirGF/$finalVfNameRoman" --include-source-fixes
gftools fix-font "$outputDirGF/$finalVfNameItalic" -o "$outputDirGF/$finalVfNameItalic" --include-source-fixes
