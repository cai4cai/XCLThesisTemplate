#!/usr/bin/env python3
# python standard library modules
import os, sys, errno
import shutil
# from optparse import OptionParser

# Sanity check
cmds = ['epstopdf', 'pdftops', 'convert']
for cmd in cmds:
    if shutil.which(cmd) is None:
        print(f"Couldn't find {cmd} -> exit")
        exit()
    else:
        print(f"Found {shutil.which(cmd)}")

all_files = os.listdir(".")

for file in all_files:
    if file.lower().endswith(".eps"):
        print("eps: " + file)
        pdf_replace = file[:-4] + ".pdf"
        png_replace = file[:-4] + ".png"
        jpeg_replace = file[:-4] + ".jpeg"
        jpg_replace = file[:-4] + ".jpg"
        
        try:
            i = all_files.index(pdf_replace)
            print("  pdflatex replace exist: " + pdf_replace)
        except ValueError:
            try:
                i = all_files.index(png_replace)
                print("  pdflatex replace exist: " + png_replace)
            except ValueError:
                try:
                    i = all_files.index(jpeg_replace)
                    print("  pdflatex replace exist: " + jpeg_replace)
                except ValueError:
                    try:
                        i = all_files.index(jpg_replace)
                        print("  pdflatex replace exist: " + jpg_replace)
                    except ValueError:
                        # no match
                        cmd = "epstopdf " + file
                        cmdline_output = os.popen(cmd).readlines()
                        print("  done pdf: " + pdf_replace)

    elif file.lower().endswith(".pdf"):
        print("pdf: " + file)
        eps_replace = file[:-4] + ".eps"
        
        try:
            i = all_files.index(eps_replace)
            print("  latex replace exist: " + eps_replace)
        except ValueError:
            # no match
            cmd = "pdftops -eps " + file
            cmdline_output = os.popen(cmd).readlines()
            print("  done eps: " + eps_replace)

    elif file.lower().endswith(".png") \
             or file.lower().endswith(".jpeg") \
             or file.lower().endswith(".jpg"):
        print("raster: " + file)
        if file.lower().endswith(".png") \
               or file.lower().endswith(".jpg"):
            eps_replace = file[:-4] + ".eps"
        else:
            eps_replace = file[:-5] + ".eps"
            
        try:
            i = all_files.index(eps_replace)
            print("  latex replace exist: " + eps_replace)
        except ValueError:
            # no match
            cmd = "convert " + file + " " + eps_replace
            cmdline_output = os.popen(cmd).readlines()
            print("  done eps: " + eps_replace)

print("Done all!")
