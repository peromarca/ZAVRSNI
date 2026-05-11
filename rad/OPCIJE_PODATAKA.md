# Opcije za podatke — Poglavlje 5 i 6

> **Plan:** Train set 2021–2023 (75%), Test set 2024 (25%)
>
> ⚠️ Napomena: Yahoo Finance nema kompletne podatke za 2025. (tvrtke objavljuju kvartale s kašnjenjem), pa je test set pomaknut na 2024.

---

## **3 OPCIJE ZA PODATKE**

### **OPCIJA 1: Yahoo Finance API** ⭐ PREPORUČENO

**Što je:** Besplatni API za financijske podatke javnih tvrtki (S&P 500, NASDAQ...)

**Što sadrži:**
- Kvartalni Income Statement (Revenue, COGS, OPEX, EBITDA, Net Income)
- Period: 2021–2024 (Q1 2021 do Q4 2024, kompletni podatci)
- Format: CSV/JSON putem Python biblioteke `yfinance`

**Kako preuzeti:**
```bash
pip install yfinance pandas
```

```python
import yfinance as yf
import pandas as pd

# Odaberi 3-5 tvrtki iz iste industrije
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
all_data = []

for symbol in tickers:
    ticker = yf.Ticker(symbol)
    income = ticker.quarterly_income_stmt.T  # Transponuj
    
    df = pd.DataFrame({
        'Date': income.index,
        'Company': symbol,
        'Revenue': income.get('Total Revenue', 0),
        'COGS': income.get('Cost Of Revenue', 0),
        'Operating_Expenses': income.get('Operating Expense', 0),
        'EBITDA': income.get('EBITDA', 0),
        'Net_Income': income.get('Net Income', 0)
    })
    all_data.append(df)

# Kombiniraj sve
final_df = pd.concat(all_data, ignore_index=True)
final_df['Date'] = pd.to_datetime(final_df['Date'])
final_df = final_df[(final_df['Date'] >= '2021-01-01') & (final_df['Date'] <= '2024-12-31')]
final_df = final_df.sort_values('Date')

# Spremi
final_df.to_csv('financial_data_2021_2024.csv', index=False)
print(f"✅ Dataset spremljen: {len(final_df)} redaka")
```

**Train/Test split:**
- Train: 2021 Q1 – 2023 Q4 (12 kvartala × 5 tvrtki = **60 redaka**)
- Test: 2024 Q1–Q4 (4 kvartala × 5 tvrtki = **20 redaka**)
- Omjer: **75% / 25%**

**Prednosti:**
- ✅ Besplatno, bez API ključa
- ✅ Stvarni podatci
- ✅ Standardizirani financijski pokazatelji
- ✅ Lako integrirati u Qlik i Python

**Mane:**
- ❌ Kvartalni (ne mjesečni), ali to je OK za ML
- ❌ Samo javne tvrtke

---

### **OPCIJA 2: Mock podatci** (backup)

**Što je:** Tvoja postojeća `generate_mock_data.py` skripta

**Što sadrži:**
- Mjesečni P&L podatci 2021–2024 (48 mjeseci)
- Simulirani trend + sezonalnost + šum

**Kako koristiti:**
```bash
cd c:\Users\petar\Desktop\ZAVRŠNI\rad\mock_data
python generate_mock_data.py
```

Output: `mock_financials.csv`

**Train/Test split:**
- Train: 2021-01 do 2023-12 (36 mjeseci)
- Test: 2024-01 do 2024-12 (12 mjeseci)

**Prednosti:**
- ✅ Mjesečna granularnost
- ✅ Potpuna kontrola
- ✅ Već spremno

**Mane:**
- ❌ Sintetički podatci (mentor može pitati zašto ne koristiš stvarne)

---

### **OPCIJA 3: Podatci iz firme** (idealno, ali čeka)

**Što bi trebalo:**
- Anonimizirani mjesečni P&L klijenta (2021–2024)
- Prihodi po segmentima, troškovi, EBITDA

**Prednosti:**
- ✅ Stvarni podatci
- ✅ Najjači argument za rad

**Mane:**
- ❌ Čeka odobrenje i pristup

---

## **MOJA PREPORUKA**

### **SADA (sljedećih tjedan dana):**
1. Pokreni **Yahoo Finance skriptu** (OPCIJA 1)
2. Učitaj podatke u Qlik Sense (ETL)
3. Testiraj Qlik Predict
4. Implementiraj Python modele (ARIMA, XGBoost, LSTM)
5. Generiraj prve rezultate

### **KASNIJE (za finalni rad):**
- Ako dobiješ pristup podatcima iz firme → zamijeni dataset, pipeline ostaje isti

---

## **ŠTO DATASET MORA IMATI**

### Minimalne kolone:

| Kolona | Tip | Opis |
|---|---|---|
| `Date` | Date | Datum izvještaja |
| `Revenue` | Float | Ukupni prihodi |
| `COGS` | Float | Cost of Goods Sold |
| `Operating_Expenses` | Float | OPEX |
| `EBITDA` | Float | Operativna dobit |
| `Net_Income` | Float | Neto dobit |

### Opcionalno (za bolje modele):
- `Company` ili `Segment` (ako kombiniraš više tvrtki)
- Makroekonomski indikatori (GDP, inflacija, kamatne stope)

---

## **SLJEDEĆI KORACI**

1. **Odluči:** Yahoo Finance ili čekaj podatke iz firme?
2. **Preuzmi dataset** (pokreni skriptu iznad)
3. **Učitaj u Qlik Sense** (ETL load script)
4. **Pokreni Qlik Predict** (no-code predviđanje)
5. **Implementiraj Python modele** (ARIMA, XGBoost, LSTM)
6. **Usporedi rezultate** (MAE, RMSE, MAPE)

---

## **DODATAK: Skripta za preuzimanje Yahoo Finance podataka**

Spremi kao `download_yahoo_finance.py`:

```python
import yfinance as yf
import pandas as pd
from datetime import datetime

# Konfiguracija
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
start_date = "2021-01-01"
end_date = "2024-12-31"
train_cutoff = "2023-12-31"  # Sve do kraja 2023 = train
test_start = "2024-01-01"   # 2024 = test

print("🔄 Preuzimanje podataka s Yahoo Finance...")

all_data = []

for symbol in tickers:
    print(f"   Preuzimam {symbol}...")
    try:
        ticker = yf.Ticker(symbol)
        income = ticker.quarterly_income_stmt.T
        
        df = pd.DataFrame({
            'Date': income.index,
            'Company': symbol,
            'Revenue': income.get('Total Revenue', 0),
            'COGS': income.get('Cost Of Revenue', 0),
            'Operating_Expenses': income.get('Operating Expense', 0),
            'EBITDA': income.get('EBITDA', 0),
            'Net_Income': income.get('Net Income', 0)
        })
        all_data.append(df)
    except Exception as e:
        print(f"   ❌ Greška za {symbol}: {e}")

# Kombiniraj sve
final_df = pd.concat(all_data, ignore_index=True)
final_df['Date'] = pd.to_datetime(final_df['Date'])
final_df = final_df[(final_df['Date'] >= start_date) & (final_df['Date'] <= end_date)]
final_df = final_df.sort_values('Date')

# Izračunaj dodatne pokazatelje
final_df['Gross_Profit'] = final_df['Revenue'] - final_df['COGS']
final_df['EBITDA_Margin'] = (final_df['EBITDA'] / final_df['Revenue'] * 100).round(2)

# Spremi kompletan dataset
output_file = 'financial_data_2021_2024.csv'
final_df.to_csv(output_file, index=False)

# Spremi i zasebne train/test CSV-ove
train_df = final_df[final_df['Date'] <= train_cutoff]
test_df  = final_df[final_df['Date'] >= test_start]
train_df.to_csv('train_2021_2023.csv', index=False)
test_df.to_csv('test_2024.csv', index=False)

print(f"\n✅ Dataset spremljen: {output_file}")
print(f"   Ukupno redaka: {len(final_df)}")
print(f"   Train (2021–2023): {len(train_df)} redaka")
print(f"   Test  (2024):      {len(test_df)} redaka")
print(f"   Tvrtke: {', '.join(final_df['Company'].unique())}")
print(f"\n📊 Pregled prvih 5 redaka:")
print(final_df.head())
```

Pokreni s:
```bash
python download_yahoo_finance.py
```

Outputi:
- `financial_data_2021_2024.csv` — kompletan dataset
- `train_2021_2023.csv` — za treniranje modela
- `test_2024.csv` — za evaluaciju modela

---

## **ZAŠTO NE 2025?**

Yahoo Finance sadrži samo objavljene kvartalne izvještaje. Tvrtke objavljuju financijske rezultate s kašnjenjem:

| Kvartal | Period | Objavljuje se |
|---|---|---|
| Q1 2025 | sij–ožu 2025 | travanj/svibanj 2025 |
| Q2 2025 | tra–lip 2025 | srpanj/kolovoz 2025 |
| Q3 2025 | srp–ruj 2025 | listopad/studeni 2025 |
| Q4 2025 | lis–pro 2025 | siječanj/veljača 2026 |

U svibnju 2026. **Q4 2025 bi trebao biti dostupan**, ali pouzdanost podataka za sve tvrtke varira. Pomak na **2024 kao test set** eliminira ovaj problem i daje čišću evaluaciju.
