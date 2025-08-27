import pandas as pd
import re
import sys

# regex patterns for PII
EMAIL = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
PHONE = r'\b\d{10}\b'
PAN = r'\b[A-Z]{5}\d{4}[A-Z]\b'
AADHAAR = r'\b\d{12}\b'
NAME = r'[A-Z][a-z]+ [A-Z][a-z]+'   # very simple pattern

def mask(text):
    if pd.isna(text):
        return text
    text = str(text)
    text = re.sub(EMAIL, "xxx@email.com", text)
    text = re.sub(PHONE, "98XXXXX4321", text)
    text = re.sub(PAN, "XXXXX9999X", text)
    text = re.sub(AADHAAR, "XXXXXXXXXXXX", text)
    text = re.sub(NAME, "NAME_REDACTED", text)
    return text

def has_pii(text):
    if pd.isna(text):
        return False
    text = str(text)
    if re.search(EMAIL, text) or re.search(PHONE, text) or re.search(PAN, text) or re.search(AADHAAR, text) or re.search(NAME, text):
        return True
    return False

def main(file):
    df = pd.read_csv(file)

    df["is_pii"] = df.apply(lambda row: any(has_pii(row[col]) for col in df.columns), axis=1)

    for c in df.columns:
        df[c] = df[c].apply(mask)

    out = "redacted_output_" + file
    df.to_csv(out, index=False)
    print("file saved as", out)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("run as: python3 detector_full_candidate_name.py iscp_pii_dataset.csv")
    else:
        main(sys.argv[1])

