"""
Evaluates the Teachable Machine model on the G1020 test set.

Usage:
    python src/evaluate.py
"""
import cv2
import numpy as np
import tf_keras
from pathlib import Path


BASE_DIR     = Path(__file__).resolve().parent.parent
WEIGHTS_PATH = BASE_DIR / "weights/teachable_machine_model.h5"
TEST_DIR     = BASE_DIR / "data/raw/G1020/Testing"
CLASS_NAMES  = ["Glaucoma", "Normal"]


def predict(model, image_path: str) -> int:
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    tensor = np.expand_dims(img.astype(np.float32) / 255.0, axis=0)
    probs = model.predict(tensor, verbose=0)[0]
    return int(np.argmax(probs))


def run(model_path: str = None):
    path = model_path or str(WEIGHTS_PATH)
    print(f"Loading model: {path}")
    model = tf_keras.models.load_model(path, compile=False)

    tp, tn, fp, fn = 0, 0, 0, 0

    print("Evaluating glaucoma images...")
    for f in sorted((TEST_DIR / "glaucoma").iterdir()):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            pred = predict(model, str(f))
            if pred == 0: tp += 1   # correctly identified glaucoma
            else:         fn += 1   # missed glaucoma (dangerous)

    print("Evaluating normal images...")
    for f in sorted((TEST_DIR / "normal").iterdir()):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            pred = predict(model, str(f))
            if pred == 1: tn += 1   # correctly cleared normal
            else:         fp += 1   # false alarm

    total       = tp + tn + fp + fn
    accuracy    = (tp + tn) / total * 100
    sensitivity = tp / (tp + fn) * 100
    specificity = tn / (tn + fp) * 100

    print()
    print("=" * 40)
    print(f"  Total images  : {total}")
    print(f"  Accuracy      : {accuracy:.1f}%")
    print(f"  Sensitivity   : {sensitivity:.1f}%  (glaucoma detection rate)")
    print(f"  Specificity   : {specificity:.1f}%  (normal clearance rate)")
    print(f"  TP={tp}  TN={tn}  FP={fp}  FN={fn}")
    print("=" * 40)


if __name__ == "__main__":
    import sys
    model_path = sys.argv[1] if len(sys.argv) > 1 else None
    run(model_path)
