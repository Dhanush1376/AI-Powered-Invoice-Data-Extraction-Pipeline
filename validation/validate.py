def is_valid_line_item(item):
    return (
        item["description"]
        and item["qty"] is not None
        and (item["unit_price"] is not None or item["total"] is not None)
    )
