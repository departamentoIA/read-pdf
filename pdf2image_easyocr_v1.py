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
A part of the imagen is cut depending on the coordinates of two text conditions.
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
text_condition1 = 'OG'      # Text to search for in the image
text_condition2 = 'TFE'
dx = 10

# File to write some text
f = open(output_path, "w", encoding="utf-8")

# Create OCR reader
reader = easyocr.Reader(['es', 'en'])


def save_text(cropped: np.array) -> None:
    text = reader.readtext(cropped)
    # Save the file
    for linea in text:
        f.write(linea + "\n")
        print(linea)


def text_from_image(img_np: np.array, text_condition1: str, text_condition2: str) -> None:
    '''Obtain the coordinates of the bounding box of a text found in the image.'''
    results = reader.readtext(img_np)
    # results → [ [bbox, texto, prob], ... ]
    boxes_found_1, boxes_found_2 = [], []

    # Search for text condition
    for (bbox, text, prob) in results:
        if text.strip() == text_condition1:
            print(f"Text: {text} (confidence: {prob:.1f})")
            boxes_found_1.append(bbox)
        if text.__contains__(text_condition2):
            print(f"Text: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    try:
        x1 = int(boxes_found_1[0][0][0]) - dx
        y1 = int(boxes_found_1[0][0][1])
        x2 = int(boxes_found_2[0][0][0])
        y2 = int(boxes_found_2[0][0][1])
        cropped = img_np[y1:, x1:x2]
        plt.figure(figsize=(8, 10))
        plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
        save_text(cropped)
    except:
        return


def main():
    '''All pages will be converted to images and
    these images will be cropped according to two text conditions.'''
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
        # Obtain text
        text_from_image(img_np, text_condition1, text_condition2)
    f.close()


if __name__ == "__main__":
    main()
