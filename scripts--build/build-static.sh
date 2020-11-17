# !/bin/bash

set -e

DS=$1

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    pwd
    python "./scripts--build/helpers/update-feature-code-for-statics.py" "$ufo"
done


fontmake -o otf -i -m sources/shantell-300_800.designspace --output-dir fonts/shantell-sans-v08
