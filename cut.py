import cv2

image_path = "sample.png"
x1, y1 = 200, 400
x2, y2 = 1000, 1200
result_path = "result.png"

image = cv2.imread(image_path)
if image is None:
    raise FileNotFoundError(f"Impossible de charger '{image_path}'")

cropped = image[y1:y2, x1:x2]

gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray,
    maxValue=255,
    adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    thresholdType=cv2.THRESH_BINARY_INV,
    blockSize=11,
    C=3
)

cv2.imwrite(result_path, thresh)
print(f"Crop + seuillage appliqués : '{result_path}' généré.")
