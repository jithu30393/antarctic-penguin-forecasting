# Build Status

Date: 2026-09-21

- Python runtime used for verification: 3.13.x container runtime (project targets Python 3.11+).
- Node runtime available: 22.16.0 (project targets Node 18+).
- Fixture dataset: generated successfully; synthetic/offline, not MAPPPD.
- Demo pipeline: PASS — 6 colony forecasts generated.
- Automated tests: PASS — 51 passed, 0 failed.
- Negative tests: PASS — 5 passed.
- Acceptance runner: PASS — AC-1 through AC-4 reported.
- API checks: PASS — health, colonies, validation, forecast, explanations and lineage endpoints returned 200; missing colony returns 404.
- Model: PASS — pure-PyTorch ST-GNN training/inference completed in demo mode; model artifact created.
- Hierarchical model: PASS — fitted and summary artifact generated.
- Baselines: PASS — persistence and Holt exponential smoothing evaluated.
- Lineage: PASS — 100% of generated forecast outputs carry run-level lineage metadata.
- Frontend dependency/build: NOT VERIFIED IN THIS OFFLINE BUILD ENVIRONMENT because `npm install` could not complete without network access. The React/Vite source and package manifest are included; run `cd frontend && npm install && npm run build` on the target Mac with internet access.
- Docker: configuration files included; image build not executed in this offline environment.
- KPI targets: NOT pre-claimed. Actual metric values are generated under `metrics/`; target/actual/pass-fail comparison should be made from the run artifacts.
- Known limitations: fixture is synthetic; public-data acquisition remains an optional verified-data replacement; the hierarchical implementation is a lightweight partial-pooling probabilistic equivalent rather than mandatory MCMC; frontend build requires network/package cache.
