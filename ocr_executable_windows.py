#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           ocr_executable_windows.py
Author:         Antonio Arteaga
Last Updated:   2025-11-19
Version:        1.0
Description:
Simple example of converting to executable a script that uses poppler,
easyocr and tesseract models.
Dependencies:   pdf2image==1.17.0, easyocr==1.7.2, pillow==12.0.0, numpy==2.2.6,
poppler-25.07.0 and tesseractOCR installed.
Instructions for portability:
Copy the content of r'C:/poppler/Library' in the folder './poppler'.
Copy content of (hidden folder) r'C:/Users/youruser/.EasyOCR/model' in './easyOCR'.
Copy the content of r'C:/Program Files/Tesseract-OCR' in './tesseract'.
To make this project executable, run (3 lines are 1 line):
pyinstaller --onefile --add-data "./poppler/bin;poppler/bin"
--add-data "./easyOCR;easyOCR" --add-data "./tesseract;tesseract"
ocr_executable_windows.py
Finally, paste folder './data' in the same path of your executable.exe created
in './dist'
"""

import sys
import os
from pdf2image import convert_from_path
import easyocr
import numpy as np
import pytesseract as tess
from PIL import Image
from pathlib import Path

pdf_path = "./data/raw/3. 2024-38-91E-85.pdf"
img_path = "./data/raw/example.png"

# Base path (normal script or .exe)
if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent


# Poppler
poppler_path = os.path.join(base_path, "poppler", "bin")

# Tesseract
tess.pytesseract.tesseract_cmd = os.path.join(
    base_path, "tesseract", "tesseract.exe")

# EasyOCR
easyocr_model_path = os.path.join(base_path, "easyOCR")


# Create OCR reader
reader = easyocr.Reader(['es', 'en'],
                        model_storage_directory=easyocr_model_path,
                        download_enabled=False)

# Convert PDF to images (for Windows)
imagenes = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)

# Convert PDF to images (for Linux)
# imagenes = convert_from_path(pdf_path, dpi=200)

# Use easyOCR
for i, img in enumerate(imagenes, start=1):
    print(f"\n--- Page {i} ---\n")
    # Convert PIL Image → NumPy for EasyOCR
    img_np = np.array(img)
    # Perform easyOCR
    texto = reader.readtext(img_np, detail=0)
    print(f"{texto[:10]} ...")

# Load image
img = Image.open('./data/raw/example.png')

#  Use tesseractOCR
text = tess.image_to_string(img, lang='eng')
print(text)
