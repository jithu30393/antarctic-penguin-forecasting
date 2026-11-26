# Model design
## Baselines
Persistence and Holt exponential smoothing share the same colony-wise chronological split.
## Hierarchical model
Global, species and colony effects are estimated with partial-pooling weighted effects; empirical residual dispersion supplies probabilistic uncertainty. This lightweight equivalent keeps the demo offline and avoids mandatory MCMC runtime.
## ST-GNN
A GRU encodes sequences; normalized graph aggregation propagates information between geographically close colonies; a two-value head emits population forecast and uncertainty scale. Training is deterministic under a fixed seed.
## Observation process
Survey method, quality, observation uncertainty and missingness are retained as explicit fields rather than silently pooling methods.
