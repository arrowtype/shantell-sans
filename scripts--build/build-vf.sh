# !/bin/bash

set -e

DS=$1

parentDir=$(dirname "$DS")
for ufo in $parentDir/*.ufo; do
    pwd
    python "./scripts--build/helpers/update-feature-code-for-vf.py" "$ufo"
done

fontmake -o variable -m $DS --output-dir fonts/shantell-sans-v08
