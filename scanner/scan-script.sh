#!/bin/bash
# Goes in /etc/scanbd/scripts

set -eux -o pipefail

SCAN_STATUS=/tmp/scan-status

function finish {
  rm -f $SCAN_STATUS
}
trap finish EXIT

echo "Scanning..." > $SCAN_STATUS

OUT_DIR=/mnt/smb/src/munger/scans
TMP_DIR=`mktemp -d`
FILE_NAME=scan_`date +%Y-%m-%d-%H%M%S`

echo 'scanning...'  
scanimage --resolution 300 \
          --batch="$TMP_DIR/${FILE_NAME}_%03d.pnm" \
          --format=pnm \
          --mode Color \
          --source 'ADF Duplex'
echo "Output saved in $TMP_DIR/scan*.pnm"

# cd $TMP_DIR

# for i in scan_*.pnm; do  
#     echo "${i}"
#     convert "${i}" "${i}.tiff"
# done

# for i in *.tiff; do
#     echo "converting file ${i}"
#     convert "${i}" -white-threshold 90% "processed_${i}"
#     tiff2pdf -z "processed_${i}" > "processed_${i}.pdf"
# done
# pdftk *.tiff.pdf cat output $FILE_NAME.pdf
# cp $FILE_NAME.pdf $OUT_DIR/
echo "Copying to server..." > $SCAN_STATUS
mv $TMP_DIR/*.pnm $OUT_DIR/