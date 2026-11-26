# System architecture
1. Ingestion -> validation/quarantine. 2. Feature engineering retains `time_delta`, `observation_mask`, survey method and quality. 3. Graph builder creates k-nearest spatial edges. 4. Baseline and hierarchical models establish references. 5. ST-GNN combines GRU temporal encoding and graph message passing. 6. Residual calibration produces intervals whose width increases with sparse evidence, long gaps and poor quality. 7. Explainability and risk are attached to predictions. 8. FastAPI exposes the system and React renders the dashboard.

Apple Silicon uses CPU by default in the lightweight implementation; the training module is pure PyTorch and can be extended to MPS. PyTorch Geometric is intentionally not required.
