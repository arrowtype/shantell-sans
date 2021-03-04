# !/bin/bash

set -e

DS=$1

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    pwd
    python "./scripts--build/helpers/update-feature-code-for-statics.py" "$ufo"
    # python "scripts--build/helpers/update-feature-code-for-statics-wght_bnce_flux-med_charset.py" "$ufo"
done


fontmake -o otf -i -m $DS --no-production-names --output-dir fonts/shantell-sans-v13/static-OTF
# fontmake -o ttf -i -m $DS --no-production-names --output-dir fonts/shantell-sans-v13/static-TTF

# TODO? remove alts & calt code from static "normal" (non-bouncy, non-irregular) fonts
