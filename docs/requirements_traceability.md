# Requirements traceability
| Requirement | Source | Implementation | Test | Evidence |
|---|---|---|---|---|
| FR-1 | SRS | `src/data` | validation tests | API `/api/data/ingest` |
| FR-2 | SRS | `src/models/baseline.py` | baseline tests | `metrics/baseline_metrics.csv` |
| FR-3/5 | SRS | `hierarchical_model.py` | model tests | `models/hierarchical_summary.json` |
| FR-4 | SRS | `uncertainty/calibration.py` | interval tests | forecast bounds |
| FR-6 | SRS | `pipeline.py` | integration | dashboard/API |
| FR-7 | SRS | validation/API | negative tests | pytest results |
