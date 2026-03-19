def group_text_by_rows(blocks, y_threshold=12):
    rows = []

    for block in sorted(blocks, key=lambda x: x["bbox"][1]):
        placed = False
        for row in rows:
            if abs(row["y"] - block["bbox"][1]) <= y_threshold:
                row["items"].append(block)
                placed = True
                break
        if not placed:
            rows.append({
                "y": block["bbox"][1],
                "items": [block]
            })
    return rows


def parse_row_by_columns(row_items):
    qty = None
    description = []
    unit_price = None
    total = None

    for item in row_items:
        if "bbox" not in item or not item["bbox"]:
            continue

        x1 = item["bbox"][0]
        text = item["text"].strip()

        if not text:
            continue

        # DESCRIPTION
        if 140 <= x1 <= 650:
            description.append(text)

        # QTY
        elif 400 <= x1 <= 480:
            try:
                qty = int(text.replace(",", "").split(".")[0])
            except:
                pass

        # UNIT PRICE
        elif 740 <= x1 <= 880:
            try:
                unit_price = float(text.replace(".", "").replace(",", "."))
            except:
                pass

        # TOTAL
        elif x1 >= 1000:
            try:
                total = float(text.replace(".", "").replace(",", "."))
            except:
                pass

    return {
        "qty": qty,
        "description": " ".join(description),
        "unit_price": unit_price,
        "total": total
    }
