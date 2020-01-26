#!/bin/bash

set -eux -o pipefail

SCAN_STATUS=/tmp/scan-status

function finish {
  rm -f $SCAN_STATUS
}
trap finish EXIT

echo "Scanning..." > $SCAN_STATUS

OUT_DIR=<%= @out_dir %>
TMP_DIR=`mktemp -d`
FILE_NAME=scan_`date +%Y-%m-%d-%H%M%S`

echo 'scanning...'  
scanimage --resolution 300 \
          --batch="$TMP_DIR/${FILE_NAME}_%03d.pnm" \
          --format=pnm \
          --mode Color \
          --source 'ADF Duplex'
echo "Output saved in $TMP_DIR/scan*.pnm"

echo "Copying to server..." > $SCAN_STATUS
mv $TMP_DIR/*.pnm $OUT_DIR/