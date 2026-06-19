import cv2
import numpy as np


def quality_check(image: np.ndarray, min_mean: float = 20.0, min_laplacian: float = 2.0) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if gray.mean() < min_mean:
        return False
    if cv2.Laplacian(gray, cv2.CV_64F).var() < min_laplacian:
        return False
    return True


def preprocess(image: np.ndarray, size: int = 512) -> np.ndarray:
    # Green channel has the most diagnostic info and is least affected by color differences
    green = image[:, :, 1]

    # CLAHE normalizes contrast regardless of illumination source (LED vs clinical xenon)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    green = clahe.apply(green)

    green = cv2.resize(green, (size, size))

    # Models expect 3-channel input
    green_3ch = cv2.merge([green, green, green])

    return green_3ch.astype(np.float32) / 255.0


def preprocess_file(path: str, size: int = 512) -> np.ndarray:
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Could not read image: {path}")
    if not quality_check(image):
        raise ValueError("Image failed quality check: too dark or too blurry — recapture")
    return preprocess(image, size)
