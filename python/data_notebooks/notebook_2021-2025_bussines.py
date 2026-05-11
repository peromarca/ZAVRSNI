import os
import time
import requests
import pandas as pd

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(OUTPUT_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# --- Konfiguracija ---
API_KEY = "BKBLC8V2JHN86B0D"
BASE_URL = "https://www.alphavantage.co/query"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
TRAIN_END = "2023-12-31"
TEST_START = "2024-01-01"
TEST_END = "2024-12-31"

# --- Dohvati kvartalne income statemente za svaki ticker ---
all_data = []

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

    df = pd.DataFrame(data["quarterlyReports"])

    # --- Spremi sirove podatke (za Qlik ETL) ---
    df['symbol'] = symbol
    raw_path = os.path.join(RAW_DIR, f"raw_financial_{symbol}.csv")
    df.to_csv(raw_path, index=False)

    col_map = {
        'fiscalDateEnding':  'Date',
        'totalRevenue':      'Revenue',
        'costOfRevenue':     'COGS',
        'operatingExpenses': 'Operating_Expenses',
        'ebitda':            'EBITDA',
        'netIncome':         'Net_Income',
        'grossProfit':       'Gross_Profit',
        'operatingIncome':   'Operating_Income',
    }
    available = {k: v for k, v in col_map.items() if k in df.columns}
    df = df[list(available.keys())].rename(columns=available)
    df['Company'] = symbol

    all_data.append(df)
    print(f"OK ({len(df)} kvartala)")

    # Alpha Vantage limit: 5 req/min na free planu
    if i < len(TICKERS) - 1:
        time.sleep(12)

# --- Spoji sve ---
if not all_data:
    raise RuntimeError("Nema podataka ni za jedan ticker.")

final_df = pd.concat(all_data, ignore_index=True)
final_df['Date'] = pd.to_datetime(final_df['Date'])

for col in ['Revenue', 'COGS', 'Operating_Expenses', 'EBITDA', 'Net_Income', 'Gross_Profit', 'Operating_Income']:
    if col in final_df.columns:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce')

# --- Filtriraj 2021-2024 ---
final_df = final_df[(final_df['Date'] >= '2021-01-01') & (final_df['Date'] <= TEST_END)]
final_df = final_df.sort_values(['Date', 'Company']).reset_index(drop=True)

if final_df.empty:
    raise RuntimeError("Nema podataka za 2021-2024. Provjeri API kljuc i tickere.")

# --- Konvertiraj u milijune USD ---
money_cols = [c for c in ['Revenue', 'COGS', 'Operating_Expenses', 'EBITDA', 'Net_Income', 'Gross_Profit', 'Operating_Income'] if c in final_df.columns]
for col in money_cols:
    final_df[col] = (final_df[col] / 1_000_000).round(2)

# --- Izracunaj EBITDA marginu ---
safe_rev = final_df['Revenue'].where(final_df['Revenue'] != 0)
final_df['EBITDA_Margin'] = (final_df['EBITDA'] / safe_rev * 100).round(2)
final_df['Currency_Unit'] = 'millions USD'

# --- Train/test split ---
train_df = final_df[final_df['Date'] <= TRAIN_END]
test_df  = final_df[(final_df['Date'] >= TEST_START) & (final_df['Date'] <= TEST_END)]

# --- Spremi CSV-ove ---
final_df.to_csv(os.path.join(OUTPUT_DIR, 'financial_data_2021_2024.csv'), index=False)
train_df.to_csv(os.path.join(OUTPUT_DIR, 'train_2021_2023.csv'), index=False)
test_df.to_csv(os.path.join(OUTPUT_DIR, 'test_2024.csv'), index=False)

# --- Ispis ---
print(f"\nOK - Ukupno redaka: {len(final_df)}")
print(f"   Train (2021-2023): {len(train_df)} redaka")
print(f"   Test  (2024):      {len(test_df)} redaka")
print(f"   Date range:        {final_df['Date'].min().date()} - {final_df['Date'].max().date()}")
print(f"   Tvrtke:            {', '.join(final_df['Company'].unique())}")
print(f"\n{final_df[['Date','Company','Revenue','EBITDA','EBITDA_Margin']].head(10).to_string()}")