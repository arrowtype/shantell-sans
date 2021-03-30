# !/bin/bash

set -e

DS=$1
outputDir="fonts/shantell-sans-v14"

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    python "./scripts--build/helpers/update-feature-code-for-statics.py" "$ufo"
done


# -----------------------------------------------------------------------------------
# build static fonts

# Build TTFs
fontmake -o ttf -i -m $DS --output-dir $outputDir/static-TTF

# Build OTFs (don’t optimize the CFF table, because it takes a super long time)
fontmake -o otf -i -m $DS --output-dir $outputDir/static-OTF --optimize-cff=0


# -----------------------------------------------------------------------------------
# remove alts & calt code from static "normal" (non-bouncy, non-irregular) fonts

normalStatics=$(ls $outputDir/static-*TF/*Normal*.*tf)

for normalStatic in $normalStatics
do  
    # subset calt table out to avoid unused alts
    pyftsubset $normalStatic --layout-features-="calt" --unicodes="*" --output-file="$normalStatic.subset"
    # move subset file back to previous name
    mv "$normalStatic.subset" $normalStatic
done

