# Public Data Sources

## FTTP Coverage

Primary candidate: Ofcom Connected Nations fixed broadband coverage and full-fibre datasets.

Current implemented source:

- Ofcom Connected Nations Spring 2026 fixed broadband coverage ZIP.
- File used: `202601_fixed_laua_coverage_r1/202601_fixed_laua_coverage_r1.csv`.
- Columns used: `All Premises` and `Number of premises with Full Fibre availability`.

Needed fields:

- geography or postcode reference
- total premises
- FTTP available premises or FTTP availability percentage
- publication date

## Postcode District Geography

Primary candidate: ONS Postcode Directory / National Statistics Postcode Lookup and ONS Open Geography Portal.

Needed fields:

- full postcode or postcode district
- coordinates or geographic lookup
- nation / region / local authority where available

## Boundary Geometry

Preferred: public postcode district boundary GeoJSON or shapefile.

Fallback: derive approximate postcode district geometry from postcode points and label the limitation in the app.

Current implemented source:

- ONS Local Authority Districts December 2025 Boundaries UK BGC.
- Feature key used for joining: `LAD25CD`.

## Version 1 Rule

Do not include copper, ADSL, PSTN, or FTTC-only metrics in the core dashboard. Gigabit-capable coverage should not be treated as FTTP unless the source explicitly identifies FTTP/full fibre.

The Spring 2026 Ofcom postcode files inspected in the fixed broadband ZIP include speed and gigabit fields, but not an explicit full-fibre field. For that reason, real FTTP mapping currently uses local-authority geography rather than postcode districts.
