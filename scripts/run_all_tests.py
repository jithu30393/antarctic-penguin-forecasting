import sys; from pathlib import Path; sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import subprocess,sys
r=subprocess.run([sys.executable,'-m','pytest','-q']); sys.exit(r.returncode)
