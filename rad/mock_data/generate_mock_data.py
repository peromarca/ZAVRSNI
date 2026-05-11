"""
Skripta za generiranje anonimiziranih mock financijskih podataka.
Generira mjesečne P&L podatke za fiktivnu tvrtku "AlphaServis d.o.o."
za razdoblje od siječnja 2021. do prosinca 2025.

Podatci su strukturirani tako da budu pogodni za:
1. Učitavanje u Qlik Sense (ETL i vizualizacija)
2. Export u format za Qlik Predict i Python ML modele (predviđanje)

Zadnjih 20% podataka (2025.) služi kao test set za usporedbu predikcija.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import os

# Fiksni seed za reproduktivnost
np.random.seed(42)

# =============================================================================
# PARAMETRI
# =============================================================================
START_DATE = "2021-01-01"
END_DATE = "2025-12-31"
COMPANY_NAME = "AlphaServis d.o.o."

# Segmenti prihoda
REVENUE_SEGMENTS = {
    "Konzalting": {"base": 450_000, "growth_annual": 0.08, "seasonality_amp": 0.12},
    "Licenciranje": {"base": 280_000, "growth_annual": 0.15, "seasonality_amp": 0.05},
    "Implementacija": {"base": 320_000, "growth_annual": 0.10, "seasonality_amp": 0.18},
    "Podrška": {"base": 180_000, "growth_annual": 0.05, "seasonality_amp": 0.03},
}

# Kategorije troškova (kao postotak ukupnih prihoda + fiksna komponenta)
COST_CATEGORIES = {
    "Plaće i naknade": {"fixed": 380_000, "variable_pct": 0.10, "growth_annual": 0.06},
    "Materijalni troškovi": {"fixed": 45_000, "variable_pct": 0.05, "growth_annual": 0.03},
    "Usluge trećih strana": {"fixed": 30_000, "variable_pct": 0.08, "growth_annual": 0.04},
    "Amortizacija": {"fixed": 55_000, "variable_pct": 0.00, "growth_annual": 0.02},
    "Ostali troškovi": {"fixed": 25_000, "variable_pct": 0.03, "growth_annual": 0.03},
}

# Makroekonomski indikatori (kvartalni)
MACRO_PARAMS = {
    "BDP_rast_pct": {"start": 3.2, "trend": -0.1, "noise_std": 0.5},
    "Inflacija_pct": {"start": 2.0, "trend": 0.3, "noise_std": 0.4},
    "EUR_HRK": {"start": 7.53, "trend": -0.01, "noise_std": 0.02},  # do uvođenja eura
}


# =============================================================================
# GENERIRANJE VREMENSKIH SERIJA
# =============================================================================
def generate_dates(start, end, freq="MS"):
    """Generira datumski niz."""
    return pd.date_range(start=start, end=end, freq=freq)


def add_seasonality(n_months, amplitude, peak_month=11):
    """Dodaje sezonalnost s vrhom u zadanom mjesecu (0-indexed, 11 = prosinac)."""
    months = np.arange(n_months)
    return amplitude * np.sin(2 * np.pi * (months - peak_month + 3) / 12)


def add_trend(n_months, annual_growth_rate):
    """Dodaje eksponencijalni trend."""
    months = np.arange(n_months)
    return (1 + annual_growth_rate) ** (months / 12)


def add_noise(n_months, noise_pct=0.05):
    """Dodaje slučajni šum."""
    return 1 + np.random.normal(0, noise_pct, n_months)


def generate_revenue_data(dates):
    """Generira mjesečne prihode po segmentima."""
    n = len(dates)
    records = []

    for segment, params in REVENUE_SEGMENTS.items():
        base = params["base"]
        trend = add_trend(n, params["growth_annual"])
        seasonality = add_seasonality(n, params["seasonality_amp"])
        noise = add_noise(n, noise_pct=0.06)

        values = base * trend * (1 + seasonality) * noise
        values = np.round(values, 2)

        for date, value in zip(dates, values):
            records.append({
                "Datum": date,
                "Godina": date.year,
                "Mjesec": date.month,
                "Segment": segment,
                "Prihod_EUR": max(value, 0),
            })

    return pd.DataFrame(records)


def generate_cost_data(dates, total_monthly_revenue):
    """Generira mjesečne troškove po kategorijama."""
    n = len(dates)
    records = []

    for category, params in COST_CATEGORIES.items():
        fixed = params["fixed"]
        var_pct = params["variable_pct"]
        trend = add_trend(n, params["growth_annual"])
        noise = add_noise(n, noise_pct=0.04)

        for i, (date, rev) in enumerate(zip(dates, total_monthly_revenue)):
            value = (fixed * trend[i] + var_pct * rev) * noise[i]
            value = round(max(value, 0), 2)
            records.append({
                "Datum": date,
                "Godina": date.year,
                "Mjesec": date.month,
                "Kategorija_troška": category,
                "Trošak_EUR": value,
            })

    return pd.DataFrame(records)


def generate_macro_data(start, end):
    """Generira kvartalne makroekonomske indikatore."""
    quarters = pd.date_range(start=start, end=end, freq="QS")
    n = len(quarters)
    records = []

    for q_date in quarters:
        record = {"Datum": q_date, "Godina": q_date.year, "Kvartal": (q_date.month - 1) // 3 + 1}

        for indicator, params in MACRO_PARAMS.items():
            idx = list(quarters).index(q_date)
            value = params["start"] + params["trend"] * (idx / 4) + np.random.normal(0, params["noise_std"])

            # EUR/HRK fiksiran na ~7.5345 nakon 2023 (uvođenje eura)
            if indicator == "EUR_HRK" and q_date.year >= 2023:
                value = 7.5345

            record[indicator] = round(value, 2)

        records.append(record)

    return pd.DataFrame(records)


def generate_plan_data(revenue_df, cost_df):
    """
    Generira planske podatke (budžet) s realnošću:
    - Plan se radi krajem prethodne godine za sljedeću
    - Koristi se prošlogodišnji trend + pretpostavljeni rast
    - Dodaje se "bias" jer planovi su tipično optimistični
    """
    # Agregiraj prihode po mjesecu
    monthly_rev = revenue_df.groupby(["Godina", "Mjesec"])["Prihod_EUR"].sum().reset_index()
    monthly_cost = cost_df.groupby(["Godina", "Mjesec"])["Trošak_EUR"].sum().reset_index()

    plan_records = []
    years = sorted(monthly_rev["Godina"].unique())

    for year in years:
        if year == years[0]:
            # Za prvu godinu plan = actuals * (1 + optimistic_bias)
            bias = np.random.uniform(0.02, 0.08)
            year_rev = monthly_rev[monthly_rev["Godina"] == year].copy()
            year_cost = monthly_cost[monthly_cost["Godina"] == year].copy()

            for _, row in year_rev.iterrows():
                plan_rev = row["Prihod_EUR"] * (1 + bias + np.random.normal(0, 0.03))
                plan_records.append({
                    "Datum": pd.Timestamp(year=int(row["Godina"]), month=int(row["Mjesec"]), day=1),
                    "Godina": int(row["Godina"]),
                    "Mjesec": int(row["Mjesec"]),
                    "Plan_prihod_EUR": round(max(plan_rev, 0), 2),
                })

            for _, row in year_cost.iterrows():
                plan_cost = row["Trošak_EUR"] * (1 - np.random.uniform(0, 0.03) + np.random.normal(0, 0.02))
                idx = len(plan_records) - 12 + int(row["Mjesec"]) - 1
                if 0 <= idx < len(plan_records):
                    plan_records[idx]["Plan_trošak_EUR"] = round(max(plan_cost, 0), 2)
        else:
            # Za ostale godine: prošla godina * (1 + planirani rast)
            prev_rev = monthly_rev[monthly_rev["Godina"] == year - 1]
            prev_cost = monthly_cost[monthly_cost["Godina"] == year - 1]
            growth_assumption = np.random.uniform(0.05, 0.12)
            cost_growth = np.random.uniform(0.03, 0.07)

            for month in range(1, 13):
                prev_r = prev_rev[prev_rev["Mjesec"] == month]["Prihod_EUR"].values
                prev_c = prev_cost[prev_cost["Mjesec"] == month]["Trošak_EUR"].values

                if len(prev_r) > 0 and len(prev_c) > 0:
                    plan_rev = prev_r[0] * (1 + growth_assumption + np.random.normal(0, 0.02))
                    plan_cost = prev_c[0] * (1 + cost_growth + np.random.normal(0, 0.02))

                    plan_records.append({
                        "Datum": pd.Timestamp(year=year, month=month, day=1),
                        "Godina": year,
                        "Mjesec": month,
                        "Plan_prihod_EUR": round(max(plan_rev, 0), 2),
                        "Plan_trošak_EUR": round(max(plan_cost, 0), 2),
                    })

    return pd.DataFrame(plan_records)


# =============================================================================
# MAIN
# =============================================================================
def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Generiranje mock podataka za: {COMPANY_NAME}")
    print(f"Period: {START_DATE} - {END_DATE}")
    print(f"Output direktorij: {output_dir}")
    print("-" * 60)

    # Generiraj datume
    dates = generate_dates(START_DATE, END_DATE)
    print(f"Generirano {len(dates)} mjeseci")

    # 1. Prihodi
    revenue_df = generate_revenue_data(dates)
    print(f"Prihodi: {len(revenue_df)} zapisa ({len(REVENUE_SEGMENTS)} segmenata)")

    # 2. Troškovi (treba ukupni mjesečni prihod)
    monthly_revenue = revenue_df.groupby("Datum")["Prihod_EUR"].sum().values
    cost_df = generate_cost_data(dates, monthly_revenue)
    print(f"Troškovi: {len(cost_df)} zapisa ({len(COST_CATEGORIES)} kategorija)")

    # 3. Makroekonomski indikatori
    macro_df = generate_macro_data(START_DATE, END_DATE)
    print(f"Makro indikatori: {len(macro_df)} kvartala")

    # 4. Planski podatci
    plan_df = generate_plan_data(revenue_df, cost_df)
    print(f"Planski podatci: {len(plan_df)} zapisa")

    # 5. Izvedeni P&L (agregirani)
    monthly_rev_agg = revenue_df.groupby(["Datum", "Godina", "Mjesec"])["Prihod_EUR"].sum().reset_index()
    monthly_rev_agg.rename(columns={"Prihod_EUR": "Ukupni_prihod_EUR"}, inplace=True)

    monthly_cost_agg = cost_df.groupby(["Datum", "Godina", "Mjesec"])["Trošak_EUR"].sum().reset_index()
    monthly_cost_agg.rename(columns={"Trošak_EUR": "Ukupni_trošak_EUR"}, inplace=True)

    pl_df = monthly_rev_agg.merge(monthly_cost_agg, on=["Datum", "Godina", "Mjesec"])
    pl_df["EBITDA_EUR"] = pl_df["Ukupni_prihod_EUR"] - pl_df["Ukupni_trošak_EUR"]
    pl_df["EBITDA_marža_pct"] = round(pl_df["EBITDA_EUR"] / pl_df["Ukupni_prihod_EUR"] * 100, 2)

    # Spoji s planskim podatcima
    pl_df = pl_df.merge(plan_df, on=["Datum", "Godina", "Mjesec"], how="left")
    pl_df["Plan_EBITDA_EUR"] = pl_df["Plan_prihod_EUR"] - pl_df["Plan_trošak_EUR"]

    # Izračunaj odstupanja
    pl_df["Odstupanje_prihod_EUR"] = pl_df["Ukupni_prihod_EUR"] - pl_df["Plan_prihod_EUR"]
    pl_df["Odstupanje_prihod_pct"] = round(
        pl_df["Odstupanje_prihod_EUR"] / pl_df["Plan_prihod_EUR"] * 100, 2
    )
    pl_df["Odstupanje_EBITDA_EUR"] = pl_df["EBITDA_EUR"] - pl_df["Plan_EBITDA_EUR"]

    print(f"P&L izvještaj: {len(pl_df)} mjeseci")

    # === SPREMI CSV DATOTEKE ===
    revenue_df.to_csv(os.path.join(output_dir, "prihodi_po_segmentima.csv"), index=False, encoding="utf-8-sig")
    cost_df.to_csv(os.path.join(output_dir, "troskovi_po_kategorijama.csv"), index=False, encoding="utf-8-sig")
    macro_df.to_csv(os.path.join(output_dir, "makroekonomski_indikatori.csv"), index=False, encoding="utf-8-sig")
    plan_df.to_csv(os.path.join(output_dir, "planski_podatci.csv"), index=False, encoding="utf-8-sig")
    pl_df.to_csv(os.path.join(output_dir, "pl_izvjestaj.csv"), index=False, encoding="utf-8-sig")

    print("-" * 60)
    print("Generirane datoteke:")
    print("  1. prihodi_po_segmentima.csv    - mjesečni prihodi po 4 segmenta")
    print("  2. troskovi_po_kategorijama.csv  - mjesečni troškovi po 5 kategorija")
    print("  3. makroekonomski_indikatori.csv - kvartalni makro indikatori")
    print("  4. planski_podatci.csv           - budžetirani prihodi i troškovi")
    print("  5. pl_izvjestaj.csv              - agregirani P&L s odstupanjima")

    # === STATISTIKE ===
    print("\n" + "=" * 60)
    print("PREGLED GENERIRANIH PODATAKA")
    print("=" * 60)

    print(f"\nUkupni prihod (2021-2025): {pl_df['Ukupni_prihod_EUR'].sum():,.0f} EUR")
    print(f"Prosječni mjesečni prihod: {pl_df['Ukupni_prihod_EUR'].mean():,.0f} EUR")
    print(f"Prosječna EBITDA marža: {pl_df['EBITDA_marža_pct'].mean():.1f}%")

    for year in sorted(pl_df["Godina"].unique()):
        year_data = pl_df[pl_df["Godina"] == year]
        print(f"\n{year}:")
        print(f"  Prihod: {year_data['Ukupni_prihod_EUR'].sum():>12,.0f} EUR")
        print(f"  Trošak: {year_data['Ukupni_trošak_EUR'].sum():>12,.0f} EUR")
        print(f"  EBITDA:  {year_data['EBITDA_EUR'].sum():>12,.0f} EUR")
        print(f"  Marža:   {year_data['EBITDA_marža_pct'].mean():>11.1f}%")

    # Train/test split info
    print(f"\n{'=' * 60}")
    print("TRAIN/TEST SPLIT")
    print(f"{'=' * 60}")
    train = pl_df[pl_df["Godina"] <= 2024]
    test = pl_df[pl_df["Godina"] == 2025]
    print(f"Train set: {len(train)} mjeseci (2021-2024)")
    print(f"Test set:  {len(test)} mjeseci (2025)")


if __name__ == "__main__":
    main()
