"""OCR runner using PaddleOCR with lazy import and offline-friendly behavior.

This module avoids importing `paddleocr` at import time because that package
may perform network checks which block startup. The import and model
initialization are performed lazily on the first call to `run_ocr()`.

If `paddleocr` is not available, a clear RuntimeError is raised explaining how
to install it or how to run in an offline mode by setting
`DISABLE_MODEL_SOURCE_CHECK=True` in the environment.
"""
from __future__ import annotations

import os
from typing import List, Dict, Any, Optional

# Respect an existing env var but ensure a sensible default to avoid long
# network checks when importing paddlex/paddleocr.
os.environ.setdefault("DISABLE_MODEL_SOURCE_CHECK", "True")

# Cache the initialized OCR object so we only create it once.
_ocr: Optional[object] = None


def _init_ocr() -> object:
    """Import and initialize PaddleOCR, returning the OCR instance.

    Raises:
        RuntimeError: if PaddleOCR cannot be imported/initialized.
    """
    global _ocr
    if _ocr is not None:
        return _ocr

    try:
        # Import here to avoid performing network checks during module import.
        from paddleocr import PaddleOCR
    except Exception as exc:  # pragma: no cover - environment-specific
        raise RuntimeError(
            "PaddleOCR is required for OCR processing but could not be imported. "
            "Install it with `pip install paddleocr` or set the environment "
            "variable DISABLE_MODEL_SOURCE_CHECK=True to bypass remote checks. "
            f"Original error: {exc!s}"
        ) from exc

    # Initialize with sensible defaults; adjust parameters as needed.
    _ocr = PaddleOCR(use_angle_cls=False, lang="en", enable_mkldnn=False)
    return _ocr


def run_ocr(image_path: str) -> List[Dict[str, Any]]:
    """Run OCR on `image_path` and return a list of text blocks.

    Each block is a dict with keys: `text`, `confidence`, `bbox`.
    """
    ocr = _init_ocr()
    result = ocr.ocr(image_path)
    blocks: List[Dict[str, Any]] = []

    if result is None:
        return []
    
    # Handle PaddleOCR 3.x / PaddleX format where result is a list of dicts
    # Each dict: {'input_path': ..., 'page_index': ..., 'res': ...}
    if result and isinstance(result[0], dict) and "res" in result[0]:
        blocks_data = []
        for page in result:
            res = page.get("res")
            if isinstance(res, dict):
                # New dictionary-based format
                texts = res.get("rec_texts", [])
                scores = res.get("rec_scores", [])
                boxes = res.get("rec_boxes", res.get("det_polygons", []))
                for i in range(len(texts)):
                    blocks_data.append({
                        "text": texts[i],
                        "confidence": scores[i] if i < len(scores) else 0,
                        "bbox": boxes[i] if i < len(boxes) else [],
                    })
            elif isinstance(res, list):
                # Old list-based format wrapped in dict
                for item in res:
                    if isinstance(item, dict):
                        blocks_data.append({
                            "text": item.get("text", ""),
                            "confidence": item.get("confidence", 0),
                            "bbox": item.get("bbox", []),
                        })
                    elif isinstance(item, (list, tuple)) and len(item) > 1:
                        blocks_data.append({
                            "text": item[1][0],
                            "confidence": item[1][1],
                            "bbox": item[0],
                        })
        return blocks_data

    return blocks

