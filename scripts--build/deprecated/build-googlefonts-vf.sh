# !/bin/bash

set -e

DS="sources/build-prep/ital_wght_BNCE_IRGL_TRAK--prepped/shantell_sans-ital_wght_BNCE_IRGL_TRAK-googlefonts.designspace"
outputDir="fonts/shantell_sans-for-googlefonts"
vfName="Shantell_Sans-Variable.ttf"
finalVfNameRoman="ShantellSans[BNCE,IRGL,TRAK,wght].ttf"
finalVfNameItalic="ShantellSans-Italic[BNCE,IRGL,TRAK,wght].ttf"

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

# split roman/italic VFs for googlefonts
fonttools varLib.instancer "$vfPath" ital=0 --output "$outputDir/$finalVfNameRoman"
fonttools varLib.instancer "$vfPath" ital=1 --output "$outputDir/$finalVfNameItalic"

# remove unneeded full VF with old path
rm "$vfPath"

# opens the font in whatever the default app is for .ttf files – (I personally recommend FontGoggles)
open "$outputDir/$finalVfNameRoman" "$outputDir/$finalVfNameItalic"
