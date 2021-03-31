# !/bin/bash

set -e

DS=$1
outputDir="fonts/shantell-sans"

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

for normalStatic in $normalStatics; do
    # subset calt table out to avoid unused alts
    pyftsubset $normalStatic --layout-features-="calt" --unicodes="*" --output-file="$normalStatic.subset"
    # move subset file back to previous name
    mv "$normalStatic.subset" $normalStatic
done

# -----------------------------------------------------------------------------------
# font fixes

statics=$(ls $outputDir/static-*TF/*.*tf)
for static in $statics; do
    ext=${static##*.}
    echo $ext

    # fix nonhinting
    gftools fix-nonhinting "$static" "$static"
    rm ${static/".$ext"/"-backup-fonttools-prep-gasp.$ext"}

    # remove MVAR (custom underline values, which mess up line heights on older versions of Windows)
    gftools fix-unwanted-tables $static

    # remove DSIG
    gftools fix-dsig --autofix $static

    # set fsType to allow editable embedding
    gftools fix-fstype $static
    mv "$static.fix" "$static"

    # TODO: add v-font versioning
done
