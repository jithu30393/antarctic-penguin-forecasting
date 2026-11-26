import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.pipeline import run
run('configs/full.yaml'); print('Full ST-GNN training complete')
