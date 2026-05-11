"""
Dohvaca sirove kvartalne income statemente iz Alpha Vantage API-ja
i sprema ih u raw/ folder BEZ IKAKVE OBRADE.

Sirovi podaci sadrze:
- SVE kvartale koje AV vrati (~80+), ne samo 2021-2024
- Originalne AV nazive stupaca (fiscalDateEnding, totalRevenue, itd.)
- Pune USD iznose kao stringove (npr. '89584000000')
- 'None' stringove za nedostajuce vrijednosti
- Bez rename, konverzije, filtriranja
"""

import os
import time
import json
import requests
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "..", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# --- Konfiguracija ---
API_KEY = "BKBLC8V2JHN86B0D"
BASE_URL = "https://www.alphavantage.co/query"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]

for i, symbol in enumerate(TICKERS):
    url = f"{BASE_URL}?function=INCOME_STATEMENT&symbol={symbol}&apikey={API_KEY}"
    print(f"Preuzimam {symbol}...", end=" ")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"GRESKA ({e})")
        continue

    if "quarterlyReports" not in data or not data["quarterlyReports"]:
        print(f"nema podataka ({data.get('Note', data.get('Information', 'nepoznato'))})")
        continue

    reports = data["quarterlyReports"]

    # Spremi sirovi JSON response (za referencu)
    json_path = os.path.join(RAW_DIR, f"raw_financial_{symbol}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    # Spremi kao CSV — tocno onako kako AV vraca, bez transformacija
    df = pd.DataFrame(reports)
    csv_path = os.path.join(RAW_DIR, f"raw_financial_{symbol}.csv")
    df.to_csv(csv_path, index=False)

    print(f"OK ({len(df)} kvartala, {len(df.columns)} stupaca)")
    print(f"   Stupci: {list(df.columns)[:8]}...")

    # Alpha Vantage limit: 5 req/min
    if i < len(TICKERS) - 1:
        time.sleep(12)

print(f"\nOK - Sirovi financijski podaci spremljeni u: {RAW_DIR}")
print("Datoteke:")
for f in sorted(os.listdir(RAW_DIR)):
    if f.startswith("raw_financial_"):
        size = os.path.getsize(os.path.join(RAW_DIR, f))
        print(f"  {f}  ({size:,} bytes)")
