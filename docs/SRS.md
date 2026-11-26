# Software Requirements Specification
## Scope
Forecast Antarctic penguin colony population from irregular survey records while combining temporal, spatial and climate information and exposing uncertainty, explanations and lineage.
## Users
Researcher/conservation analyst, reviewer/operator, administrator/developer.
## Functional requirements
FR-1 ingest public/reference records and fixture data; FR-2 reproducible baselines; FR-3 hierarchical colony/species/time sharing; FR-4 calibrated intervals; FR-5 probabilistic hierarchical functionality; FR-6 complete forecasting result; FR-7 safe degraded response.
## Non-functional
Performance measured by tests; invalid data is rejected; schema, time semantics, units and lineage validated; configuration and tests are versioned; health/logging/status are exposed.
## Inputs/outputs
Input fields are defined in `docs/data_dictionary.md`. Forecast output contains point forecast, lower/upper bounds, confidence, risk and evidence counts.
## Boundary
The system owns data validation, modelling, inference, API and dashboard. External public data services are optional dependencies.
## Constraints
Sparse irregular Antarctic surveys, offline operation, Apple Silicon compatibility, no mandatory GPU or physical hardware.
## Acceptance
Held-out/independent acceptance partitions, adversarial conditions and frozen resource envelope are required; actual KPI values are reported without fabrication.
