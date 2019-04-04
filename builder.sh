#!/bin/bash

if [! -d "builds" ]; then
    mkdir builds;
fi
OUTFILE="builds/ender.zip"

rm -rf $OUTFILE
echo "Creating zipfile..."
zip $OUTFILE -j __main__.py beacon.py
echo "Enderman installer saved to $OUTFILE."