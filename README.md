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

Version 1 supports sample/cache data. Public-data ingestion should be treated as transparent and reproducible, but exact provider attribution is not part of the first release.

The current dashboard ships with sample postcode district metrics and geometry. It validates the methodology and interface; replacing the sample files with current Ofcom and ONS public data is the next data-engineering step.
