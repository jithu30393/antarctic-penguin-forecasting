from pathlib import Path
def test_acceptance_artifacts(): assert Path('docs/SRS.md').exists() and Path('docs/architecture.md').exists()
def test_frozen_envelope(): assert Path('configs/demo.yaml').exists()
def test_lineage_artifact(): assert Path('src/data/lineage.py').exists()
