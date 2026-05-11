# Qlik Sense ETL — čišćenje i priprema podataka za ML

Ovaj dokument opisuje korake čišćenja i transformacije sirovih podataka iz `raw/` foldera unutar Qlik Sense-a, kao dio ETL (Extract, Transform, Load) procesa u završnom radu.

---

## Cilj ETL procesa

Učitati sirove CSV datoteke iz `raw/` foldera, provesti čišćenje i transformaciju, te dobiti čist dataset ekvivalentan `structured/merged_dataset.csv` koji Python ML modeli koriste za treniranje.

```
raw/raw_financial_*.csv  ─┐
                           ├─► Qlik ETL ─► čist joined dataset ─► ML modeli
raw/raw_macro_all.csv     ─┘
```

---

## Ulazne datoteke

| Datoteka | Problemi koje treba riješiti |
|---|---|
| `raw_financial_AAPL.csv` (i ostala 4) | `None` stringovi, puni USD, originalni AV nazivi stupaca, ~83 kvartala (treba filtrirati na 2021-2024) |
| `raw_macro_all.csv` | Svi indikatori u jednoj koloni `value`, treba pivot, GDP datumi su početak kvartala (01-01), CPI/Fed/Unemployment su mjesečni |

---

## Korak 1 — Load i spajanje financijskih datoteka

Učitaj svih 5 financijskih CSV-ova i spoji ih u jednu tablicu (CONCATENATE). AV ne vraća ticker u odgovoru pa ga dodajemo kao literal. Odmah filtriramo na 2021-2024 da reduciramo podatke s ~83 na 16 kvartala po tvrtki.

```qlik
FinancialRaw:
LOAD
    fiscalDateEnding    AS Date,
    'AAPL'              AS Company,
    totalRevenue        AS Revenue_raw,
    costOfRevenue       AS COGS_raw,
    operatingExpenses   AS Operating_Expenses_raw,
    ebitda              AS EBITDA_raw,
    netIncome           AS Net_Income_raw,
    grossProfit         AS Gross_Profit_raw,
    operatingIncome     AS Operating_Income_raw
FROM [raw/raw_financial_AAPL.csv] (txt, utf8, embedded labels, delimiter is ',')
WHERE fiscalDateEnding >= '2021-01-01' AND fiscalDateEnding <= '2024-12-31';

CONCATENATE (FinancialRaw)
LOAD fiscalDateEnding AS Date, 'MSFT' AS Company,
     totalRevenue AS Revenue_raw, costOfRevenue AS COGS_raw,
     operatingExpenses AS Operating_Expenses_raw, ebitda AS EBITDA_raw,
     netIncome AS Net_Income_raw, grossProfit AS Gross_Profit_raw,
     operatingIncome AS Operating_Income_raw
FROM [raw/raw_financial_MSFT.csv] (txt, utf8, embedded labels, delimiter is ',')
WHERE fiscalDateEnding >= '2021-01-01' AND fiscalDateEnding <= '2024-12-31';

CONCATENATE (FinancialRaw)
LOAD fiscalDateEnding AS Date, 'GOOGL' AS Company,
     totalRevenue AS Revenue_raw, costOfRevenue AS COGS_raw,
     operatingExpenses AS Operating_Expenses_raw, ebitda AS EBITDA_raw,
     netIncome AS Net_Income_raw, grossProfit AS Gross_Profit_raw,
     operatingIncome AS Operating_Income_raw
FROM [raw/raw_financial_GOOGL.csv] (txt, utf8, embedded labels, delimiter is ',')
WHERE fiscalDateEnding >= '2021-01-01' AND fiscalDateEnding <= '2024-12-31';

CONCATENATE (FinancialRaw)
LOAD fiscalDateEnding AS Date, 'AMZN' AS Company,
     totalRevenue AS Revenue_raw, costOfRevenue AS COGS_raw,
     operatingExpenses AS Operating_Expenses_raw, ebitda AS EBITDA_raw,
     netIncome AS Net_Income_raw, grossProfit AS Gross_Profit_raw,
     operatingIncome AS Operating_Income_raw
FROM [raw/raw_financial_AMZN.csv] (txt, utf8, embedded labels, delimiter is ',')
WHERE fiscalDateEnding >= '2021-01-01' AND fiscalDateEnding <= '2024-12-31';

CONCATENATE (FinancialRaw)
LOAD fiscalDateEnding AS Date, 'META' AS Company,
     totalRevenue AS Revenue_raw, costOfRevenue AS COGS_raw,
     operatingExpenses AS Operating_Expenses_raw, ebitda AS EBITDA_raw,
     netIncome AS Net_Income_raw, grossProfit AS Gross_Profit_raw,
     operatingIncome AS Operating_Income_raw
FROM [raw/raw_financial_META.csv] (txt, utf8, embedded labels, delimiter is ',')
WHERE fiscalDateEnding >= '2021-01-01' AND fiscalDateEnding <= '2024-12-31';
```

---

## Korak 2 — Čišćenje financijskih podataka

Zamjena `None` stringova s `NULL`, type casting u numeričke vrijednosti.

```qlik
FinancialClean:
LOAD
    Date(Date#(Date, 'YYYY-MM-DD'), 'YYYY-MM-DD') AS Date,
    Company,
    IF(Revenue_raw = 'None', NULL(), Num(Revenue_raw))         AS Revenue_full,
    IF(COGS_raw = 'None', NULL(), Num(COGS_raw))               AS COGS_full,
    IF(Operating_Expenses_raw = 'None', NULL(), Num(Operating_Expenses_raw)) AS OpEx_full,
    IF(EBITDA_raw = 'None', NULL(), Num(EBITDA_raw))           AS EBITDA_full,
    IF(Net_Income_raw = 'None', NULL(), Num(Net_Income_raw))   AS Net_Income_full,
    IF(Gross_Profit_raw = 'None', NULL(), Num(Gross_Profit_raw)) AS Gross_Profit_full,
    IF(Operating_Income_raw = 'None', NULL(), Num(Operating_Income_raw)) AS Operating_Income_full
RESIDENT FinancialRaw;

DROP TABLE FinancialRaw;
```

---

## Korak 3 — Konverzija jedinica (puni USD → milijuni USD)

Alpha Vantage vraća vrijednosti u punim dolarima (npr. `89584000000`). Dijeli s 1.000.000.

```qlik
FinancialMillions:
LOAD
    Date,
    Company,
    Round(Revenue_full / 1000000, 0.01)         AS Revenue,
    Round(COGS_full / 1000000, 0.01)             AS COGS,
    Round(OpEx_full / 1000000, 0.01)             AS Operating_Expenses,
    Round(EBITDA_full / 1000000, 0.01)           AS EBITDA,
    Round(Net_Income_full / 1000000, 0.01)       AS Net_Income,
    Round(Gross_Profit_full / 1000000, 0.01)     AS Gross_Profit,
    Round(Operating_Income_full / 1000000, 0.01) AS Operating_Income
RESIDENT FinancialClean;

DROP TABLE FinancialClean;
```

---

## Korak 4 — Load makro podataka i pivot

`raw_macro_all.csv` ima sve indikatore u jednoj koloni `value`, razlikovani po `indicator` koloni. GDP ima datume početka kvartala (01-01), CPI/Fed/Unemployment su mjesečni — sve treba razdvojiti u zasebne stupce i normalizirati na kraj kvartala.

```qlik
// Učitaj svaki indikator zasebno i agregiraj na kvartale
GDP_raw:
LOAD
    Date(MonthEnd(Date(date, 'YYYY-MM-DD'), 2), 'YYYY-MM-DD') AS QuarterEnd,
    Num(value) AS GDP
FROM [raw/raw_macro_all.csv]
WHERE indicator = 'REAL_GDP' AND date >= '2021-01-01' AND date <= '2024-12-31';

CPI_raw:
LOAD
    Date(MonthEnd(Date(date, 'YYYY-MM-DD'), 2), 'YYYY-MM-DD') AS QuarterEnd,
    Avg(Num(value)) AS CPI
FROM [raw/raw_macro_all.csv]
WHERE indicator = 'CPI' AND date >= '2021-01-01' AND date <= '2024-12-31'
GROUP BY QuarterEnd;

FedRate_raw:
LOAD
    Date(MonthEnd(Date(date, 'YYYY-MM-DD'), 2), 'YYYY-MM-DD') AS QuarterEnd,
    Avg(Num(value)) AS Fed_Rate
FROM [raw/raw_macro_all.csv]
WHERE indicator = 'FEDERAL_FUNDS_RATE' AND date >= '2021-01-01' AND date <= '2024-12-31'
GROUP BY QuarterEnd;

Unemployment_raw:
LOAD
    Date(MonthEnd(Date(date, 'YYYY-MM-DD'), 2), 'YYYY-MM-DD') AS QuarterEnd,
    Avg(Num(value)) AS Unemployment
FROM [raw/raw_macro_all.csv]
WHERE indicator = 'UNEMPLOYMENT' AND date >= '2021-01-01' AND date <= '2024-12-31'
GROUP BY QuarterEnd;
```

---

## Korak 5 — Normalizacija datuma na kraj kvartala

Financijski datumi moraju odgovarati makro datumima (oboje na kraju kvartala: 03-31, 06-30, 09-30, 12-31).

```qlik
FinancialAligned:
LOAD
    Date(MonthEnd(Date(Date, 'YYYY-MM-DD'), 2), 'YYYY-MM-DD') AS QuarterEnd,
    Company,
    Revenue,
    COGS,
    Operating_Expenses,
    EBITDA,
    Net_Income,
    Gross_Profit,
    Operating_Income
RESIDENT FinancialMillions;

DROP TABLE FinancialMillions;
```

---

## Korak 6 — Join financijskih i makro podataka

Spoji sve tablice po `QuarterEnd` datumu.

```qlik
MasterData:
LOAD
    QuarterEnd  AS Date,
    Company,
    Revenue,
    COGS,
    Operating_Expenses,
    EBITDA,
    Net_Income,
    Gross_Profit,
    Operating_Income
RESIDENT FinancialAligned;

LEFT JOIN (MasterData)
LOAD QuarterEnd AS Date, GDP FROM GDP_raw;

LEFT JOIN (MasterData)
LOAD QuarterEnd AS Date, CPI FROM CPI_raw;

LEFT JOIN (MasterData)
LOAD QuarterEnd AS Date, Fed_Rate FROM FedRate_raw;

LEFT JOIN (MasterData)
LOAD QuarterEnd AS Date, Unemployment FROM Unemployment_raw;

DROP TABLES FinancialAligned, GDP_raw, CPI_raw, FedRate_raw, Unemployment_raw;
```

---

## Korak 7 — Izvedene metrike

Izračunaj EBITDA maržu i filtriraj na period 2021–2024.

```qlik
FinalDataset:
LOAD
    Date,
    Company,
    Revenue,
    COGS,
    Operating_Expenses,
    EBITDA,
    Net_Income,
    Gross_Profit,
    Operating_Income,
    GDP,
    CPI,
    Fed_Rate,
    Unemployment,
    Round(EBITDA / Revenue * 100, 0.01) AS EBITDA_Margin,
    'millions USD' AS Currency_Unit
RESIDENT MasterData
WHERE Date >= '2021-01-01' AND Date <= '2024-12-31';

DROP TABLE MasterData;
```

---

## Korak 8 — Train/test split

```qlik
TrainSet:
LOAD * RESIDENT FinalDataset
WHERE Date <= '2023-12-31';

TestSet:
LOAD * RESIDENT FinalDataset
WHERE Date >= '2024-01-01';
```

---

## Rezultat ETL procesa

| Tablica | Redaka | Opis |
|---|---|---|
| `FinalDataset` | 80 | Cijeli dataset 2021–2024 |
| `TrainSet` | 60 | 2021–2023, za treniranje modela |
| `TestSet` | 20 | 2024, za evaluaciju modela |

**Stupci finalnog dataseta (13):**
`Date`, `Company`, `Revenue`, `COGS`, `Operating_Expenses`, `EBITDA`, `Net_Income`, `Gross_Profit`, `Operating_Income`, `GDP`, `CPI`, `Fed_Rate`, `Unemployment`, `EBITDA_Margin`, `Currency_Unit`

---

## Usporedba: Qlik ETL vs. Python pipeline

| Korak | Qlik Sense | Python |
|---|---|---|
| Load sirovih podataka | `LOAD ... FROM` | `pd.read_csv()` |
| Zamjena `None` → NULL | `IF(val='None', NULL(), Num(val))` | `pd.to_numeric(errors='coerce')` |
| Konverzija jedinica | `Round(col / 1000000, 0.01)` | `df[col] / 1_000_000` |
| Agregacija na kvartale | `GROUP BY QuarterEnd` | `resample("QE").mean()` |
| Normalizacija datuma | `MonthEnd(date, 2)` | `pd.offsets.QuarterEnd(0)` |
| Join tablica | `LEFT JOIN` | `pd.merge(..., how='left')` |
| Izvedene metrike | `Round(EBITDA/Revenue*100, 0.01)` | `(df.EBITDA / df.Revenue * 100).round(2)` |
| Filtriranje datuma | `WHERE Date >= '2021-01-01'` | `df[df.Date >= '2021-01-01']` |

Oba pristupa daju isti rezultat — Qlik demonstrira vizualni ETL proces, Python osigurava programatsku reproduktivnost.
