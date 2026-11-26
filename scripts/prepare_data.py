import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.data.generate_fixture import generate
generate('data/processed/penguin_observations.csv'); print('Prepared data/processed/penguin_observations.csv')
