import os
import time
import requests
import pandas as pd

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(OUTPUT_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

raw_monthly_frames = []

# --- Konfiguracija ---
API_KEY = "BKBLC8V2JHN86B0D"
BASE_URL = "https://www.alphavantage.co/query"
DATE_START = "2021-01-01"
DATE_END = "2024-12-31"

# --- Makro indikatori ---
indicators = {
    "REAL_GDP":           {"interval": "quarterly", "col": "GDP"},
    "CPI":                {"interval": "monthly",   "col": "CPI"},
    "FEDERAL_FUNDS_RATE": {"interval": "monthly",   "col": "Fed_Rate"},
    "UNEMPLOYMENT":       {"interval": "monthly",   "col": "Unemployment"},
}

all_series = {}

for func_name, cfg in indicators.items():
    interval = cfg["interval"]
    col_name = cfg["col"]
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

    df = pd.DataFrame(data["data"])

    # --- Spremi sirove podatke (za Qlik ETL) ---
    df_raw = df.copy()
    df_raw["indicator"] = func_name
    df_raw["interval"] = interval
    raw_monthly_frames.append(df_raw)

    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    df = df[(df["date"] >= DATE_START) & (df["date"] <= DATE_END)]
    df = df.sort_values("date")

    if interval == "monthly":
        # Agregiraj mjesecne podatke na kvartale (prosjek)
        df = df.set_index("date").resample("QE").mean().reset_index()
    elif interval == "quarterly":
        # GDP dolazi s pocetkom kvartala (01-01, 04-01...) — normalizirati na kraj kvartala
        df = df.set_index("date").resample("QE").last().reset_index()

    df = df.rename(columns={"date": "Date", "value": col_name})
    all_series[col_name] = df[["Date", col_name]]
    print(f"OK ({len(df)} zapisa)")

    time.sleep(12)  # rate limit: 5 req/min

# --- Spremi raw makro CSV ---
if raw_monthly_frames:
    raw_macro = pd.concat(raw_monthly_frames, ignore_index=True)
    raw_macro.to_csv(os.path.join(RAW_DIR, "raw_macro_monthly.csv"), index=False)
    print(f"Raw makro spremen: {len(raw_macro)} redaka")

# --- Spoji sve indikatore po datumu ---
if not all_series:
    raise RuntimeError("Nema makro podataka. Provjeri API kljuc.")

merged = None
for col_name, df in all_series.items():
    if merged is None:
        merged = df
    else:
        merged = pd.merge(merged, df, on="Date", how="outer")

merged = merged.sort_values("Date").reset_index(drop=True)

# --- Spremi ---
out_path = os.path.join(OUTPUT_DIR, "macro_indicators_2021_2024.csv")
merged.to_csv(out_path, index=False)

print(f"\nOK - Makro indikatori spremljeni")
print(f"   Redaka:     {len(merged)}")
print(f"   Stupci:     {list(merged.columns)}")
print(f"   Date range: {merged['Date'].min().date()} - {merged['Date'].max().date()}")
print(f"\n{merged.to_string()}")
