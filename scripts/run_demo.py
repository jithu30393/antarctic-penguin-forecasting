import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data.generate_fixture import generate
generate(); from src.pipeline import run
s=run('configs/demo.yaml'); print(f"Demo complete: {s['forecast_count']} forecasts; lineage={s['lineage_coverage']}%")
