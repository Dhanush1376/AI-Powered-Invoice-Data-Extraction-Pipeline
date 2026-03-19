import re

def clean_description(desc):
    desc = desc.lower()

    # remove VAT artifacts
    desc = re.sub(r"\b10%\b", "", desc)
    desc = re.sub(r"\bvat\b", "", desc)

    # remove single stray numbers
    desc = re.sub(r"\b\d\b", "", desc)

    # normalize spaces
    desc = re.sub(r"\s+", " ", desc).strip()

    return desc.title()
