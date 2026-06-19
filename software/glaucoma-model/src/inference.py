"""
Single-image inference using a Teachable Machine exported Keras model (.h5).

Export from Teachable Machine:
    Tensorflow tab → Keras → Download Model → place .h5 in weights/

Usage:
    python src/inference.py <path_to_image>
"""
import sys
import cv2
import numpy as np
from pathlib import Path

BASE_DIR     = Path(__file__).resolve().parent.parent
WEIGHTS_PATH = BASE_DIR / "weights/teachable_machine_model.h5"

# Must match labels.txt order in weights/
CLASS_NAMES = ["Glaucoma", "Normal"]

_model = None


def load_model(weights_path: str = None):
    global _model
    import tf_keras
    path = weights_path or str(WEIGHTS_PATH)
    _model = tf_keras.models.load_model(path, compile=False)


def _quality_check(image: np.ndarray) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.mean() >= 20.0 and cv2.Laplacian(gray, cv2.CV_64F).var() >= 2.0


def predict(image_path: str, weights_path: str = None) -> dict:
    global _model
    if _model is None:
        load_model(weights_path)

    image = cv2.imread(image_path)
    if image is None:
        return {"result": None, "confidence": None, "glaucoma_probability": None,
                "error": f"Could not read image: {image_path}"}

    if not _quality_check(image):
        return {"result": None, "confidence": None, "glaucoma_probability": None,
                "error": "Image failed quality check: too dark or too blurry — recapture"}

    # Teachable Machine expects color (BGR→RGB), 224x224, normalized [0, 1]
    image_rgb     = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (224, 224))
    tensor        = np.expand_dims(image_resized.astype(np.float32) / 255.0, axis=0)

    probs = _model.predict(tensor, verbose=0)[0]
    pred  = int(np.argmax(probs))

    return {
        "result":               CLASS_NAMES[pred],
        "confidence":           round(float(probs[pred]) * 100, 1),
        "glaucoma_probability": round(float(probs[CLASS_NAMES.index("Glaucoma")]) * 100, 1),
        "error":                None,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/inference.py <image_path>")
    else:
        print(predict(sys.argv[1]))
