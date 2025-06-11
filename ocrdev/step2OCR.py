import cv2
import numpy as np
import pytesseract
import os

def analyseImage():

    # Configuration / Chemins
    IMAGE_PATH   = "result.png"       # Fichier venant de la Step 1
    GRID_SIZE    = 4                  # Grille 4×4
    DEBUG_FOLDER = "debug_cases"      # Dossier de debug
    os.makedirs(DEBUG_FOLDER, exist_ok=True)

    # Paramètres Tesseract
    TESS_CONFIG_CHAR  = "--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    TESS_CONFIG_BLOCK = "--psm 7  -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Facteur d’agrandissement du ROI avant appel à Tesseract
    SCALE_FACTOR = 2.0

    # Kernels morphologiques
    KERNEL_CLOSE = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    KERNEL_OPEN  = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    KERNEL_DIL   = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Nombre d’itérations pour les opérations morphologiques
    CLOSE_ITERS  = 1    # fermeture pour reconnecter (“E”, “N”, “B”)
    OPEN_ITERS   = 1    # ouverture pour enlever petits bruit
    DILATE_ITERS = 2    # dilatation pour épaissir toutes les lettres, surtout “I”

    # Lecture et découpage de l’image
    img = cv2.imread(IMAGE_PATH)
    if img is None:
        raise FileNotFoundError(f"Impossible de charger '{IMAGE_PATH}'")

    h_full, w_full = img.shape[:2]
    cell_h = h_full // GRID_SIZE
    cell_w = w_full // GRID_SIZE

    print("\n=== Résultat OCR (4×4) ===\n")

    letters=[]
    # Traitement cellule par cellule
    for i in range(GRID_SIZE):
        row_letters = []
        for j in range(GRID_SIZE):
            y0 = i * cell_h
            y1 = y0 + cell_h
            x0 = j * cell_w
            x1 = x0 + cell_w
            cell = img[y0:y1, x0:x1]

            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            bin_inv = cv2.adaptiveThreshold(
                blurred,
                maxValue=255,
                adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv2.THRESH_BINARY_INV,
                blockSize=15,
                C=3
            )

            bin_close = cv2.morphologyEx(bin_inv, cv2.MORPH_CLOSE, KERNEL_CLOSE, iterations=CLOSE_ITERS)
            bin_open = cv2.morphologyEx(bin_close, cv2.MORPH_OPEN, KERNEL_OPEN, iterations=OPEN_ITERS)
            bin_dil = cv2.dilate(bin_open, KERNEL_DIL, iterations=DILATE_ITERS)
            contours, _ = cv2.findContours(
                bin_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            if contours:
                max_cnt = max(contours, key=cv2.contourArea)
                x, y, w_box, h_box = cv2.boundingRect(max_cnt)
                pad = 2  # pixels de marge pour ne pas rogner
                x0r = max(x - pad, 0)
                y0r = max(y - pad, 0)
                x1r = min(x + w_box + pad, cell_w - 1)
                y1r = min(y + h_box + pad, cell_h - 1)
                roi = bin_dil[y0r:y1r + 1, x0r:x1r + 1]
            else:
                roi = bin_dil.copy()

            h_r, w_r = roi.shape
            if h_r > 0 and w_r > 0:
                roi_big = cv2.resize(
                    roi,
                    (int(w_r * SCALE_FACTOR), int(h_r * SCALE_FACTOR)),
                    interpolation=cv2.INTER_LINEAR
                )
            else:
                roi_big = roi.copy()

            debug_path = os.path.join(DEBUG_FOLDER, f"cell_{i}_{j}.png")
            cv2.imwrite(debug_path, roi_big)

            txt = pytesseract.image_to_string(
                roi_big,
                config=TESS_CONFIG_CHAR
            ).strip().upper()
            if len(txt) > 1:
                txt = txt[0]
            if not txt.isalpha():
                txt2 = pytesseract.image_to_string(
                    roi_big,
                    config=TESS_CONFIG_BLOCK
                ).strip().upper()
                if txt2 and txt2[0].isalpha():
                    txt = txt2[0]
                else:
                    txt = "?"
            row_letters.append(txt)
        letters.append(row_letters)
        print(" ".join(row_letters))

    return letters
    
