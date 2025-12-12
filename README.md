# read-pdf
Read a table from a PDF file by using easyocr python library.

## Repository Structure
```
read-pdf/
│
├── main.py
├── globals_functions.py
├── .gitignore
├── env/                # Virtual enviroment
└── requirements.txt
└── data/               # Contains all source files (PDFs, etc.)
└── easyOCR/            # Contains easyOCR models (not provided and used for executable)
    └── *.pth           # Models
└── poppler/            # Contains poppler files (not provided and used for executable)
    └── bin/            # Binary files
    └── ...
└── tesseract/          # Contains tesseract models (not provided and used for executable)
    └── tessdata/
    └── tesseract.exe
    └── ...
```
## Details
**globals_functions.py:** Contains all global variables and functions used in 'main.py'.

**main.py:** Reads and processes PDF files. The PDF file contains flat text and tables, all pages will be converted to images. Text is obtained using the pdf2image (with poppler) to convert the pages to images,
easyocr is used to obtain the coordinates of 2 bounding boxes of 2 text conditions, finally, easyocr is used again to read text in the cropped image. This process is applied to 4 columns for all pages. Columns conent is saved in "output_path1", ..., "output_path4". Finally, all columns are cleaned and saved in an Excel file.

**ocr_executable_windows:** Simple example of converting to executable a script that uses poppler, easyocr and tesseract models. This script is not part of the rest of this repository.

## 🚀 How to run locally
1. Clone this repository:
```
git clone https://github.com/departamentoIA/read-pdf.git
```
2. Set virtual environment and install dependencies.

For Windows:
```
python -m venv env
env/Scripts/activate
pip install -r requirements.txt
```
For Linux:
```
python -m venv env && source env/bin/activate && pip install -r requirements.txt
```
3. Run "main.py".

## Make executable
In order to make main.py executable, run this command:
```
pyinstaller --onefile --add-data "poppler/bin;poppler/bin" --add-data "easyOCR;easyOCR" --add-data "tesseract;tesseract" --add-data "data;data" ocr_executable_windows.py
```
