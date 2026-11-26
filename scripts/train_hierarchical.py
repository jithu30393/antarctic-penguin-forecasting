import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd, json
from src.models.hierarchical_model import HierarchicalPopulationModel
df=pd.read_csv('data/fixtures/penguin_observations.csv'); m=HierarchicalPopulationModel().fit(df); json.dump({'global_mean':m.global_mean,'residual_std':m.resid_std},open('models/hierarchical_summary.json','w'),indent=2); print('Hierarchical model fitted')
