# UK FTTP Opportunity Map

Public-data Streamlit dashboard for understanding UK full-fibre availability and remaining FTTP opportunity.

## Scope

- Public data only.
- FTTP / full fibre only.
- Real deployed geography: UK local authorities.
- Postcode district sample data is retained only for development/demo checks.
- Premises-led opportunity scoring.

## Run

```powershell
pip install -r requirements.txt
streamlit run main.py
```

The deployed app uses processed public Ofcom/ONS files committed in `data/public`. You can refresh the source cache manually:

```powershell
python scripts/fetch_real_data.py
```

## Methodology

### Data Inputs

The real deployed layer uses:

- Ofcom Connected Nations Spring 2026 fixed broadband coverage data.
- ONS Local Authority Districts December 2025 boundaries.

From Ofcom, the app uses the local-authority coverage file:

```text
202601_fixed_laua_coverage_r1/202601_fixed_laua_coverage_r1.csv
```

The main source fields are mapped as:

| App field | Ofcom source field |
|---|---|
| `postcode_district` | `laua` |
| `area_name` | `laua_name` |
| `total_premises` | `All Premises` |
| `fttp_available_premises` | `Number of premises with Full Fibre availability` |

The field name `postcode_district` is currently reused as the internal geography key, but in the real deployed layer it contains the local-authority code, such as `E06000052`.

### Core Metrics

The core opportunity metric is premises without FTTP:

```text
non_fttp_premises = total_premises - fttp_available_premises
```

FTTP coverage percentage is:

```text
fttp_coverage_percent =
  (fttp_available_premises / total_premises) * 100
```

Premises density is:

```text
premises_density = total_premises / area_sq_km
```

For the current local-authority public layer, `area_sq_km` is not included in the Ofcom coverage file, so density is set to `0`. This means the current opportunity score is effectively driven by:

- remaining premises without FTTP
- inverse FTTP coverage

The density component is retained in the model for future postcode-district or boundary-derived area calculations.

### Opportunity Score

The app calculates three component scores:

```text
non_fttp_score =
  min-max normalised non_fttp_premises

inverse_coverage_score =
  1 - (fttp_coverage_percent / 100)

density_score =
  min-max normalised premises_density
```

The final score is:

```text
opportunity_score =
  (
    0.50 * non_fttp_score
  + 0.30 * inverse_coverage_score
  + 0.20 * density_score
  ) * 100
```

Scores are rounded to two decimal places. A higher score means a larger public-data FTTP opportunity, not a guaranteed build recommendation.

### Opportunity Categories

Categories are assigned using these rules, in order:

| Category | Rule |
|---|---|
| `Full-fibre strong` | FTTP coverage is at least 85% and fewer than 500 premises remain without FTTP |
| `Dense priority` | FTTP coverage is below 40% and premises density is at least 750 premises per sq km |
| `Major opportunity` | At least 5,000 premises remain without FTTP |
| `Fibre gap` | FTTP coverage is below 40% |
| `Moderate coverage` | FTTP coverage is below 75% |
| `Lower priority` | Opportunity score is below 25 |
| `Moderate coverage` | Default category if no earlier rule matches |

Because current local-authority density is `0`, `Dense priority` will not normally appear until area/density data is added.

### Interpretation

The score is designed to highlight areas where public data suggests:

- many premises remain without full fibre
- FTTP coverage is relatively low
- future versions may also account for density/build economics

It should not be interpreted as:

- an Openreach internal strength/weakness score
- a provider-specific market share model
- a build-cost model
- a copper, ADSL, PSTN, FTTC, or gigabit-capable broadband score

Copper, ADSL, PSTN, FTTC-only, and gigabit-capable proxy metrics are out of scope. The app uses explicit Ofcom `Full Fibre availability` fields only.

## Data Caveat

Version 1 includes processed public Ofcom/ONS data in `data/public` for reliable deployment. If the required public files cannot be loaded, the app shows a transparent unavailable-data message instead of silently substituting sample values. Public-data ingestion is transparent and reproducible, but exact provider attribution is not part of the first release.

The current real-data layer uses Ofcom Spring 2026 local-authority FTTP coverage because the Spring 2026 postcode CSVs inspected in the Ofcom ZIP do not expose an explicit `Full Fibre availability` column. The postcode-district sample remains in the repo for development/demo checks only and is not used as a production fallback.
