# !/bin/bash

set -e

DS="sources/build-prep/ital_wght_BNCE_INFM_SPAC--prepped/shantell_sans-ital_wght_BNCE_INFM_SPAC--static-simplified.designspace"
outputDir="fonts/Shantell Sans/Desktop"
staticDir="$outputDir/Static"
webDir="fonts/Shantell Sans/Web"

mkdir -p "$outputDir"
mkdir -p "$outputDir/static-TTF"
mkdir -p "$outputDir/static-OTF"

# -----------------------------------------------------------------------------------
# build static fonts

# Build TTFs
fontmake -o ttf -i -m $DS --expand-features-to-instances --output-dir "$outputDir/static-TTF" &                                       # full build
# fontmake -o ttf -i -m $DS --expand-features-to-instances  -i ".*Normal.*" --output-dir "$outputDir/static-TTF" &                        # use this line for a faster test build of only Normal weights w/ italics
# fontmake -o ttf -i -m $DS --expand-features-to-instances -i ".*Normal Regular" --output-dir "$outputDir/static-TTF" &                   # use this line for a much faster test build of only Normal Regular
wait

find "sources/build-prep/ital_wght_BNCE_INFM_SPAC--prepped/instances" -path '*.ufo' -print0 | while read -d $'\0' file
do
    fontmake -o otf -u "$file" --optimize-cff=0 --output-dir "$outputDir/static-OTF" &
    wait
done

# # Build OTFs (don’t optimize the CFF table, because it takes a super long time for marginal benefit)
# fontmake -o otf -i -m $DS --expand-features-to-instances --optimize-cff=0 --output-dir "$outputDir/static-OTF" &                       # full build if the TTF build isn’t done first
# fontmake -o otf -i -m $DS --expand-features-to-instances -i ".*Normal.*" --optimize-cff=0 --output-dir "$outputDir/static-OTF" &        # use this line for a faster test build of only Normal weights w/ italics
# fontmake -o otf -i -m $DS --expand-features-to-instances -i ".*Normal Regular" --optimize-cff=0 --output-dir "$outputDir/static-OTF" &  # use this line for a much faster test build of only Normal Regular
# wait


# -----------------------------------------------------------------------------------
# remove alts & feature code from static "normal" (non-bouncy, non-irregular) fonts

function subsetNormal {
    normalStatic="$1"
    echo $normalStatic
    # subset rlig table out to avoid unused alts, but make sure to keep all other features
    pyftsubset "$normalStatic" --layout-features+=aalt,calt,case,ccmp,dnom,frac,liga,locl,numr,ordn,sinf,ss01,ss02,ss03,ss04,sups,tnum,zero --layout-features-="rlig" --unicodes="*" --glyph-names --notdef-outline --name-IDs='*' --output-file="$normalStatic.subset"
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
    fonttools ttLib.woff2 compress "$ttf"

    woff2name=$(basename "${ttf/.ttf/.woff2}")
    mv "${ttf/.ttf/.woff2}" "$webDir/Static/$woff2name"
done

# -----------------------------------------------------------------------------------
# sort fonts

mkdir -p "$staticDir"

# remove old "Static/OTF" dir and then move/rename new static-OTF
rm -rf "$staticDir/OTF"
mv "$outputDir/static-OTF" "$staticDir/OTF"

# remove old "Static/TTF" dir and then move/rename new static-TTF
rm -rf "$staticDir/TTF"
mv "$outputDir/static-TTF" "$staticDir/TTF"
