# Public Data Sources

## FTTP Coverage

Primary candidate: Ofcom Connected Nations fixed broadband coverage and full-fibre datasets.

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

## Version 1 Rule

Do not include copper, ADSL, PSTN, or FTTC-only metrics in the core dashboard. Gigabit-capable coverage should not be treated as FTTP unless the source explicitly identifies FTTP/full fibre.
