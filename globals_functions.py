# globals_functions.py
import os
from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2
from pathlib import Path
import sys

if not os.path.exists("./data/processed"):
    os.makedirs("./data/processed")

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
# ---------------------------------------
# Files to write some text
f1 = open(output_path1, "w", encoding="utf-8")
f2 = open(output_path2, "w", encoding="utf-8")
f3 = open(output_path3, "w", encoding="utf-8")
f4 = open(output_path4, "w", encoding="utf-8")

# Base path (normal script or .exe)
if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).resolve().parent

# Poppler
poppler_path = os.path.join(base_path, "poppler", "bin")

# EasyOCR
easyocr_model_path = os.path.join(base_path, "easyOCR")

# Create OCR reader
reader = easyocr.Reader(['es', 'en'],
                        model_storage_directory=easyocr_model_path,
                        download_enabled=False)


def txt_from_img(file, img: np.array, raw=True) -> None:
    '''Save the text read in the image and return the cleaned text.'''
    results = reader.readtext(img)
    for (bbox, text, prob) in results:
        if raw == False:
            data = ''.join([c for c in text if c.isdigit()])
        else:
            data = text
        if data != '':
            file.write(data + "\n")


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


def text_from_column1(results: list, img_np: np.array, text_condition1: str, text_condition2: str) -> bool:
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
        txt_from_img(f1, cropped, False)
        return False
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column2(results: list, img_np: np.array, text_condition2: str) -> None:
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
        txt_from_img(f2, cropped, False)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column3(results: list, img_np: np.array, text_condition3: str) -> None:
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
        txt_from_img(f3, cropped, True)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def text_from_column4(results: list, img_np: np.array, text_condition4: str) -> None:
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
        txt_from_img(f4, cropped, True)
    except Exception as e:
        # print("ERROR en recorte: ", e)
        return


def read_pdf():
    '''Convert PDF to images and crop according to text conditions.
    Text of 4 columns are saved in txt files.'''
    cond_found = False
    # Convert PDF to images (for Windows)
    imagenes_pil = convert_from_path(
        pdf_path, dpi=300, poppler_path=poppler_path)

    # Process every page
    for i, img in enumerate(imagenes_pil, start=1):
        print(f"\n========== Page {i} ==========")
        # Convert PIL Image → NumPy for EasyOCR
        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        results = reader.readtext(img_np)
        # results → [ [bbox, texto, prob], ... ]
        cond_found = text_from_column1(
            results, img_np, text_condition1, text_condition2)
        if cond_found:
            break
        text_from_column2(results, img_np, text_condition2)
        text_from_column3(results, img_np, text_condition3)
        text_from_column4(results, img_np, text_condition4)
    f1.close()
    f2.close()
    f3.close()
    f4.close()
