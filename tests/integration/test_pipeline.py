from src.pipeline import run
def test_pipeline():
 s=run('configs/demo.yaml'); assert s['forecast_count']==6; assert s['lineage_coverage']==100.0
