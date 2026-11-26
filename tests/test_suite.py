import pandas as pd, numpy as np, json
from src.data.generate_fixture import generate
from src.data.validation import validate
from src.models.baseline import persistence,exponential_smoothing,evaluate
from src.models.graph_builder import build_edges,haversine
from src.models.hierarchical_model import HierarchicalPopulationModel
from src.uncertainty.calibration import conformal_interval,multiplier
from src.validation.metrics import metrics,normalized_score

def df(): return pd.read_csv('data/fixtures/penguin_observations.csv',parse_dates=['survey_date'])
def test_01_fixture_exists(): assert len(df())>50
def test_02_schema(): assert validate(df())['valid']
def test_03_dates(): assert pd.api.types.is_datetime64_any_dtype(df().survey_date)
def test_04_population_nonnegative(): assert (df().population_count>=0).all()
def test_05_sst_numeric(): assert df().sea_surface_temperature.dtype.kind in 'fc'
def test_06_ice_range(): assert df().sea_ice_concentration.between(0,1).all()
def test_07_colony_count(): assert df().colony_id.nunique()==6
def test_08_irregular_gaps(): assert df().groupby('colony_id').time_delta.max().max()>180
def test_09_persistence(): assert len(persistence(pd.Series([1,2]),3))==3
def test_10_exp_smooth(): assert len(exponential_smoothing(pd.Series([1,2,3,4,5]),2))==2
def test_11_baseline_metrics(): assert len(evaluate(df()))>0
def test_12_graph_nodes(): c,e=build_edges(df()); assert len(c)==6
def test_13_graph_edges(): c,e=build_edges(df()); assert len(e)>=6
def test_14_haversine(): assert haversine((0,0),(0,1))>100
def test_15_hierarchical_fit(): m=HierarchicalPopulationModel().fit(df()); assert m.global_mean>0
def test_16_hierarchical_predict(): m=HierarchicalPopulationModel().fit(df()); assert len(m.predict(df().head(5)))==5
def test_17_uncertainty_bounds(): lo,hi,q=conformal_interval(100,[1,2,3,4]); assert lo<100<hi
def test_18_sparse_multiplier(): assert multiplier(1,500,'low')>multiplier(10,10,'high')
def test_19_metrics(): x=metrics([1,2,3],[1,2,4]); assert 'mae' in x and x['mae']>0
def test_20_coverage(): x=metrics([1,2],[1,2],[0,1],[2,3]); assert x['interval_coverage']==100
def test_21_score(): assert abs(normalized_score(5,10)-50)<1e-6
def test_22_duplicate_detection():
 d=df().head(2); d=pd.concat([d,d.iloc[[0]]]); assert not validate(d)['valid']
def test_23_invalid_date(): d=df().head(2); d.loc[d.index[0],'survey_date']='bad'; assert not validate(d)['valid']
def test_24_negative_population(): d=df().head(2); d.loc[d.index[0],'population_count']=-1; assert not validate(d)['valid']
def test_25_bad_ice(): d=df().head(2); d.loc[d.index[0],'sea_ice_concentration']=2; assert not validate(d)['valid']
def test_26_missing_column(): d=df().drop(columns=['species']); assert not validate(d)['valid']
def test_27_latitude(): d=df().head(2); d.loc[d.index[0],'latitude']=100; assert not validate(d)['valid']
def test_28_observation_mask(): assert set(df().observation_mask.unique())=={1}
def test_29_source_ids(): assert df().source_id.str.startswith('FIXTURE-').all()
def test_30_uncertainty_positive(): assert (df().observation_uncertainty>0).all()
def test_31_species_present(): assert set(df().species)=={'Adelie','Chinstrap','Gentoo'}
def test_32_methods_present(): assert df().survey_method.nunique()>=3
def test_33_quality_present(): assert df().survey_quality.nunique()==3
def test_34_time_delta_nonnegative(): assert (df().time_delta>=0).all()
def test_35_sorted_dates():
 d=df(); assert all(g.survey_date.is_monotonic_increasing for _,g in d.groupby('colony_id'))
