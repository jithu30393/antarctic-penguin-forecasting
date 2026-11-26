import sqlite3
from pathlib import Path
def init_db(path="artifacts/penguin.db"):
 Path(path).parent.mkdir(parents=True,exist_ok=True)
 con=sqlite3.connect(path); con.executescript("CREATE TABLE IF NOT EXISTS forecasts(colony_id TEXT, forecast REAL, lower_bound REAL, upper_bound REAL, confidence REAL, risk_level TEXT); CREATE TABLE IF NOT EXISTS lineage(prediction_version TEXT, payload TEXT);"); con.commit(); con.close()
