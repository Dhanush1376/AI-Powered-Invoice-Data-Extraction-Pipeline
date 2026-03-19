import os
import sys
import traceback

# Add current dir to path
sys.path.append(os.getcwd())

from preprocessing.preprocess import preprocess_image
from ocr.ocr_engine import run_ocr
from line_items.table_extraction import group_text_by_rows, parse_row_by_columns
from validation.validate import is_valid_line_item
from utils.cleaners import clean_description
from utils.extraction_utils import extract_invoice_number, extract_date, extract_total_amount

input_path = os.path.join("uploads", "d28b8f45-558d-47d0-bcab-35e3eab2592d.jpg")
processed_path = os.path.join("uploads", "test_verify_processed.jpg")

print(f"--- START VERIFICATION ---")

try:
    if not os.path.exists(input_path):
        print(f"[FAIL] Base image {input_path} not found.")
        sys.exit(1)

    print("[STEP] Preprocessing...")
    try:
        preprocess_image(input_path, processed_path)
        print("[OK] Preprocessing done.")
    except Exception as e:
        print(f"[FAIL] Preprocessing: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("[STEP] OCR...")
    try:
        blocks = run_ocr(processed_path)
        print(f"[OK] OCR found {len(blocks)} blocks.")
    except Exception as e:
        print(f"[FAIL] OCR: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("[STEP] Table Extraction...")
    try:
        rows = group_text_by_rows(blocks)
        final_items = []
        for row in rows:
            item = parse_row_by_columns(row["items"])
            if is_valid_line_item(item):
                item["description"] = clean_description(item["description"])
                final_items.append(item)
        print(f"[OK] Table Extraction: {len(final_items)} items.")
    except Exception as e:
        print(f"[FAIL] Table Extraction: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("[STEP] Global Extraction...")
    try:
        invoice_no = extract_invoice_number(blocks)
        invoice_date = extract_date(blocks)
        line_total_sum = sum([item["total"] for item in final_items if item.get("total") is not None])
        grand_total = extract_total_amount(blocks) or line_total_sum
        print(f"[OK] Global Extraction")
        print(f"      Inv No: {invoice_no}")
        print(f"      Date: {invoice_date}")
        print(f"      Total: {grand_total}")
    except Exception as e:
        print(f"[FAIL] Global Extraction: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("--- SUCCESS ---")

except Exception as e:
    print(f"[CRITICAL] Unexpected error: {e}")
    traceback.print_exc()
    sys.exit(1)
