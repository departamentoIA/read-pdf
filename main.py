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

import pandas as pd
from globals_functions import *
output_path_root = "./data/processed"
table_name = "./data/processed/tabla.xlsx"


def str_to_float(col: list) -> list:
    '''Converts a list of strings to a list of floats.
    Spaces, letters, dots and commas are removed.'''
    clean_list = []
    num = None
    for s in col:
        # Delete spaces
        s = s.replace(" ", "").replace(",", "").replace(";", "")
        # Delete letters
        s = "".join(c for c in s if c.isdigit() or c == ".")
        # If there is more than one decimal point, keep only the last one
        if s.count(".") > 1:
            partes = s.split(".")
            s = "".join(partes[:-1]) + "." + partes[-1]
        try:
            num = float(s)
            clean_list.append(num)
        except:
            clean_list.append(None)
    return clean_list


def delete_letters(col: list) -> list:
    '''Delete letters in a list.'''
    elements = []
    for element in col:
        data = ''.join([c for c in element if not c.isalpha()])
        if data != '':
            elements.append(data)
    return elements


def read_txt_lines(path: str) -> list:
    """Reads a .txt file and returns a list with each line as an element.
    Lines are returned without the trailing line break."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return lines


def get_txt_filenames(path: str) -> list:
    """Returns a list of the names of all .txt files
    that exist in the specified path."""
    return [fname for fname in os.listdir(path) if fname.endswith(".txt")]


def process_cols() -> None:
    '''Read the txt files to obtain the 4 columns of the final DataFrame.'''
    columns = [[], [], [], []]
    column1, column2, column3, column4 = [], [], [], []
    file_list = get_txt_filenames(output_path_root)
    file_list.sort()
    i = 0
    for file in file_list:
        columns[i] = read_txt_lines(os.path.join(output_path_root, file))
        i += 1
    column1, column2, column3, column4 = columns[0], columns[1], columns[2], columns[3],
    column3 = delete_letters(column3)
    column3 = str_to_float(column3)
    column4 = delete_letters(column4)
    column4 = str_to_float(column4)
    drop_cols = len(column3) - len(column1)
    if drop_cols > 0:
        column3 = column3[:-drop_cols]
    drop_cols = len(column4) - len(column1)
    if drop_cols > 0:
        column4 = column4[:-drop_cols]
    if len(column2) - len(column1) > 0:
        print("OCR está fallando al leer la columna 'TFEC'")
        return
    df = pd.DataFrame(
        {
            'OG': column1, 'TFE': column2, 'AMP': column3, 'RED': column4
        }
    )
    try:
        df.to_excel(table_name, index=False)
    except:
        print("El Excel está abierto, no puedo reescribirlo.")


def main():
    '''
    Text of 4 columns is obatained and saved in 4 txt files (function read_pdf).
    4 txt files are read and preprocessed to obtain the final table
    (function process_cols).
    '''
    read_pdf()
    process_cols()


if __name__ == "__main__":
    main()
