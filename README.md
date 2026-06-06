# UK FTTP Opportunity Map

Public-data Streamlit dashboard for understanding UK full-fibre availability and opportunity at postcode district level.

## Scope

- Public data only.
- FTTP / full fibre only.
- Postcode district geography, such as `SW1`, `M1`, and `B15`.
- Premises-led opportunity scoring.

## Run

```powershell
pip install -r requirements.txt
streamlit run main.py
```

The app downloads the public Ofcom/ONS cache files on first run. You can also prefetch them manually:

```powershell
python scripts/fetch_real_data.py
```

## Methodology

The core opportunity metric is premises without FTTP:

```text
non_fttp_premises = total_premises - fttp_available_premises
```

The first scoring model is:

```text
opportunity_score =
  50% normalised non-FTTP premises
+ 30% inverse FTTP coverage percentage
+ 20% premises density
```

Population is secondary context. Copper, ADSL, PSTN, and FTTC-only coverage are out of scope.

## Data Caveat

Version 1 includes processed public Ofcom/ONS data in `data/public` for reliable deployment. If the required public files cannot be loaded, the app shows a transparent unavailable-data message instead of silently substituting sample values. Public-data ingestion is transparent and reproducible, but exact provider attribution is not part of the first release.

The current real-data layer uses Ofcom Spring 2026 local-authority FTTP coverage because the Spring 2026 postcode CSVs inspected in the Ofcom ZIP do not expose an explicit `Full Fibre availability` column. The postcode-district sample remains in the repo for development/demo checks only and is not used as a production fallback.
