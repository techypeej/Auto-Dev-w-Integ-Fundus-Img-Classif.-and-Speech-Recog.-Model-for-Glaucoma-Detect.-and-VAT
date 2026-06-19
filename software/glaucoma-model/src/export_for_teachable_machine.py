"""
Organizes preprocessed images into class subfolders for Teachable Machine upload.

Teachable Machine expects images grouped by class — run this after prepare_dataset.py.

Output:
    data/teachable_machine/
        glaucoma/   <- upload all these as "Glaucoma" class
        normal/     <- upload all these as "Normal" class

Usage:
    python src/export_for_teachable_machine.py
"""
import shutil
import pandas as pd
from pathlib import Path


BASE_DIR      = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data/processed"
SPLITS_DIR    = BASE_DIR / "data/splits"
OUT_DIR       = BASE_DIR / "data/teachable_machine"

LABEL_MAP = {0: "normal", 1: "glaucoma"}


def run():
    # Create output class folders
    for label_name in LABEL_MAP.values():
        (OUT_DIR / label_name).mkdir(parents=True, exist_ok=True)

    # Use all splits (train + val + test) — Teachable Machine handles its own split
    all_dfs = []
    for split in ["train.csv", "val.csv", "test.csv"]:
        csv_path = SPLITS_DIR / split
        if csv_path.exists():
            all_dfs.append(pd.read_csv(csv_path))

    if not all_dfs:
        print("No CSVs found. Run prepare_dataset.py first.")
        return

    df = pd.concat(all_dfs, ignore_index=True)

    copied = {0: 0, 1: 0}
    for _, row in df.iterrows():
        src  = PROCESSED_DIR / row["filename"]
        dest = OUT_DIR / LABEL_MAP[row["label"]] / row["filename"]
        if src.exists():
            shutil.copy2(str(src), str(dest))
            copied[row["label"]] += 1

    print("Done. Upload these folders to Teachable Machine:")
    print(f"  Glaucoma : {OUT_DIR}/glaucoma/  ({copied[1]} images)")
    print(f"  Normal   : {OUT_DIR}/normal/    ({copied[0]} images)")
    print(f"\nAfter training, export the model as Keras (.h5) and place it in:")
    print(f"  {BASE_DIR}/weights/teachable_machine_model.h5")


if __name__ == "__main__":
    run()
