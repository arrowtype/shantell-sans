# !/bin/bash

version=$(cat "version.txt")

fontDir="fonts/Shantell Sans"
releaseDir="fonts/Shantell Sans $version"

# clean up prior run
rm -rf "$releaseDir"
rm -rf ${releaseDir// /_}.zip

# make new folder for release
cp -r "$fontDir" "$releaseDir"

# copy in supporting documents
cp "scripts--build/release-data/ABOUT" "$releaseDir/1 - About"
cp "OFL.txt" "$releaseDir/2 - License"

# remove TTFs for simplicity
rm -rf "$releaseDir/Desktop/Static/TTF"

# move OTFs to top level of Desktop dir
mv "$releaseDir/Desktop/Static/OTF" "$releaseDir/Desktop"

# remove old Static dir
rm -rf "$releaseDir/Desktop/Static"

# change OTF folder name to simply Static
mv "$releaseDir/Desktop/OTF" "$releaseDir/Desktop/Static"

function zipit {
  currentDir=$(pwd)                             # get current dir so you can return later
  cd $(dirname "$1")                              # change to target’s dir (works better for zip)
  target=$(basename "$1")                         # get target’s name
  zip -r "${target// /_}.zip" "$target" -x '*/.DS_Store'   # make a zip of the target, excluding macOS metadata
  echo "zip made of " "$1"                        # announce completion
  cd $currentDir                                # return to where you were
}

zipit "$releaseDir"

rm -r "$releaseDir"
