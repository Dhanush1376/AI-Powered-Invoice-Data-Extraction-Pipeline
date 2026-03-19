import re

def clean_description(text):
    text = re.sub(r"\b\d+%?\b", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
