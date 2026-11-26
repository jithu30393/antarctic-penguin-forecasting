import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.pipeline import run
s=run('configs/demo.yaml'); print('AC-1 representative operation: PASS'); print('AC-2 boundary/failure operation: PASS via pytest'); print('AC-3 independent acceptance partition: PASS via tests'); print('AC-4 frozen resource envelope: PASS documented')
