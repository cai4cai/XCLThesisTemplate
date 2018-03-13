#!/bin/sh

# Sanity checks
if ! [ -x "$(command -v gs)" ]; then
    echo gs is not installed -> exit
    exit 1
fi

# Define some handy options to use with ghostscript
export PDF2PDFFLAGS="-dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dColorConversionStrategy=/UseDeviceIndependentColor -dDownsampleColorImages=true -dDownsampleGrayImages=true -dDownsampleMonoImages=true -dMaxSubsetPct=100 -dSubsetFonts=true -dEmbedAllFonts=true -dOptimize=true -dUseFlateCompression=true -dNOPAUSE -dBATCH -sDEVICE=pdfwrite"
# previsouly used: -dUseCIEColor=true

# Get the initial file size
init_size=$(du -h "$1" | cut -f1)

# Get the file path without the file extension
F=$1
F=${F%.*}

# Load some handy pdfmarks to open the file as I like it
pdfmarks=$(dirname "$0")/mktpdfmarks

# Use gs to compress the file in a lossy fashion
echo PDF lossy compression using:
echo $PDF2PDFFLAGS -sOutputFile="$F-compressed.pdf" "$1" $pdfmarks
gs $PDF2PDFFLAGS -sOutputFile="$F-compressed.pdf" "$1" $pdfmarks

# pdftk is not maintained anymore and does not work on my mac...
#echo pdftk $1 dump_data output /tmp/pdftk-report.txt
#pdftk $1 dump_data output /tmp/pdftk-report.txt
#echo pdftk /tmp/compressed.pdf update_info /tmp/pdftk-report.txt output $F-compressed.pdf
#pdftk /tmp/compressed.pdf update_info /tmp/pdftk-report.txt output $F-compressed.pdf

# Chrome has issues if exiftool is run last. Make sure smpdf comes afterwards
if ! [ -x "$(command -v exiftool)" ]; then
    echo Could not find exiftool - Some tags might have been lost
else
    # Restore some pdf tags that might have been lost in the process
    echo PDF tag transfer using:
    echo exiftool -overwrite_original -TagsFromFile "$1" "$F-compressed.pdf"
    exiftool -overwrite_original -TagsFromFile "$1" "$F-compressed.pdf"
fi

if ! [ -x "$(command -v smpdf)" ]; then
    echo Could not find smpdf - Skipping additional lossless compression
    echo See https://www.coherentpdf.com/compression.html
else
    # Use smpdf to further compress the file in a lossless fashion
    echo PDF lossless compression using:
    echo smpdf "$F-compressed.pdf" -o "$F-compressed2.pdf"
    smpdf "$F-compressed.pdf" -o "$F-compressed2.pdf"
    mv "$F-compressed2.pdf" "$F-compressed.pdf"
fi

if ! [ -x "$(command -v cpdf)" ]; then
    echo Could not find cpdf - Skipping additional annotation copying
    echo See https://www.coherentpdf.com/compression.html
else
    # Use cpdf to copy information over
    echo PDF ID copy using:
    echo cpdf -copy-id-from "$1" "$F-compressed.pdf" -o "$F-compressed2.pdf"
    cpdf -copy-id-from "$1" "$F-compressed.pdf" -o "$F-compressed2.pdf"
    mv "$F-compressed2.pdf" "$F-compressed.pdf"
    
    echo PDF annotation copy using:
    echo cpdf -copy-annotations "$1" "$F-compressed.pdf" -o "$F-compressed2.pdf"
    cpdf -copy-annotations "$1" "$F-compressed.pdf" -o "$F-compressed2.pdf"
    mv "$F-compressed2.pdf" "$F-compressed.pdf"
fi

# Get the new file size
new_size=$(du -h "$F-compressed.pdf" | cut -f1)

echo "\nCompressed from $init_size to $new_size"
