# !/bin/bash

set -e

DS=$1

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    pwd
    python "./scripts--build/helpers/update-feature-code-for-statics.py" "$ufo"
    # python "scripts--build/helpers/update-feature-code-for-statics-wght_bnce_flux-med_charset.py" "$ufo"
done

# try not optimizing the CFF table, because it takes a super long time
fontmake -o otf -i -m $DS --output-dir fonts/shantell-sans-v14/static-OTF --optimize-cff=0

fontmake -o ttf -i -m $DS --output-dir fonts/shantell-sans-v14/static-TTF

# TODO? remove alts & calt code from static "normal" (non-bouncy, non-irregular) fonts
