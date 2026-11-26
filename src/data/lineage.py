import hashlib, json, subprocess, datetime
from pathlib import Path
def file_hash(path):
    h=hashlib.sha256(); h.update(Path(path).read_bytes()); return h.hexdigest()
def make_lineage(source, dataset_version, model_version, config):
    try: git=subprocess.check_output(['git','rev-parse','HEAD'],stderr=subprocess.DEVNULL,text=True).strip()
    except Exception: git='uncommitted'
    return {'source':source,'source_url':'https://www.penguinmap.org/','access_date':datetime.date.today().isoformat(),'dataset_version':dataset_version,'file_hash':file_hash(source) if Path(source).exists() else None,'transformation':'validation -> feature engineering -> model inference','model_version':model_version,'configuration':config,'git_commit':git,'prediction_version':datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
def save(lineage,path='artifacts/lineage.json'): Path(path).write_text(json.dumps(lineage,indent=2))
