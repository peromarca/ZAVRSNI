# Što mogu pisati ODMAH

> Sve ispod ne zahtijeva pristup Qliku, Farseeru ni finalnom datasetu.
> Pisanje na hrvatskom, LaTeX datoteka: `zavrsni_rad.tex`

---

## POGLAVLJE 2 — Financijsko planiranje i analiza odstupanja
**Ciljano: ~1800–2500 riječi | ~5–7 stranica**

### 2.1 Postupci financijskog planiranja (~600–800 riječi)
- **Tradicionalno budžetiranje** — što je, godišnji ciklus, top-down vs bottom-up pristup, prednosti i mane
- **Rolling forecast** — što je kotrljajuća prognoza, kako se razlikuje od fiksnog budžeta, zašto je fleksibilnija
- **Scenarij planiranje** — best case / worst case / base case, primjena u neizvjesnim uvjetima

### 2.2 Ključni financijski pokazatelji (~300–400 riječi)
- Prihodi (ukupni, po segmentima), Troškovi (COGS, OPEX), Bruto marža, EBITDA, Neto dobit
- Kratke definicije + formule (npr. `EBITDA = Prihodi - COGS - OPEX`)

### 2.3 Metode analize odstupanja (~500–700 riječi)
- Definicija variance analysis (plan vs. ostvarenje)
- Formule: apsolutno odstupanje, relativno odstupanje (%)
- Price variance vs volume variance — kratko objašnjenje
- Primjer tablice: plan / ostvarenje / odstupanje (iznos i %)

### 2.4 Izazovi tradicionalnog pristupa (~400–500 riječi)
- Ručni procesi, pristranost planera (optimizam), nije skalabilno
- Statičnost godišnjeg budžeta u dinamičnom tržištu
- Ovaj dio vodi prirodno u uvod poglavlja 3 (zašto ML)

**Reference za ovo poglavlje:**
- `hyndman2021forecasting` — poglavlje o forecasting procesima
- `horngren2015cost` — klasična upravljačka računovodstvena knjiga
- `brealey2020principles` — principi korporativnih financija

---

## POGLAVLJE 3 — Metode strojnog učenja za financijsko predviđanje
**Ciljano: ~2000–2800 riječi | ~6–8 stranica**

### 3.1 Statističke metode (~700–900 riječi)
- **ARIMA** — AutoRegressive Integrated Moving Average, parametri (p,d,q), stacionarnost, kada koristiti
- **Eksponencijalno zaglađivanje** — Simple (SES), Double (Holt), Triple (Holt-Winters sa sezonalnošću)
- **Linearna regresija** — višestruka regresija za financijsko predviđanje, značajke (features)

### 3.2 Metode strojnog učenja (~800–1000 riječi)
- **Random Forest** — ensemble metoda, kako radi za regresiju, prednosti za tabelarne podatke
- **Gradient Boosting / XGBoost** — sekvencijalno poboljšanje, zašto je popularan za financije
- **LSTM neuronske mreže** — kratki opis, pamćenje dugih zavisnosti, primjena na vremenske serije
  *(samo kratki opis — ne treba ići u dubinu, Farseer ga koristi interno)*

### 3.3 Metrike evaluacije modela (~300–400 riječi)
- **MAE** — Mean Absolute Error (formula + interpretacija)
- **RMSE** — Root Mean Square Error (osjetljiviji na outliere)
- **MAPE** — Mean Absolute Percentage Error (interpretabilniji za biznis)
- Kratka usporedba kada koristiti koju metriku

### 3.4 Odabir metode za primjenu (~200–300 riječi)
- Zašto je ML bolji od čiste statistike za kompleksne financijske serije
- Osvrt na tablicu usporedbe (već postavljena u .tex — samo popuni vrijednosti)

**Reference za ovo poglavlje:**
- `hastie2009elements` — teorijska osnova ML metoda
- `breiman2001random` — originalni Random Forest rad
- `chen2016xgboost` — XGBoost paper
- `hochreiter1997lstm` — originalni LSTM rad
- `makridakis2018statistical` — usporedba statističkih i ML metoda
- `ahmed2010empirical` — empirijska usporedba za vremenske serije
- `hyndman2006another` — metrike evaluacije
- `fischer2018deep` — deep learning za financije
- `masini2023machine` — ML za forecasting (pregled)

---

## POGLAVLJE 4 — Alati (opći dio, bez screenshotova)
**Ciljano: ~1200–1600 riječi | ~4–5 stranica**

### 4.1 Qlik Sense (~400–500 riječi)
- Što je Qlik Sense, kratka povijest, pozicioniranje na tržištu BI alata
- **Asocijativni model podataka** — ključna razlika od SQL/tabličnog pristupa, in-memory engine
- ETL mogućnosti — load script, transformacije, spajanje izvora podataka
- Self-service BI — korisnici bez tehničkih znanja mogu istraživati podatke

### 4.2 Farseer (~400–500 riječi)
- Što je Farseer, da je hrvatski softver, za koga je namijenjen (FP&A odjeli)
- Mogućnosti financijskog planiranja — budžetiranje, forecasting, version management
- ML feature — opis na visokoj razini (bez detalja koje ne znaš dok ne dobiješ pristup)
- Zašto je dobar odabir za ovaj rad

### 4.3 Alternativni pristupi (~300–400 riječi)
- Power BI + Azure ML — prednosti/mane
- Python ekosustav (pandas, scikit-learn, Prophet) — fleksibilnost ali složenost
- SAP Analytics Cloud — enterprise rješenje
- Tablica usporedbe je već u .tex — samo popuni tekstualni komentar ispod tablice

### 4.4 Arhitektura rješenja (~100–150 riječi)
- Kratki tekstualni opis toka: podatci → Qlik (ETL + vizualizacija) → Farseer (predviđanje)
- *(Dijagram/slika dolazi kad dobiješ pristup alatima)*

**Reference za ovo poglavlje:**
- `qlik2024` — službena Qlik dokumentacija
- `farseer2024` — Farseer web stranica
- `kimball2013data` — data warehouse pristup (za ETL dio)

---

## UKUPNO ZA ODMAH
| Poglavlje | Stranice | Riječi |
|-----------|----------|--------|
| 2. Financijsko planiranje | 5–7 str. | ~1800–2500 |
| 3. Metode ML | 6–8 str. | ~2000–2800 |
| 4. Alati (opći dio) | 4–5 str. | ~1200–1600 |
| **Ukupno** | **~15–20 str.** | **~5000–6900** |

To je otprilike **40–50% cijelog rada** koji možeš završiti bez pristupa alatima.

---

## NAPOMENE ZA PISANJE

- Svako poglavlje počni s kratkim uvodnim odlomkom (2-3 rečenice) koji objašnjava što će biti opisano
- Formule pišeš u LaTeX-u kao `\begin{equation}...\end{equation}`
- Za tablice koristi strukturu koja je već postavljena u `.tex`
- Kada citiš: `\cite{breiman2001random}` — ključevi su već u `literatura.bib`
- Tekst piši u slobodnom obliku — ne treba biti savršen, bitno je pokriti sadržaj
- Slike (dijagrami, grafovi) dodaješ naknadno kad imaš screenshotove

## PREPORUČENI SLIJED PISANJA
1. Poglavlje 3.1 + 3.2 (Metode ML) — najviše referenci, najlakše istražiti
2. Poglavlje 2.3 + 2.4 (Analiza odstupanja + izazovi) — prirodno vodi u ML
3. Poglavlje 2.1 + 2.2 (Planiranje + KPI) — teorija
4. Poglavlje 4 (Alati) — istraži Qlik i Farseer web dokumentaciju
