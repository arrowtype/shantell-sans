# !/bin/bash

set -e

DS="sources/wght_BNCE_IRGL--prepped/shantell_sans-wght_BNCE_IRGL.designspace"
outputDir="fonts/shantell-sans"
vfName="Shantell_Sans-Variable.ttf"

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    pwd
    python "./scripts--build/helpers/update-feature-code-for-vf.py" "$ufo"    
done

vfPath="$outputDir/$vfName"

fontmake -o variable -m $DS --no-production-names --output-path $vfPath

# add STAT table

python3 "./scripts--build/helpers/add-STAT.py" $vfPath

# ----------------------------------------------------------------------------------------------
# fixes

# fix nonhinting
gftools fix-nonhinting "$vfPath" "$vfPath"
rm ${vfPath/".ttf"/"-backup-fonttools-prep-gasp.ttf"}

# remove MVAR (custom underline values, which mess up line heights on older versions of Windows)
gftools fix-unwanted-tables $vfPath

# add dummy DSIG
gftools fix-dsig --autofix $vfPath

# set fsType to allow editable embedding
gftools fix-fstype $vfPath
mv "$vfPath.fix" "$vfPath"

# add a dummy AVAR table to pass FontBakery check (linear axes will allow for easier VF animations)
python scripts--build/helpers/add-AVAR.py $vfPath

# set version data
version=$(cat "version.txt")
font-v write --ver=$version --sha1 $vfPath

# change to official filename
mv $vfPath "$outputDir/ShantellSans[BNCE,IRGL,wght].ttf"

# opens the font in whatever the default app is for .ttf files – FontGoggles recommended
open "$outputDir/ShantellSans[BNCE,IRGL,wght].ttf"
