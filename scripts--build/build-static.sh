# !/bin/bash

set -e

DS="sources/ital_wght_BNCE_IRGL_TRAK--prepped/shantell_sans-ital_wght_BNCE_IRGL_TRAK--static.designspace"
outputDir="fonts/Shantell Sans/Desktop"
staticDir="$outputDir/Static"
webDir="fonts/Shantell Sans/Web"

mkdir -p "$outputDir"


# -----------------------------------------------------------------------------------
# update feature code to point to correct feature file paths

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    python "./scripts--build/helpers/update-feature-code-for-statics.py" "$ufo"
done


# -----------------------------------------------------------------------------------
# build static fonts

# Build TTFs
fontmake -o ttf -i -m $DS --output-dir "$outputDir/static-TTF" &
wait

# Build OTFs (don’t optimize the CFF table, because it takes a super long time for marginal benefit)
fontmake -o otf -i -m $DS --optimize-cff=0 --output-dir "$outputDir/static-OTF" &
wait


# -----------------------------------------------------------------------------------
# remove alts & calt code from static "normal" (non-bouncy, non-irregular) fonts

function subsetNormal {
    normalStatic="$1"
    echo $normalStatic
    # subset calt table out to avoid unused alts
    pyftsubset "$normalStatic" --layout-features-="calt" --unicodes="*" --glyph-names --notdef-outline --name-IDs='*' --output-file="$normalStatic.subset"
    # move subset file back to previous name
    mv "$normalStatic.subset" "$normalStatic"
}

find "$outputDir/static-TTF" "$outputDir/static-OTF" -path '*Normal*.*tf' -print0 | while read -d $'\0' file
do
    subsetNormal "$file"
done


# -----------------------------------------------------------------------------------
# font fixes

version=$(cat "version.txt")

function fixfont {
    static="$1"

    ext=${static##*.}
    echo "$ext"

    # fix nonhinting
    gftools fix-nonhinting "$static" "$static"
    rm "${static/.$ext/-backup-fonttools-prep-gasp.$ext}"

    # remove MVAR (custom underline values, which mess up line heights on older versions of Windows)
    gftools fix-unwanted-tables "$static"

    # # add dummy DSIG
    # gftools fix-dsig --autofix "$static"

    # set fsType to allow editable embedding
    gftools fix-fstype "$static"
    if [ -f "$static.fix" ]; then
        mv "$static.fix" "$static"
    fi

    # set version data
    sha1=$(git log -1 --format="%h") # get latest git commit hash
    python scripts--build/helpers/set-version-data.py "$static" --version "$version" --sha1 "$sha1" --inplace
}

find "$outputDir/static-TTF" "$outputDir/static-OTF" -path '*.*tf' -print0 | while read -d $'\0' file
do
    fixfont "$file"
done

# -----------------------------------------------------------------------------------
# web fonts

mkdir -p "$webDir/Static"

find "$outputDir/static-TTF" -path '*.ttf' -print0 | while read -d $'\0' ttf
do
    woff2_compress "$ttf"

    woff2name=$(basename "${ttf/.ttf/.woff2}")
    mv "${ttf/.ttf/.woff2}" "$webDir/Static/$woff2name"
done

# -----------------------------------------------------------------------------------
# sort fonts

mkdir -p "$staticDir"

mv "$outputDir/static-OTF" "$staticDir/OTF"
mv "$outputDir/static-TTF" "$staticDir/TTF"
