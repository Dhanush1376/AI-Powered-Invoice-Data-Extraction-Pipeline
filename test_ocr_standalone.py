import sys
import os
from ocr.ocr_engine import run_ocr

# Add current dir to path
sys.path.append(os.getcwd())

IMAGE_PATH = "uploads/d28b8f45-558d-47d0-bcab-35e3eab2592d_processed.jpg"

print(f"Testing OCR on {IMAGE_PATH}...")
try:
    blocks = run_ocr(IMAGE_PATH)
    print(f"Success! Found {len(blocks)} blocks.")
    for b in blocks[:5]:
        print(f"- {b['text']}")
except Exception as e:
    print(f"OCR Failed: {e}")
