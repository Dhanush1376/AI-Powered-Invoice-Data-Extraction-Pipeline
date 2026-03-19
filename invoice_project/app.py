import json
from preprocessing.preprocess import preprocess_image
from ocr.ocr_engine import run_ocr
from line_items.table_extraction import group_text_by_rows, parse_row_by_columns
from validation.validate import is_valid_line_item
from utils.cleaners import clean_description

INPUT_IMAGE = "input/invoice.jpg"
PREPROCESSED_IMAGE = "input/preprocessed.jpg"

preprocess_image(INPUT_IMAGE, PREPROCESSED_IMAGE)
print("✅ STEP 2 DONE")

blocks = run_ocr(PREPROCESSED_IMAGE)
print(f"✅ STEP 3 DONE: {len(blocks)} OCR blocks")

rows = group_text_by_rows(blocks)
print(f"✅ STEP 4 DONE: {len(rows)} rows detected")

final_items = []

for row in rows:
    item = parse_row_by_columns(row["items"])
    if is_valid_line_item(item):
        item["description"] = clean_description(item["description"])
        final_items.append(item)

print(f"✅ STEP 6 DONE: {len(final_items)} line items")

output = {
    "invoice_number": "51109338",
    "line_items": final_items
}

with open("final_invoice.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ STEP 7 DONE: JSON saved")
