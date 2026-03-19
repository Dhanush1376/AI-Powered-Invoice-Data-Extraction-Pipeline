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
    _ocr = PaddleOCR(use_angle_cls=False, lang="en")
    return _ocr


def run_ocr(image_path: str) -> List[Dict[str, Any]]:
    """Run OCR on `image_path` and return a list of text blocks.

    Each block is a dict with keys: `text`, `confidence`, `bbox`.
    """
    ocr = _init_ocr()
    result = ocr.ocr(image_path)
    blocks: List[Dict[str, Any]] = []

    for line in result:
        for word in line:
            blocks.append({
                "text": word[1][0],
                "confidence": word[1][1],
                "bbox": word[0],
            })

    return blocks

