import sys
import os
sys.path.append(os.getcwd())
from ocr.ocr_engine import run_ocr, _init_ocr

img = "uploads/d28b8f45-558d-47d0-bcab-35e3eab2592d_processed.jpg"
print(f"Testing OCR on {img}...")
try:
    blocks = run_ocr(img)
    print(f"Success: Found {len(blocks)} blocks.")
    for b in blocks[:3]:
        print(f"- {b['text']} @ {b['bbox']}")
except Exception as e:
    print(f"Failed: {e}")
    import traceback
    traceback.print_exc()
