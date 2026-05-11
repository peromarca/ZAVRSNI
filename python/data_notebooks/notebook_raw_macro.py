"""
Dohvaca sirove makroekonomske indikatore iz Alpha Vantage API-ja
i sprema ih u raw/ folder BEZ IKAKVE OBRADE.

Sirovi podaci sadrze:
- SVE dostupne datume (ne samo 2021-2024), stotine redaka
- Mjesecne podatke za CPI, Fed_Rate, Unemployment (neagregirane)
- GDP s originalnim datumima pocetka kvartala (01-01, 04-01, 07-01, 10-01)
- Sve u jednom CSV-u s kolonama: date, value, indicator, interval
- Bez agregacije, normalizacije datuma, filtriranja
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

indicators = {
    "REAL_GDP":           {"interval": "quarterly"},
    "CPI":                {"interval": "monthly"},
    "FEDERAL_FUNDS_RATE": {"interval": "monthly"},
    "UNEMPLOYMENT":       {"interval": "monthly"},
}

all_frames = []

for i, (func_name, cfg) in enumerate(indicators.items()):
    interval = cfg["interval"]
    url = f"{BASE_URL}?function={func_name}&interval={interval}&apikey={API_KEY}"
    print(f"Preuzimam {func_name} ({interval})...", end=" ")

    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"GRESKA ({e})")
        continue

    if "data" not in data:
        print(f"nema podataka ({data.get('Note', data.get('Information', 'nepoznato'))})")
        continue

    records = data["data"]

    # Spremi sirovi JSON response po indikatoru (za referencu)
    json_path = os.path.join(RAW_DIR, f"raw_macro_{func_name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

    # Dodaj u kumulativni DataFrame — bez ikakve transformacije
    df = pd.DataFrame(records)  # kolone: date, value (oboje stringovi)
    df["indicator"] = func_name
    df["interval"] = interval
    all_frames.append(df)

    print(f"OK ({len(df)} zapisa)")

    # Alpha Vantage limit: 5 req/min
    if i < len(indicators) - 1:
        time.sleep(12)

# --- Spoji sve u jedan CSV ---
if not all_frames:
    raise RuntimeError("Nema makro podataka. Provjeri API kljuc.")

raw_macro = pd.concat(all_frames, ignore_index=True)
csv_path = os.path.join(RAW_DIR, "raw_macro_all.csv")
raw_macro.to_csv(csv_path, index=False)

print(f"\nOK - Sirovi makro podaci spremljeni u: {csv_path}")
print(f"   Ukupno redaka: {len(raw_macro)}")
print(f"   Po indikatoru:")
for name, group in raw_macro.groupby("indicator"):
    print(f"     {name}: {len(group)} zapisa, raspon: {group['date'].min()} - {group['date'].max()}")

print(f"\nPrvih 5 redaka po indikatoru:")
for name in indicators:
    subset = raw_macro[raw_macro["indicator"] == name].head(5)
    print(f"\n  --- {name} ---")
    print(f"  {subset.to_string(index=False)}")
