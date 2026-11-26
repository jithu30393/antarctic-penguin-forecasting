import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
"""Public-data hook. Offline-safe: retains the synthetic fixture unless a verified public export is supplied."""
from src.data.generate_fixture import generate
print('No network dependency required; generating offline fixture.')
generate()
