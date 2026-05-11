# Prikupljanje podataka — dokumentacija

Ovaj dokument opisuje kako su prikupljeni financijski i makroekonomski podaci koji se koriste u završnom radu za treniranje i evaluaciju ML modela predviđanja financijskih pokazatelja.

---

## Cilj

Prikupiti kvartalne financijske podatke za 5 velikih tehnoloških tvrtki i makroekonomske indikatore SAD-a za period **2021–2024**, te ih podijeliti na:
- **Train set**: 2021–2023 (12 kvartala × 5 tvrtki = 60 redaka)
- **Test set**: 2024 (4 kvartala × 5 tvrtki = 20 redaka)

---

## Izvor podataka — Alpha Vantage API

**Zašto Alpha Vantage?**
- Besplatni plan s 25 zahtjeva/dan
- Vraća kvartalne income statemente 20+ godina unazad
- Pokriva i makroekonomske indikatore (GDP, CPI, kamatne stope)
- Pouzdaniji pristup povijesnim podacima od Yahoo Finance

**Registracija i API ključ:**
1. Idi na [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)
2. Unesi email i dobij besplatni API ključ
3. API ključ pohrani u skriptama (varijabla `API_KEY`)

**Ograničenja besplatnog plana:**
- 25 zahtjeva / dan
- 5 zahtjeva / minutu → skripte imaju `time.sleep(12)` između zahtjeva

---

## Tvrtke

| Ticker | Tvrtka         |
|--------|----------------|
| AAPL   | Apple Inc.     |
| MSFT   | Microsoft Corp.|
| GOOGL  | Alphabet Inc.  |
| AMZN   | Amazon.com Inc.|
| META   | Meta Platforms |

Sve tvrtke su iz **tehnološkog sektora** (NASDAQ), što osigurava usporedivost podataka.

---

## Struktura foldera

```
python/
├── data_notebooks/          # Python skripte za prikupljanje i obradu
│   ├── notebook_2021-2025_bussines.py   # Financijski podaci tvrtki
│   ├── notebook_indicators.py           # Makroekonomski indikatori
│   ├── notebook_merge.py                # Spajanje i feature engineering
│   └── notebook_raw_export.py           # Generiranje raw/ datoteka
│
├── raw/                     # Sirovi podaci (ulaz za Qlik ETL)
│   ├── raw_financial_AAPL.csv
│   ├── raw_financial_MSFT.csv
│   ├── raw_financial_GOOGL.csv
│   ├── raw_financial_AMZN.csv
│   ├── raw_financial_META.csv
│   └── raw_macro_monthly.csv
│
└── structured/              # Obrađeni podaci (izlaz Python pipeline-a)
    ├── financial_data_2021_2024.csv   # Sve tvrtke, sve godine
    ├── macro_indicators_2021_2024.csv # Makro indikatori, kvartalno
    ├── merged_dataset.csv             # Master dataset (financijski + makro + featuresi)
    ├── merged_train.csv               # Train set: 2021–2023
    ├── merged_test.csv                # Test set: 2024
    └── test_2024.csv                  # Samo financijski test set
```

---

## Skripte — redosljed pokretanja

### 1. `notebook_2021-2025_bussines.py`
Dohvaća kvartalne **income statemente** za svih 5 tvrtki putem Alpha Vantage `INCOME_STATEMENT` endpointa.

**Što radi:**
- Za svaki ticker šalje API zahtjev → prima `quarterlyReports` array
- Sprema sirove podatke u `raw/raw_financial_TICKER.csv`
- Rename stupaca, konverzija u milijune USD, izračun EBITDA_Margin
- Filtriranje na 2021–2024, train/test split
- Output: `financial_data_2021_2024.csv`

**Trajanje:** ~60 sekundi (5 zahtjeva × 12s pauze)

**Pokreni:**
```bash
python data_notebooks/notebook_2021-2025_bussines.py
```

---

### 2. `notebook_indicators.py`
Dohvaća **makroekonomske indikatore** SAD-a za period 2021–2024.

**Indikatori:**
| Indikator | AV funkcija | Frekvencija | Opis |
|---|---|---|---|
| GDP | `REAL_GDP` | Kvartalno | Realni BDP SAD (bilj. USD) |
| CPI | `CPI` | Mjesečno → kvartalni prosjek | Indeks potrošačkih cijena |
| Fed_Rate | `FEDERAL_FUNDS_RATE` | Mjesečno → kvartalni prosjek | Kamatna stopa Fed-a |
| Unemployment | `UNEMPLOYMENT` | Mjesečno → kvartalni prosjek | Stopa nezaposlenosti (%) |

**Normalizacija datuma:** GDP AV vraća s početkom kvartala (01-01), ostali s krajem (03-31). Skripta normalizira sve na kraj kvartala (`QE`).

**Trajanje:** ~48 sekundi (4 zahtjeva × 12s pauze)

**Pokreni:**
```bash
python data_notebooks/notebook_indicators.py
```

---

### 3. `notebook_merge.py`
Spaja financijske i makro podatke u **master dataset** s engineeriranim featurima.

**Feature engineering:**
- `Revenue_lag1`, `EBITDA_lag1`, `Net_Income_lag1` — vrijednost prethodnog kvartala
- `Revenue_YoY`, `EBITDA_YoY` — godišnji rast u %
- `Target_Revenue`, `Target_EBITDA`, `Target_Net_Income` — ciljna varijabla (sljedeći kvartal)

**Pokreni:**
```bash
python data_notebooks/notebook_merge.py
```

---

### 4. `notebook_raw_export.py`
Generira `raw/` datoteke iz već obrađenih podataka — **bez API poziva**.

Koristi se kad je već pokrenut pipeline, ali trebaju se regenerirati raw datoteke za Qlik ETL bez trošenja dnevnog API limita.

```bash
python data_notebooks/notebook_raw_export.py
```

---

## Output CSV-ovi — pregled

### raw/ folder (ulaz za Qlik ETL)

| Datoteka | Opis | Stupci |
|---|---|---|
| `raw_financial_AAPL.csv` | Sirovi AV podaci za Apple | `fiscalDateEnding`, `totalRevenue`, `costOfRevenue`, `ebitda`, `netIncome`, `grossProfit`, `operatingIncome`, `operatingExpenses`, `symbol` |
| `raw_financial_MSFT.csv` | Sirovi AV podaci za Microsoft | isto |
| `raw_financial_GOOGL.csv` | Sirovi AV podaci za Alphabet | isto |
| `raw_financial_AMZN.csv` | Sirovi AV podaci za Amazon | isto |
| `raw_financial_META.csv` | Sirovi AV podaci za Meta | isto |
| `raw_macro_monthly.csv` | Sirovi makro podaci | `date`, `value`, `indicator`, `interval` |

**Napomena:** vrijednosti su u punim USD (npr. `89584000000`), nedostajuće vrijednosti su `None` stringovi.

### structured/ folder (izlaz Python pipeline-a)

| Datoteka | Redaka | Opis |
|---|---|---|
| `financial_data_2021_2024.csv` | 80 | Obrađeni financijski podaci, sve tvrtke, 2021–2024 |
| `macro_indicators_2021_2024.csv` | 16 | Kvartalni makro indikatori, 2021–2024 |
| `merged_dataset.csv` | 80 | Master dataset: financijski + makro + featuresi + targeti |
| `merged_train.csv` | 60 | Train set (2021–2023), spreman za ML |
| `merged_test.csv` | 20 | Test set (2024), za evaluaciju modela |

---

## Napomene

- **API ključ** (`BKBLC8V2JHN86B0D`) je besplatni ključ s limitom 25 zahtjeva/dan. Ako je limit iscrpljen, pričekaj do ponoći (UTC) za reset.
- Skripte 1 i 2 uvijek treba pokrenuti **prije** skripte 3.
- Skripta 4 (`notebook_raw_export.py`) može se pokrenuti u bilo kojem trenutku bez API poziva.
- Vrijednosti su u **milijunima USD** u svim `structured/` datotekama.
