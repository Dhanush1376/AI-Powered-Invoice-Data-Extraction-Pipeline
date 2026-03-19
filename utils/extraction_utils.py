import re

def extract_invoice_number(blocks):
    """
    Search for invoice number patterns.
    Look for keywords like 'Invoice #', 'Inv No', 'Invoice Number'.
    """
    patterns = [
        r"(?i)\binvoice\b\s*(?:#|no|number)?[:\s]*([\w\-/]+)",
        r"(?i)\binv\b\s*[:\s]*([\w\-/]+)",
        r"(?i)\bbill\b\s*no[:\s]*([\w\-/]+)"
    ]
    
    # First pass: look for the keyword and the following word in the same block
    for block in blocks:
        text = block["text"]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
                
    # Second pass: look for keyword in one block, and value in the next (by y-coord similarity)
    # This is more complex, let's start with the simple one first.
    return "Not Found"

def extract_date(blocks):
    """
    Search for date patterns.
    """
    # Common date patterns: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, Month DD, YYYY
    date_patterns = [
        r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        r"\d{4}[/-]\d{1,2}[/-]\d{1,2}",
        r"(?i)(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}"
    ]
    
    for block in blocks:
        text = block["text"]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
    
    return "Not Found"

def extract_total_amount(blocks):
    """
    Search for the grand total.
    Look for keywords like 'Total', 'Grand Total', 'Amount Due'.
    """
    total_keywords = ["total", "grand total", "net amount", "amount due", "total due", "total payable"]
    
    candidates = []
    
    for i, block in enumerate(blocks):
        text = block["text"].lower()
        if any(kw in text for kw in total_keywords):
            # Check if there's a number in the same block
            num_match = re.search(r"(\d+[.,]\d{2})", block["text"])
            if num_match:
                candidates.append((block, num_match.group(1)))
            else:
                # Look at nearby blocks (usually to the right or below)
                # For simplicity, let's look at the next few blocks
                for j in range(i + 1, min(i + 5, len(blocks))):
                    next_block = blocks[j]
                    num_match = re.search(r"(\d+[.,]\d{2})", next_block["text"])
                    if num_match:
                        # Simple heuristic: same y-coord roughly
                        if abs(block["bbox"][1] - next_block["bbox"][1]) < 15:
                            candidates.append((next_block, num_match.group(1)))
                            break
    
    if candidates:
        # Sort by x-coordinate (usually total is on the right) or just take the last one found in the document
        # Often the last "Total" mentioned is the final one.
        # Let's clean the number
        raw_val = candidates[-1][1]
        cleaned_val = raw_val.replace(",", "").replace(".", ".") # Adjust if needed
        try:
            # If it has more than one point, it might be European format
            if raw_val.count(".") > 1 or ("," in raw_val and "." in raw_val):
                 # Handle European format: 1.234,56 -> 1234.56
                 val = raw_val.replace(".", "").replace(",", ".")
            else:
                 val = raw_val.replace(",", "")
            return float(val)
        except:
            return None

    return None
