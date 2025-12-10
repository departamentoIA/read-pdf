#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           read_pdf.py
Author:         Antonio Arteaga
Last Updated:   2025-12-12
Version:        1.0
Description:
The PDF file contains flat text and tables, all pages will be converted to images.
Text is obtained using the pdf2image (with poppler) to convert the pages to images,
easyocr is used to obtain the coordinates of 2 bounding boxes of 2 text conditions,
finally, easyocr is used again to read text in the cropped image. This process is
applied to 4 columns for all pages.
Columns conent is saved in "output_path1", ..., "output_path4".
Dependencies:   pdf2image==1.17.0, easyocr==1.7.2, pillow==12.0.0, numpy==2.2.6,
poppler-25.07.0 installed.
"""

from globals_functions import *


def main():
    read_pdf()


if __name__ == "__main__":
    main()
