#!/bin/bash
# Usage:
#   ./test_model.sh                  → tests teachable_machine_model.h5 (current active model)
#   ./test_model.sh weights/keras_model.h5  → tests a specific model file

source venv/bin/activate
python src/evaluate.py "$1"
