import os
import pandas as pd

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Ucitaj financijske podatke ---
fin_path = os.path.join(OUTPUT_DIR, "financial_data_2021_2024.csv")
fin_df = pd.read_csv(fin_path)
fin_df["Date"] = pd.to_datetime(fin_df["Date"])
print(f"Financijski podatci: {len(fin_df)} redaka, {fin_df['Company'].nunique()} tvrtki")

# --- Ucitaj makro indikatore ---
macro_path = os.path.join(OUTPUT_DIR, "macro_indicators_2021_2024.csv")
macro_df = pd.read_csv(macro_path)
macro_df["Date"] = pd.to_datetime(macro_df["Date"])
print(f"Makro indikatori:    {len(macro_df)} redaka, stupci: {list(macro_df.columns)}")

# --- Normalizacija datuma na kraj kvartala ---
# Financijski podatci mogu imati razlicite datume unutar kvartala
fin_df["Date"] = fin_df["Date"] + pd.offsets.QuarterEnd(0)
macro_df["Date"] = macro_df["Date"] + pd.offsets.QuarterEnd(0)

# --- Merge ---
master = pd.merge(fin_df, macro_df, on="Date", how="left")
print(f"Nakon merge-a:       {len(master)} redaka")

# --- Sortiraj po tvrtki i datumu za lagged feature engineering ---
master = master.sort_values(["Company", "Date"]).reset_index(drop=True)

# --- Lagged features (prethodni kvartal, po tvrtki) ---
for col in ["Revenue", "EBITDA", "Net_Income", "Operating_Income"]:
    if col in master.columns:
        master[f"{col}_lag1"] = master.groupby("Company")[col].shift(1)

# --- YoY rast (isti kvartal prosle godine = shift(4)) ---
for col in ["Revenue", "EBITDA"]:
    if col in master.columns:
        prev_year = master.groupby("Company")[col].shift(4)
        master[f"{col}_YoY"] = ((master[col] - prev_year) / prev_year.abs() * 100).round(2)

# --- Target varijable (sljedeci kvartal = shift(-1), po tvrtki) ---
for col in ["Revenue", "EBITDA", "Net_Income"]:
    if col in master.columns:
        master[f"Target_{col}"] = master.groupby("Company")[col].shift(-1)

# --- Ukloni Currency_Unit kolonu (nije numericki feature) ---
if "Currency_Unit" in master.columns:
    master = master.drop(columns=["Currency_Unit"])

# --- Finalni sort po datumu ---
master = master.sort_values(["Date", "Company"]).reset_index(drop=True)

# --- Train/test split ---
train = master[master["Date"] <= "2023-12-31"].copy()
test  = master[(master["Date"] >= "2024-01-01") & (master["Date"] <= "2024-12-31")].copy()

# --- Spremi ---
master.to_csv(os.path.join(OUTPUT_DIR, "master_dataset.csv"), index=False)
train.to_csv(os.path.join(OUTPUT_DIR, "master_train.csv"), index=False)
test.to_csv(os.path.join(OUTPUT_DIR, "master_test.csv"), index=False)

# --- Validacija ---
print(f"\nOK - Master dataset spreman")
print(f"   Ukupno redaka:  {len(master)}")
print(f"   Train redaka:   {len(train)}")
print(f"   Test redaka:    {len(test)}")
print(f"   Stupci ({len(master.columns)}): {list(master.columns)}")

missing_train = train[["Target_Revenue", "Target_EBITDA", "Target_Net_Income"]].isna().sum()
print(f"\nNaN u train targetima:\n{missing_train}")

missing_features = test[["Revenue_lag1", "GDP", "CPI", "Fed_Rate"]].isna().sum()
print(f"\nNaN u test featurima:\n{missing_features}")

print(f"\nPreview (prve 3 kolone x 5 redaka):")
preview_cols = ["Date", "Company", "Revenue", "EBITDA", "GDP", "CPI", "Fed_Rate",
                "Revenue_lag1", "EBITDA_YoY", "Target_Revenue", "Target_EBITDA"]
available_preview = [c for c in preview_cols if c in master.columns]
print(master[available_preview].head(10).to_string())
