#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           pdf2image_easyocr_v1.py
Author:         Antonio Arteaga
Last Updated:   2025-12-08
Version:        1.0
Description:
The PDF file contains flat text and tables, all pages will be converted to images.
Text is obtained using the pdf2image (with poppler) to convert the pages to images,
easyocr is used to obtain the coordinates of the bounding box of a condition text,
finally, tesseract_ocr is used to read text in the cropped image.
Data of some columns is saved in "output_path".
Dependencies:   pdf2image==1.17.0, easyocr==1.7.2, pillow==12.0.0, numpy==2.2.6,
poppler-25.07.0 installed.
"""

from pdf2image import convert_from_path
import easyocr
import numpy as np
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
    results = reader.readtext(cropped)
    # Save the file
    print("I read:")
    # Show text found with confidence
    for (bbox, text, prob) in results:
        print(f"Text: {text} (confidence: {prob:.1f})")
        f.write(text + "\n")


def text_from_image(img_np: np.array, text_condition1: str, text_condition2: str) -> None:
    '''Obtain the coordinates of the bounding box of a text found in the image.'''
    results = reader.readtext(img_np)
    # results → [ [bbox, texto, prob], ... ]
    boxes_found_1, boxes_found_2 = [], []

    # Search for text condition
    for (bbox, text, prob) in results:
        if text.strip() == text_condition1:
            print(f"Text condition: {text} (confidence: {prob:.1f})")
            boxes_found_1.append(bbox)
        if text.__contains__(text_condition2):
            print(f"Text condition: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    if (not boxes_found_1) or (not boxes_found_2):
        print(f"No condition text found in this page.")
        return

    try:
        x1 = int(boxes_found_1[0][0][0]) - dx
        y1 = int(boxes_found_1[0][0][1])
        x2 = int(boxes_found_2[0][0][0])
        if x1 < 0 or x2 <= x1:
            print("ERROR: invelid coordinates.")
            return
        # Crop image
        cropped = img_np[y1:, x1:x2]
        if cropped is None or cropped.size == 0:
            print("ERROR: cropped image empty.")
            return
        # cropped = cv2.resize(cropped, None, fx=2, fy=2,
        # interpolation=cv2.INTER_LINEAR)
        cv2.imshow("Cropped Image", cropped)
        cv2.waitKey(0)
        cv2.destroyWindow("Cropped Image")
        save_text(cropped)
    except Exception as e:
        print("ERROR en recorte:", e)
        return


def main():
    '''Convert PDF to images and crop according to two text conditions.'''
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
