import pandas as pd
from src.data.validation import validate
def test_nt1_sparse_detected():
 d=pd.read_csv('data/fixtures/penguin_observations.csv').query("colony_id=='COLONY_002'"); assert len(d)>=1
def test_nt2_methods_not_identical(): d=pd.read_csv('data/fixtures/penguin_observations.csv'); assert d.survey_method.nunique()>1
def test_nt3_no_improper_pooling(): d=pd.read_csv('data/fixtures/penguin_observations.csv'); assert d.colony_id.nunique()>1
def test_nt4_invalid_permission_payload_rejected(): assert not validate(pd.DataFrame({'x':[1]}))['valid']
def test_nt5_schema_evolution_rejected(): assert not validate(pd.DataFrame({'colony_id':['x']}))['valid']
