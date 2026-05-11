"""
Generira raw-format CSV datoteke u raw/ folder na temelju vec obradjenih podataka.
Koristi se kad ne zelimo trositi API pozive, a trebamo raw podatke za Qlik ETL.

Raw format simulira sto bi Alpha Vantage API vratio:
- Originalni nazivi stupaca (fiscalDateEnding, totalRevenue itd.)
- Vrijednosti u punim USD (ne milijuni)
- 'None' stringovi za nedostajuce vrijednosti
- Bez izvedenih metrika (bez EBITDA_Margin, bez lagged featurea)
"""

import os
import pandas as pd

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(OUTPUT_DIR, "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# --- Generiraj raw financijske CSV-ove po tvrtki ---
fin_path = os.path.join(OUTPUT_DIR, "financial_data_2021_2024.csv")
fin_df = pd.read_csv(fin_path)

reverse_col_map = {
    'Date':               'fiscalDateEnding',
    'Revenue':            'totalRevenue',
    'COGS':               'costOfRevenue',
    'Operating_Expenses': 'operatingExpenses',
    'EBITDA':             'ebitda',
    'Net_Income':         'netIncome',
    'Gross_Profit':       'grossProfit',
    'Operating_Income':   'operatingIncome',
    'Company':            'symbol',
}

raw_fin = fin_df[[c for c in reverse_col_map if c in fin_df.columns]].copy()
raw_fin = raw_fin.rename(columns=reverse_col_map)

# Vrati u pune USD (obrnuto od /1_000_000)
money_cols = ['totalRevenue', 'costOfRevenue', 'operatingExpenses', 'ebitda',
              'netIncome', 'grossProfit', 'operatingIncome']
for col in money_cols:
    if col in raw_fin.columns:
        raw_fin[col] = (raw_fin[col] * 1_000_000).round(0).astype('Int64').astype(str)
        raw_fin[col] = raw_fin[col].replace('<NA>', 'None')

for symbol, group in raw_fin.groupby('symbol'):
    out_path = os.path.join(RAW_DIR, f"raw_financial_{symbol}.csv")
    group.to_csv(out_path, index=False)
    print(f"raw_financial_{symbol}.csv  ->  {len(group)} redaka")

# --- Generiraj raw makro CSV (kvartalac, neagregirano simulirano) ---
macro_path = os.path.join(OUTPUT_DIR, "macro_indicators_2021_2024.csv")
macro_df = pd.read_csv(macro_path)

raw_macro_frames = []
for col, indicator in [("GDP", "REAL_GDP"), ("CPI", "CPI"),
                        ("Fed_Rate", "FEDERAL_FUNDS_RATE"), ("Unemployment", "UNEMPLOYMENT")]:
    if col not in macro_df.columns:
        continue
    temp = macro_df[["Date", col]].copy()
    temp = temp.rename(columns={"Date": "date", col: "value"})
    temp["indicator"] = indicator
    temp["interval"] = "quarterly" if col == "GDP" else "monthly"
    temp["value"] = temp["value"].astype(str).replace('nan', 'None')
    raw_macro_frames.append(temp)

if raw_macro_frames:
    raw_macro = pd.concat(raw_macro_frames, ignore_index=True)
    raw_macro.to_csv(os.path.join(RAW_DIR, "raw_macro_monthly.csv"), index=False)
    print(f"raw_macro_monthly.csv        ->  {len(raw_macro)} redaka")

print(f"\nOK - Raw datoteke generirane u: {RAW_DIR}")
print("Sadrzaj raw/ foldera:")
for f in sorted(os.listdir(RAW_DIR)):
    size = os.path.getsize(os.path.join(RAW_DIR, f))
    print(f"  {f}  ({size:,} bytes)")
