# Prompt za Claude u Canvi — Vizual pipeline-a završnog rada

Kopiraj sve ispod i zalijepi u Claude unutar Canve.

---

## PROMPT:

Napravi profesionalnu prezentaciju (5–6 slajdova) za internu prezentaciju timu u firmi. Tema: završni rad na FER-u — "Predviđanje financijskih pokazatelja primjenom metoda strojnog učenja". Stil: moderan, čist, tamna pozadina (dark theme), s ikonama i dijagramima. Koristi boje: tamno plava (#1a1a2e), naglasak tirkizna (#00d4aa) i bijeli tekst.

---

### SLAJD 1 — Naslov

**Predviđanje financijskih pokazatelja primjenom metoda strojnog učenja**
Petar | FER Zagreb | 2026.
Mentor: izv. prof. dr. sc. Goran Delač

Podnaslov: "Kako ML može poboljšati točnost financijskih prognoza?"

---

### SLAJD 2 — Arhitektura rješenja (PIPELINE DIJAGRAM)

Napravi horizontalni pipeline dijagram s 3 glavna bloka spojenih strelicama:

```
[IZVORI PODATAKA] → [OBRADA & ETL] → [PREDVIĐANJE] → [EVALUACIJA]
```

Detaljnije:

**Blok 1: Izvori podataka**
- ERP sustav (mjesečni P&L: prihodi, COGS, OPEX)
- Računovodstvo (troškovi po kategorijama)
- Javni izvori (makroekonomski indikatori: BDP, inflacija, kamatne stope)
- Period: 2021–2025, mjesečna granularnost

**Blok 2: Obrada & ETL (Qlik Sense)**
- Load script: učitavanje, čišćenje, transformacija
- Anonimizacija podataka
- Spajanje izvora u jedinstveni analitički skup
- Qlik podatkovni model (asocijativni engine)
- Output: čist dataset spreman za modele

**Blok 3: Predviđanje (dva paralelna puta)**
Put A — Qlik Predict (no-code):
  - Automatski odabir modela
  - SHAP objašnjivost
  - Predict() funkcija u Qlik aplikaciji

Put B — Python (code benchmark):
  - ARIMA (statsmodels)
  - XGBoost (scikit-learn)
  - LSTM (Keras/TensorFlow)

**Blok 4: Evaluacija & Usporedba**
- Metrike: MAE, RMSE, MAPE
- Qlik Predict vs Python modeli
- Usporedba s naivnom prognozom (baseline)
- Vizualizacija u Qlik dashboardu

---

### SLAJD 3 — Poglavlje 5: Priprema podataka (detaljni pipeline)

Napravi vertikalni flow diagram s 5 koraka:

```
1. PRIKUPLJANJE
   └─ ERP export (CSV/Excel) + javni makro podatci
   
2. ANONIMIZACIJA
   └─ Promjena naziva tvrtke, modifikacija iznosa uz očuvanje trendova
   
3. ČIŠĆENJE (Qlik Load Script)
   └─ Nedostajuće vrijednosti, outlieri, formati datuma
   
4. TRANSFORMACIJA
   └─ Pivotiranje, agregiranje, izračun EBITDA i marži
   └─ Kreiranje Qlik podatkovnog modela
   
5. PRIPREMA ZA MODELE
   └─ Train set: 2021–2024 (80%)
   └─ Test set: 2025 (20%)
   └─ Export za Qlik Predict + Export CSV za Python
```

Pored svakog koraka stavi malu ikonu (📥 📝 🧹 🔄 📊).

---

### SLAJD 4 — Poglavlje 6: Modeli i usporedba

Napravi tablicu/grid s dva stupca:

| Qlik Predict (no-code) | Python ML (benchmark) |
|---|---|
| Automatski odabir algoritma | Ručna implementacija |
| Zero-code konfiguracija | Potpuna kontrola hiperparametara |
| SHAP vrijednosti za objašnjivost | Custom vizualizacije |
| Integriran u Qlik dashboard | Standalone skripte |
| **Modeli**: auto-selected | **Modeli**: ARIMA, XGBoost, LSTM |

Ispod tablice napravi 3 mini grafa (placeholder) s labelama:
- Predviđanje prihoda (Actual vs Predicted)
- Predviđanje troškova (Actual vs Predicted)  
- Predviđanje EBITDA (Actual vs Predicted)

I tablicu metrika:
| Pokazatelj | MAE | RMSE | MAPE (%) |
|---|---|---|---|
| Prihodi | ? | ? | ? |
| Troškovi | ? | ? | ? |
| EBITDA | ? | ? | ? |

---

### SLAJD 5 — Opcija: SSE integracija (bonus)

Mali dijagram koji pokazuje:
```
Qlik Sense App → SSE konektor → Python microservice → Rezultati natrag u Qlik
```

Kratki tekst: "Moguća integracija Python modela direktno u Qlik putem Server-Side Extensions — best of both worlds."

---

### SLAJD 6 — Status i sljedeći koraci

Napravi progress bar ili checklist:

✅ Poglavlje 1 — Uvod (gotovo)
✅ Poglavlje 2 — Financijsko planiranje i analiza odstupanja (gotovo)
✅ Poglavlje 3 — Metode strojnog učenja (gotovo)
✅ Poglavlje 4 — Korišteni alati i tehnologije (gotovo)
🔲 Poglavlje 5 — Priprema i obrada podataka (ČEKA: pristup Qliku i podatcima)
🔲 Poglavlje 6 — Rezultati predviđanja i usporedba (ČEKA: Qlik Predict + Python)
🔲 Poglavlje 7 — Zaključak

Progress: ~45% teorijskog dijela gotovo

**Što trebam od tima:**
- Pristup Qlik Cloud instanci s Predict licencom
- Pristup anonimiziranim financijskim podatcima klijenta
- Validacija pipeline pristupa

---

NAPOMENA ZA CLAUDE U CANVI: Koristi moderan, profesionalan dizajn. Svaki slajd treba biti vizualno jasan i čitljiv. Pipeline dijagrami trebaju imati zaobljene kutove, strelice i ikone. Ne stavljaj previše teksta — koristi bullet pointove i vizuale.
