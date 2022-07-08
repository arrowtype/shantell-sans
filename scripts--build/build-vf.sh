# !/bin/bash

set -e

# DS="sources/wght_BNCE_IRGL_TRAK--prepped/shantell_sans-wght_BNCE_IRGL_TRAK.designspace"
DS="sources/ital_wght_BNCE_IRGL_TRAK--prepped/shantell_sans-ital_wght_BNCE_IRGL_TRAK.designspace"
outputDir="fonts/Shantell Sans/Desktop"
webDir="fonts/Shantell Sans/Web"
vfName="Shantell_Sans-Variable.ttf"
finalVfName="ShantellSans[BNCE,IRGL,TRAK,ital,wght].ttf"

mkdir -p "$outputDir"

vfPath="$outputDir/$vfName"

# # update feature code to point to correct feature file paths
# parentDir=$(dirname "$DS")
# for ufo in $parentDir/*.ufo; do
#     pwd
#     python "./scripts--build/helpers/update-feature-code-for-vf.py" "$ufo"    
# done


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
