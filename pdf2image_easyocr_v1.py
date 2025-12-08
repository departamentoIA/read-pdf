#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           pdf2image_easyocr_v1.py
Author:         Antonio Arteaga
Last Updated:   2025-12-08
Version:        1.0
Description:
Text is obtained from a PDF file by using the pdf2image (with poppler) and easyocr libraries.
The PDF file contains flat text and tables, all pages will be converted to images.
A part of the imagen is cut depending on the coordinates of a text condition.
Some columns are saved in "output_path".
Dependencies:   pdf2image==1.17.0, easyocr==1.7.2, pillow==12.0.0, numpy==2.2.6,
poppler-25.07.0 installed.
"""

from pdf2image import convert_from_path
import easyocr
import numpy as np
import matplotlib.pyplot as plt
import cv2

pdf_path = "./data/raw/3. 2024-38-91E-85.pdf"
output_path = "./data/processed/text.txt"
text_condition = 'OG'      # Text to search for in the image

# Create OCR reader
reader = easyocr.Reader(['es', 'en'])


def text_from_image(img_np: np.array, text_condition: str):
    '''Obtain the coordinates of the bounding box of a text found in the image.'''
    results = reader.readtext(img_np)
    # results → [ [bbox, texto, prob], ... ]
    boxes_found = []

    # Search for text condition
    for (bbox, text, prob) in results:
        if text.strip() == text_condition:
            print(f"Text: {text} (confidence: {prob:.1f})")
            boxes_found.append(bbox)

    output_img = img_np.copy()

    # Show image with bounding boxes
    for bbox in boxes_found:
        pts = np.array(bbox).astype(int)
        cv2.polylines(output_img, [pts], isClosed=True,
                      color=(0, 255, 0), thickness=3)

    plt.figure(figsize=(8, 10))
    plt.imshow(cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()
    return boxes_found


# Convert PDF to images (for Windows)
imagenes_pil = convert_from_path(
    pdf_path, dpi=300, poppler_path=r"C:\poppler\Library\bin")

# Convert PDF to images (for Linux)
# imagenes = convert_from_path(pdf_path, dpi=200)

# Process every page
for i, img in enumerate(imagenes_pil, start=1):
    print(f"\n========== Page {i} ==========")
    # Convert PIL Image → NumPy for EasyOCR
    img_np = np.array(img)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    # Perform OCR
    boxes = text_from_image(img_np, text_condition)
    try:
        print(boxes[0][0])
    except:
        pass
