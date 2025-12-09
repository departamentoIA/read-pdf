#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File:           pdf2image2text.py
Author:         Antonio Arteaga
Last Updated:   2025-12-08
Version:        1.0
Description:
The PDF file contains flat text and tables, all pages will be converted to images.
Text is obtained using the pdf2image (with poppler) to convert the pages to images,
easyocr is used to obtain the coordinates of 2 bounding boxes of 2 text conditions,
finally, easyocr is used again to read text in the cropped image.
Data of some columns is saved in "output_path".
Dependencies:   pdf2image==1.17.0, easyocr==1.7.2, pillow==12.0.0, numpy==2.2.6,
poppler-25.07.0 installed.
"""

from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2

# Global variables-----------------------
pdf_path = "./data/raw/3. 2024-38-91E-85.pdf"
output_path = "./data/processed/text.txt"
output_path2 = "./data/processed/text2.txt"
text_condition1 = 'OG'      # Text to search for in the image
text_condition2 = 'TFE'
dx = 10
# ---------------------------------------
# File to write some text
f1 = open(output_path, "w", encoding="utf-8")
f2 = open(output_path2, "w", encoding="utf-8")

# Create OCR reader
reader = easyocr.Reader(['es', 'en'])


def save_text_from_img(file, img: np.array) -> None:
    '''Save the text read in the image.'''
    results = reader.readtext(img)
    for (bbox, text, prob) in results:
        file.write(text + "\n")


def display_img(window_name: str, img: np.array) -> None:
    cv2.imshow(window_name, img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


def text_from_column1(img_np: np.array, text_condition1: str, text_condition2: str) -> None:
    '''Obtain the coordinates of 2 bounding boxes of 2 text conditions.'''
    results = reader.readtext(img_np)
    # results → [ [bbox, texto, prob], ... ]
    boxes_found_1, boxes_found_2 = [], []

    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.strip() == text_condition1:
            print(f"Text condition: {text} (confidence: {prob:.1f})")
            boxes_found_1.append(bbox)
        if text.__contains__(text_condition2):
            print(f"Text condition: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    if (not boxes_found_1) or (not boxes_found_2):
        print(f"No text condition found in this page.")
        return

    try:
        x1 = int(boxes_found_1[0][0][0]) - dx
        y1 = int(boxes_found_1[0][0][1])
        x2 = int(boxes_found_2[0][0][0])
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates.")
            return
        # Crop image
        cropped = img_np[y1:, x1:x2]
        if cropped is None or cropped.size == 0:
            print("ERROR: cropped image empty.")
            return
        cropped = cv2.resize(cropped, None, fx=0.8, fy=0.8,
                             interpolation=cv2.INTER_LINEAR)
        display_img("Cropped Image", cropped)
        print(type(f1))
        print(type(cropped))
        save_text_from_img(f1, cropped)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column2(img_np: np.array, text_condition2: str) -> None:
    '''Obtain the coordinates of 1 bounding box.'''
    results = reader.readtext(img_np)
    # results → [ [bbox, texto, prob], ... ]
    boxes_found_2 = []

    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.__contains__(text_condition2):
            print(f"Text condition: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    if not boxes_found_2:
        print(f"No text condition found in this page for column 2.")
        return

    try:
        x1 = int(boxes_found_2[0][0][0])
        y1 = int(boxes_found_2[0][0][1])
        x2 = int(boxes_found_2[0][1][0])
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates for column 2.")
            return
        # Crop image
        cropped = img_np[y1:, x1:x2]
        if cropped is None or cropped.size == 0:
            print("ERROR: cropped image 2 empty.")
            return
        cropped = cv2.resize(cropped, None, fx=0.8, fy=0.8,
                             interpolation=cv2.INTER_LINEAR)
        display_img("Cropped Image 2", cropped)
        save_text_from_img(f2, cropped)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def main():
    '''Convert PDF to images and crop according to 2 text conditions.'''
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
        # Obtain text from image
        text_from_column1(img_np, text_condition1, text_condition2)
        text_from_column2(img_np, text_condition2)
    f1.close()
    f2.close()


if __name__ == "__main__":
    main()
