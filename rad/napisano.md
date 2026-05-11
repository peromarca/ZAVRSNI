# Napisano — Praćenje napretka završnog rada

> Zadnje ažuriranje: 4. svibnja 2026.
> Ukupni napredak: **~45%** — teorijski dio gotov, praktični čeka podatke

---

## Poglavlje 1 — Uvod
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| Uvodni tekst | ✅ Napisano | — | Ažurirano: Farseer uklonjen, dodani Qlik Predict + Python |

## Poglavlje 2 — Financijsko planiranje i analiza odstupanja
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| 2.1.1 Tradicionalno budžetiranje | ✅ Napisano | Horngren (2015), Brealey (2020) | Top-down vs bottom-up, prednosti/mane, statičnost |
| 2.1.2 Kotrljajuća prognoza | ✅ Napisano | Melnychuk (2019) FP&A Trends | Definicija, 4-6 kvartala unaprijed, 25% adopcija |
| 2.1.3 Scenarij planiranje | ✅ Napisano | Brealey (2020) str. 831 | Base/best/worst case, sensitivity vs scenario analysis |
| 2.2 Ključni financijski pokazatelji | ✅ Napisano | Horngren (2015), Brealey (2020) | Prihodi, COGS, OPEX, EBITDA, formule (eq. 1-3) |
| 2.3 Metode analize odstupanja | ✅ Napisano | Horngren (2015) pogl. 7-8 | Apsolutno/relativno odstupanje, price/volume variance, primjer tablica |
| 2.4 Izazovi tradicionalnog pristupa | ✅ Napisano | Makridakis (2018) | 4 izazova: ručni procesi, pristranost, statičnost, neskalabilnost |

## Poglavlje 3 — Metode strojnog učenja za financijsko predviđanje
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| 3.1.1 ARIMA | ✅ Napisano | Box & Jenkins (1970), Hyndman (2021) | Parametri (p,d,q), formula, ACF/PACF, SARIMA |
| 3.1.2 Eksponencijalno zaglađivanje | ✅ Napisano | Hyndman (2021) pogl. 7 | SES formula, Holt, Holt-Winters (aditivna/multiplikativna) |
| 3.1.3 Linearna regresija | ✅ Napisano | Hastie (2009), Masini (2023) | Višestruka regresija, formula, prednosti/mane |
| 3.2.1 Random Forest | ✅ Napisano | Breiman (2001) | Bootstrap, ensemble, formula prosjeka stabala |
| 3.2.2 Gradient Boosting / XGBoost | ✅ Napisano | Chen (2016), Hastie (2009) | Sekvencijalno učenje, learning rate, regularizacija |
| 3.2.3 LSTM neuronske mreže | ✅ Napisano | Hochreiter (1997), Fischer (2018) | Forget/input/output gates, prednosti za fin. serije |
| 3.3 Metrike evaluacije | ✅ Napisano | Hyndman (2006) | MAE, RMSE, MAPE — formule + interpretacija |
| 3.4 Odabir metode | ✅ Napisano | Makridakis (2018), Masini (2023) | Qlik Predict vs Python benchmark pristup |

## Poglavlje 4 — Korišteni alati i tehnologije
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| 4.1 Qlik Sense | ✅ Napisano | Qlik docs (2024) | Asocijativni model, ETL load script, vizualizacija |
| 4.2 Qlik Predict | ✅ Napisano | Qlik Predict docs (2024) | AutoML, SHAP, Predict() funkcija, no-code |
| 4.3 Python ekosustav | ✅ Napisano | scikit-learn, statsmodels, keras docs | pandas, statsmodels, scikit-learn, Keras, matplotlib |
| 4.3.1 Qlik SSE integracija | ✅ Napisano | Qlik SSE docs (2024) | Kratki opis (~100 riječi), microservice pristup |
| 4.4 Alternativni pristupi | ✅ Napisano | Općenito | Power BI + Azure ML, SAP Analytics Cloud, samo Python |
| 4.5 Arhitektura rješenja | ✅ Napisano | — | 3 komponente: Qlik ETL → Qlik Predict → Python benchmark |

## Poglavlje 5 — Priprema i obrada podataka
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| Cijelo poglavlje | ❌ Čeka podatke | — | Potreban pristup Qliku i podatcima |

## Poglavlje 6 — Rezultati predviđanja i usporedba
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| Cijelo poglavlje | ❌ Čeka podatke | — | Potreban pristup Qliku, Qlik Predictu i Python implementaciji |

## Poglavlje 7 — Zaključak
| Sekcija | Status | Izvor | Napomena |
|---------|--------|-------|----------|
| Zaključak | ❌ Čeka rezultate | — | Piše se na kraju |

---

## Dodatne izmjene
| Stavka | Status | Napomena |
|--------|--------|----------|
| Sažetak (HR) | ✅ Ažurirano | Farseer → Qlik Predict + Python |
| Abstract (EN) | ✅ Ažurirano | Farseer → Qlik Predict + Python |
| Ključne riječi | ✅ Ažurirano | Dodani: Qlik Predict, Python |
| literatura.bib | ✅ Ažurirano | Dodan: melnychuk2019rolling, qlikpredict2024, qliksse2024, scikitlearn2024, statsmodels2024, keras2024. Uklonjen: farseer2024 |
| generate_mock_data.py | ✅ Ažurirano | Komentar: Farseer → Qlik Predict + Python |

---

## Legenda
- ✅ Napisano
- 🔄 U tijeku
- ❌ Nije početo
