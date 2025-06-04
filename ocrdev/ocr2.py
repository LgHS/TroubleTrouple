import cv2
import numpy as np
import pytesseract
import os

INPUT_PATH  = "result.png"       # Image recadrée & seuillée (cases blanches sur fond noir)
OUTPUT_DIR  = "cells_detected"   # Dossier où on enregistrera chaque case (pour debug)
GRID_SIZE   = 4                  # 4×4 cases
TESS_CONFIG = "--psm 10 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"

os.makedirs(OUTPUT_DIR, exist_ok=True)

img = cv2.imread(INPUT_PATH)
if img is None:
    raise FileNotFoundError(f"Impossible de charger '{INPUT_PATH}'")

h, w = img.shape[:2]
cell_h = h // GRID_SIZE
cell_w = w // GRID_SIZE


grid_letters = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        y1 = i * cell_h
        y2 = y1 + cell_h
        x1 = j * cell_w
        x2 = x1 + cell_w
        cell = img[y1:y2, x1:x2]
        cell_path = os.path.join(OUTPUT_DIR, f"case_{i}_{j}.png")
        cv2.imwrite(cell_path, cell)


        moyenne = cv2.mean(cell)[0]
        if moyenne > 127:
            cell_bin = cv2.bitwise_not(cell)
        else:
            cell_bin = cell.copy()

        kernel = np.ones((3,3), np.uint8)
        cell_bin = cv2.erode(cell_bin, kernel, iterations=1)
        
        h2, w2 = cell_bin.shape[:2]
        dx = int(w2 * 0.20)
        dy = int(h2 * 0.20)
        cell_central = cell_bin[dy:h2-dy, dx:w2-dx]

        kernel2 = np.ones((2,2), np.uint8)
        cell_central = cv2.dilate(cell_central, kernel2, iterations=1)

        lettre = pytesseract.image_to_string(
            cell_central,
            config=TESS_CONFIG
        ).strip().upper()

        if len(lettre) > 1:
            lettre = lettre[0]

        if not lettre or not lettre.isalpha():
            lettre = "?"

        grid_letters[i][j] = lettre

print("\n=== Lettres détectées par case (ligne x colonne) ===\n")
for i in range(GRID_SIZE):
    ligne = " ".join(grid_letters[i][j] for j in range(GRID_SIZE))
    print(ligne)
