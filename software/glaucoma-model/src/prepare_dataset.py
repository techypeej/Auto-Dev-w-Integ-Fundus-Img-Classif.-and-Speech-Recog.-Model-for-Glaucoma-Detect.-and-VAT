"""
Preprocesses the G1020 dataset and generates train/val/test CSVs.

G1020 folder structure (already provided):
    data/raw/G1020/
        Training/
            glaucoma/
            normal/
        Testing/
            glaucoma/
            normal/

Usage:
    python src/prepare_dataset.py
"""
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from preprocess import preprocess, quality_check


BASE_DIR      = Path(__file__).resolve().parent.parent
RAW_DIR       = BASE_DIR / "data/raw/G1020"
PROCESSED_DIR = BASE_DIR / "data/processed"
SPLITS_DIR    = BASE_DIR / "data/splits"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
SPLITS_DIR.mkdir(parents=True, exist_ok=True)

LABEL_MAP = {"glaucoma": 1, "normal": 0}


def process_split(split_name: str) -> list:
    """Process one split folder (Training or Testing), return list of records."""
    records = []
    skipped = 0
    split_dir = RAW_DIR / split_name

    for label_name, label in LABEL_MAP.items():
        folder = split_dir / label_name
        if not folder.exists():
            print(f"  Warning: {folder} not found, skipping.")
            continue

        for img_file in sorted(folder.iterdir()):
            if img_file.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue

            image = cv2.imread(str(img_file))
            if image is None or not quality_check(image):
                skipped += 1
                continue

            processed = preprocess(image)
            out_name  = f"{split_name}_{label_name}_{img_file.stem}.png"
            out_path  = PROCESSED_DIR / out_name
            cv2.imwrite(str(out_path), (processed * 255).astype(np.uint8))

            records.append({"filename": out_name, "label": label})

    print(f"  {split_name}: {len(records)} processed, {skipped} skipped")
    return records


def run():
    print("Processing Training split...")
    train_records = process_split("Training")

    print("Processing Testing split...")
    test_records = process_split("Testing")

    if not train_records:
        print("No training images found. Check data/raw/G1020/Training/")
        return

    # Carve a validation set out of training (80/20)
    train_df = pd.DataFrame(train_records)
    train_split, val_split = train_test_split(
        train_df, test_size=0.2, stratify=train_df["label"], random_state=42
    )

    test_df = pd.DataFrame(test_records) if test_records else pd.DataFrame(columns=["filename", "label"])

    train_split.to_csv(SPLITS_DIR / "train.csv", index=False)
    val_split.to_csv(SPLITS_DIR / "val.csv",     index=False)
    test_df.to_csv(SPLITS_DIR / "test.csv",      index=False)

    print(f"\nDone.")
    print(f"  train : {len(train_split)} images")
    print(f"  val   : {len(val_split)} images")
    print(f"  test  : {len(test_df)} images")
    print(f"  Processed images saved to: {PROCESSED_DIR}")
    print(f"  CSVs saved to: {SPLITS_DIR}")


if __name__ == "__main__":
    run()
