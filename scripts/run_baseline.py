import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
from src.models.baseline import evaluate
x=pd.read_csv('data/fixtures/penguin_observations.csv',parse_dates=['survey_date']); print(evaluate(x).to_string(index=False))
