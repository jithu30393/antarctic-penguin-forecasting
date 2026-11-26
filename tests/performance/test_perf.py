import time
from src.pipeline import run
def test_pipeline_smoke_latency():
 t=time.perf_counter(); run('configs/demo.yaml'); assert time.perf_counter()-t<60
