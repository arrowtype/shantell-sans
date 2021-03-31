# !/bin/bash

set -e

DS=$1
outputDir="fonts/shantell-sans-v14"
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

# remove DSIG
gftools fix-dsig --autofix $vfPath

# set fsType to allow editable embedding
gftools fix-fstype $vfPath
mv "$vfPath.fix" "$vfPath"

# TODO: add v-font versioning

# opens the font in whatever the default app is for .ttf files – FontGoggles recommended
open $vfPath
