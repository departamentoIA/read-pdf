from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2


pdf_path = "./data/raw/3. 2024-38-91E-85.pdf"
text_condition1 = "OG"
text_condition2 = "TFE"


def detect_text_boxes(img_np, reader, text1, text2):
    """
    Procesa una imagen con EasyOCR y devuelve los bounding boxes
    de text1 y text2 si existen.
    """

    results = reader.readtext(img_np)
    box1 = None
    box2 = None

    for (bbox, text, prob) in results:
        cleaned = text.strip()

        if cleaned == text1:
            box1 = bbox

        if text2 in cleaned:
            box2 = bbox

    return box1, box2


def draw_boxes(img, box1, box2):
    """Dibuja los bounding boxes encontrados."""

    def draw_single_box(img, box, color):
        pts = np.array(box, dtype=int)
        cv2.polylines(img, [pts], True, color, 2)

    if box1:
        draw_single_box(img, box1, (0, 255, 0))  # verde

    if box2:
        draw_single_box(img, box2, (0, 0, 255))  # rojo

    return img


def safe_imshow(name, img):
    """
    Muestra la imagen solo si es válida.
    Evita el error de NULL window.
    """
    if img is None:
        print("ERROR: imagen es None")
        return

    if img.size == 0:
        print("ERROR: imagen vacía")
        return

    img = cv2.resize(img, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
    cv2.imshow(name, img)
    cv2.waitKey(0)

    # destruir solo si la ventana existe
    try:
        cv2.destroyWindow(name)
    except:
        pass


def process_pdf(pdf_path, text1, text2):

    print("Loading OCR model...")
    reader = easyocr.Reader(['es', 'en'])

    print("Converting PDF to images...")
    pages = convert_from_path(
        pdf_path, dpi=300, poppler_path=r"C:\poppler\Library\bin")

    for idx, page in enumerate(pages, start=1):
        print(f"\n=== Page {idx} ===")

        img = np.array(page)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Detect text boxes
        box1, box2 = detect_text_boxes(img, reader, text1, text2)

        if box1 is None or box2 is None:
            print("Text condition not found")
            continue

        # Draw boxes
        img_boxed = draw_boxes(img.copy(), box1, box2)

        # Show image safely
        safe_imshow(f"Page {idx}", img_boxed)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    process_pdf(pdf_path, text_condition1, text_condition2)
