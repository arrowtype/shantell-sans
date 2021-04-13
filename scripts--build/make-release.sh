# !/bin/bash

fontDir="fonts/Shantell Sans"

cp "scripts--build/release-data/ABOUT" "$fontDir/ABOUT"
cp "LICENSE.txt" "$fontDir/LICENSE"

function zipit {
  currentDir=$(pwd)                             # get current dir so you can return later
  cd $(dirname "$1")                              # change to target’s dir (works better for zip)
  target=$(basename "$1")                         # get target’s name
  zip -r $target.zip $target -x '*/.DS_Store'   # make a zip of the target, excluding macOS metadata
  echo "zip made of " "$1"                        # announce completion
  cd $currentDir                                # return to where you were
}

zipit $fontDir

version=$(cat "version.txt")
mv "$fontDir.zip" "$fontDir-v$version.zip"
