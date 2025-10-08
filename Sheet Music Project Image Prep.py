import cv2
import numpy as np

def clean_sheet_music(image_path, output_path):

    # Load image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(img, (3, 3), 0)

    # Adaptive thresholding to binarize the image
    thresh = cv2.adaptiveThreshold(
        
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    # Morphological operations to remove small noise and connect lines
    kernel = np.ones((1, 3), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Invert image back if needed
    result = cv2.bitwise_not(cleaned)
