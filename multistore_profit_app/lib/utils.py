import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(os.getenv("DATA_DIR", "./data")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

def ensure_dir(p):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p
