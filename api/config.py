import os
from pathlib import Path

MODELS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "models")
ENCODERS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "encoders")

os.makedirs(MODELS_ROOT_PATH, exist_ok=True)
os.makedirs(ENCODERS_ROOT_PATH, exist_ok=True)
