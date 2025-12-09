
from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2

pdf_path = "./data/raw/3. 2024-38-91E-85.pdf"
output_path = "./data/processed/text.txt"
text_condition1 = 'OG'
text_condition2 = 'TFE'
dx = 10

f = open(output_path, "w", encoding="utf-8")
reader = easyocr.Reader(['es', 'en'])


def save_text(cropped: np.array) -> None:
    results = reader.readtext(cropped)
    print("I read:")

    for (bbox, text, prob) in results:
        print(f"Text: {text} (confidence: {prob:.2f})")
        f.write(text + "\n")   # escribir texto correctamente


def text_from_image(img_np: np.array, text_condition1: str, text_condition2: str) -> None:
    results = reader.readtext(img_np)
    boxes_found_1, boxes_found_2 = [], []

    # Buscar textos
    for (bbox, text, prob) in results:
        if text.strip() == text_condition1:
            boxes_found_1.append(bbox)
        if text_condition2 in text:
            boxes_found_2.append(bbox)

    # ---- Validaciones ----
    if not boxes_found_1:
        print(f"No se encontró '{text_condition1}' en esta página.")
        return

    if not boxes_found_2:
        print(f"No se encontró '{text_condition2}' en esta página.")
        return

    try:
        x1 = int(boxes_found_1[0][0][0]) - dx
        y1 = int(boxes_found_1[0][0][1])
        x2 = int(boxes_found_2[0][0][0])

        # Validar rango
        if x1 < 0 or x2 <= x1:
            print("Error: coordenadas inválidas para el recorte.")
            return

        cropped = img_np[y1:, x1:x2]

        # Validar que la imagen no esté vacía
        if cropped is None or cropped.size == 0:
            print("ERROR: imagen recortada vacía.")
            return

        cv2.imshow("Cropped Image", cropped)
        cv2.waitKey(0)
        cv2.destroyWindow("Cropped Image")

        save_text(cropped)

    except Exception as e:
        print("ERROR en recorte o display:", e)
        return


def main():
    imagenes_pil = convert_from_path(
        pdf_path, dpi=300, poppler_path=r"C:\poppler\Library\bin"
    )

    for i, img in enumerate(imagenes_pil, start=1):
        print(f"\n========== Page {i} ==========")

        img_np = np.array(img)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        text_from_image(img_np, text_condition1, text_condition2)

    f.close()


if __name__ == "__main__":
    main()
