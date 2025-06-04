import cv2
import numpy as np

# Chemins et coordonnées de recadrage
image_path  = "sample2.jpg"
x1, y1      = 1098, 566
x2, y2      = 1780, 1367
result_path = "result.png"

# Couleur des lettres en hex #1b122d → BGR = (0x2d, 0x12, 0x1b)
target_bgr = np.array([0x2d, 0x12, 0x1b], dtype=np.uint8)
tolérance = 40  # tolérance de distance couleur (ajustez si nécessaire)

# 1. Chargement de l’image
image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Impossible de charger '{image_path}'")

# 2. Recadrage
cropped = image[y1:y2, x1:x2].copy()

# 3. Remplissage des zones par du blanc (255)
cropped[0:61, :]     = 255
cropped[130:264, :]  = 255
cropped[335:472, :]  = 255
cropped[536:676, :]  = 255
cropped[740:801, :]  = 255

cropped[:, 80:195]   = 255
cropped[:, 295:400]  = 255
cropped[:, 490:605]  = 255

# 4. Filtrage couleur : tout ce qui n'est pas proche de #1b122d devient blanc
#    - On calcule la distance euclidienne en BGR entre chaque pixel et target_bgr
diff = cv2.absdiff(cropped, target_bgr)                # différence absolue canal par canal
dist = np.sqrt((diff.astype(np.float32) ** 2).sum(axis=2))  # distance euclidienne

#    - On construit un masque où pixels proches de target (lettres) restent,
#      les autres (dist > tolérance) passeront en blanc
mask_letters = (dist <= tolérance)

# Créer une image blanche de même taille
h, w = cropped.shape[:2]
filtered = np.full((h, w, 3), 255, dtype=np.uint8)

# Copier les pixels “lettre” dans filtered, le reste reste blanc
filtered[mask_letters] = cropped[mask_letters]

# 5. Enregistrement du résultat (crop + remplissage + filtrage couleur)
cv2.imwrite(result_path, filtered)
print(f"Image finale (contour des lettres en couleur, fond blanc) enregistrée sous '{result_path}'")