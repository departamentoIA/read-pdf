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
from typing import Tuple, List

# Global variables-----------------------
pdf_path = "./data/raw/9. 2024-38-91E-388.pdf"
output_path1 = "./data/processed/text1.txt"
output_path2 = "./data/processed/text2.txt"
output_path3 = "./data/processed/text3.txt"
output_path4 = "./data/processed/text4.txt"
text_condition1 = 'OG'      # Text to search for in the image
text_condition2 = 'TFE'
text_condition3 = 'AMPLIACIÓN'
text_condition4 = 'REDUCCIÓN'
dx = 10
column1, column2, column3, column4 = [], [], [], []
# ---------------------------------------
# File to write some text
f1 = open(output_path1, "w", encoding="utf-8")
f2 = open(output_path2, "w", encoding="utf-8")
f3 = open(output_path3, "w", encoding="utf-8")
f4 = open(output_path4, "w", encoding="utf-8")

# Create OCR reader
reader = easyocr.Reader(['es', 'en'])


def text_from_img_raw(file, img: np.array) -> list:
    '''Save the text read in the image and return text.'''
    column_list = []
    results = reader.readtext(img)
    for (bbox, text, prob) in results:
        if text != '':
            file.write(text + "\n")
            column_list.append(text)
    return column_list


def save_text_from_img(file, img: np.array) -> list:
    '''Save the text read in the image and return the cleaned text.'''
    column_list = []
    results = reader.readtext(img)
    for (bbox, text, prob) in results:
        data = ''.join([c for c in text if c.isdigit()])
        if data != '':
            file.write(data + "\n")
            column_list.append(data)
    return column_list


def display_img(window_name: str, img: np.array) -> None:
    cv2.imshow(window_name, img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


def crop_img(img_np: np.array, x1: int, y1: int, x2: int) -> np.array:
    '''Retrive an image and return the cropped image according to coordinates'''
    cropped = img_np[y1:, x1:x2]
    if cropped is None or cropped.size == 0:
        print("ERROR: cropped image empty.")
        return
    cropped = cv2.resize(cropped, None, fx=0.7, fy=0.7,
                         interpolation=cv2.INTER_LINEAR)
    display_img("Cropped Image", cropped)
    return cropped


def text_from_column1(results: list, img_np: np.array, text_condition1: str, text_condition2: str) -> Tuple[bool, List[str]]:
    '''Obtain the coordinates of 2 bounding boxes of 2 text conditions.
    Display the cropped image and write in a file, obtain the content in column 1.
    A flag is also returned to especify that no text condition1 found.'''
    boxes_found_1, boxes_found_2 = [], []
    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.strip() == text_condition1:
            print(f"Text condition1: {text} (confidence: {prob:.1f})")
            boxes_found_1.append(bbox)
        if text.__contains__(text_condition2):
            print(f"Text condition1: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    if (not boxes_found_1) or (not boxes_found_2):
        print(f"No text condition1 found in this page.")
        return True, []

    try:
        x1 = int(boxes_found_1[0][0][0]) - dx
        y1 = int(boxes_found_1[0][0][1])
        x2 = int(boxes_found_2[0][0][0])
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates.")
            return
        cropped = crop_img(img_np, x1, y1, x2)
        column1_list = save_text_from_img(f1, cropped)
        return False, column1_list
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column2(results: list, img_np: np.array, text_condition2: str) -> list:
    '''Obtain the coordinates of 1 bounding box.
    Display the cropped image and write in a file,
    finally, obtain the content in column 2.'''
    boxes_found_2 = []
    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.__contains__(text_condition2):
            print(f"Text condition 2: {text} (confidence: {prob:.1f})")
            boxes_found_2.append(bbox)

    if not boxes_found_2:
        print(f"No text condition found in this page for column 2.")
        return

    try:
        x1 = int(boxes_found_2[0][0][0])
        y1 = int(boxes_found_2[0][0][1])
        x2 = int(boxes_found_2[0][1][0]) + 5*dx
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates for column 2.")
            return
        cropped = crop_img(img_np, x1, y1, x2)
        return save_text_from_img(f2, cropped)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column3(results: list, img_np: np.array, text_condition3: str) -> list:
    '''Obtain the coordinates of 1 bounding box.
    Display the cropped image and write in a file,
    finally, obtain the content in column 3.'''
    boxes_found_3 = []
    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.__contains__(text_condition3):
            print(f"Text condition 3: {text} (confidence: {prob:.1f})")
            boxes_found_3.append(bbox)

    if not boxes_found_3:
        print(f"No text condition found in this page for column 3.")
        return

    try:
        x1 = int(boxes_found_3[0][0][0])
        y1 = int(boxes_found_3[0][0][1])
        x2 = int(boxes_found_3[0][1][0]) + 2*dx
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates for column 3.")
            return
        cropped = crop_img(img_np, x1, y1, x2)
        return text_from_img_raw(f3, cropped)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column4(results: list, img_np: np.array, text_condition4: str) -> list:
    '''Obtain the coordinates of 1 bounding box.
    Display the cropped image and write in a file,
    finally, obtain the content in column 4.'''
    boxes_found_4 = []
    # Search for text conditions
    for (bbox, text, prob) in results:
        if text.__contains__(text_condition4):
            print(f"Text condition 4: {text} (confidence: {prob:.1f})")
            boxes_found_4.append(bbox)

    if not boxes_found_4:
        print(f"No text condition found in this page for column 4.")
        return

    try:
        x1 = int(boxes_found_4[0][0][0])
        y1 = int(boxes_found_4[0][0][1])
        x2 = int(boxes_found_4[0][1][0]) + 2*dx
        if x1 < 0 or x2 <= x1:
            print("ERROR: invalid coordinates for column 4.")
            return
        cropped = crop_img(img_np, x1, y1, x2)
        return text_from_img_raw(f4, cropped)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def main():
    '''Convert PDF to images and crop according to text conditions.'''
    cond_found = False
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
        results = reader.readtext(img_np)
        # results → [ [bbox, texto, prob], ... ]
        cond_found, column1 = text_from_column1(
            results, img_np, text_condition1, text_condition2)
        if cond_found:
            break
        column2 = text_from_column2(results, img_np, text_condition2)
        column3 = text_from_column3(results, img_np, text_condition3)
        column4 = text_from_column4(results, img_np, text_condition4)

    f1.close()
    f2.close()
    f3.close()
    f4.close()


if __name__ == "__main__":
    main()
