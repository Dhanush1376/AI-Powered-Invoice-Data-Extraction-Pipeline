import re

def normalize_number(text):
    # European format → standard float
    text = text.replace(".", "").replace(",", ".")
    try:
        return float(text)
    except:
        return None


def extract_line_item(row_items):
    texts = [item["text"].strip() for item in row_items]

    qty = None
    prices = []
    description_parts = []

    for t in texts:
        # Quantity (1–20)
        if qty is None and re.fullmatch(r"\d{1,2}", t):
            qty = int(t)

        # Prices like 209,00 or 37,75
        elif re.search(r"\d+[.,]\d{2}", t):
            num = normalize_number(t)
            if num:
                prices.append(num)

        else:
            description_parts.append(t)

    unit_price = prices[0] if len(prices) >= 1 else None
    total = prices[-1] if len(prices) >= 2 else None

    return {
        "qty": qty,
        "description": " ".join(description_parts),
        "unit_price": unit_price,
        "total": total
    }
