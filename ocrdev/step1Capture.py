import cv2
import numpy as np
import subprocess
import os

def capture():
    screenshot_path = "full_screenshot.jpg" # Fichier temporaire
    subprocess.run(["screencapture", "-x", screenshot_path], check=True)
    x1, y1 = 1098, 566
    x2, y2 = 1780, 1367
    result_path = "result.png"

    # Couleur des lettres en hex #1b122d → BGR = (0x2d, 0x12, 0x1b)
    target_bgr = np.array([0x2d, 0x12, 0x1b], dtype=np.uint8)
    tolérance = 40

    image = cv2.imread(screenshot_path)
    if image is None:
        raise FileNotFoundError(f"Impossible de charger '{screenshot_path}'")

    # Recadrage
    cropped = image[y1:y2, x1:x2].copy()
    cropped[0:61, :]     = 255
    cropped[130:264, :]  = 255
    cropped[335:472, :]  = 255
    cropped[536:676, :]  = 255
    cropped[740:801, :]  = 255
    cropped[:, 80:195]   = 255
    cropped[:, 295:400]  = 255
    cropped[:, 490:605]  = 255

    # Filtrage couleur
    diff = cv2.absdiff(cropped, target_bgr)
    dist = np.sqrt((diff.astype(np.float32) ** 2).sum(axis=2))
    mask_letters = (dist <= tolérance)
    h, w = cropped.shape[:2]
    filtered = np.full((h, w, 3), 255, dtype=np.uint8)
    filtered[mask_letters] = cropped[mask_letters]

    cv2.imwrite(result_path, filtered)
    print(f"Image finale (contour des lettres en couleur, fond blanc) enregistrée sous '{result_path}'")

    os.remove(screenshot_path)
