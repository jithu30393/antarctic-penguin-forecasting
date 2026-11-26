from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd, json, os
from pathlib import Path
from src.data.validation import validate
from src.pipeline import run
app=FastAPI(title='Penguin ST-GNN API',version='1.0.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
DATA='data/fixtures/penguin_observations.csv'
class ForecastRequest(BaseModel): colony_id:str|None=None
class IngestRequest(BaseModel): records:list[dict]
@app.get('/health')
def health(): return {'status':'ok','model':'stgnn-v1.0.0'}
@app.get('/api/system-status')
def status(): return {'api':'UP','data':Path(DATA).exists(),'model':Path('models/stgnn.pt').exists()}
@app.get('/api/colonies')
def colonies():
 d=pd.read_csv(DATA); return d[['colony_id','species','latitude','longitude']].drop_duplicates().to_dict('records')
@app.get('/api/colonies/{colony_id}')
def colony(colony_id:str):
 d=pd.read_csv(DATA); x=d[d.colony_id==colony_id];
 if x.empty: raise HTTPException(404,'Colony not found')
 return {'colony_id':colony_id,'species':x.species.iloc[0],'latitude':x.latitude.iloc[0],'longitude':x.longitude.iloc[0],'history':x.sort_values('survey_date').to_dict('records')}
@app.post('/api/forecast')
def forecast(req:ForecastRequest):
 p=Path('artifacts/forecasts.json');
 if not p.exists(): run('configs/demo.yaml')
 data=json.loads(p.read_text())
 if req.colony_id is None: return data
 for x in data:
  if x['colony_id']==req.colony_id: return x
 raise HTTPException(404,'Forecast not found')
@app.get('/api/forecast')
def list_forecasts():
    p=Path('artifacts/forecasts.json')
    if not p.exists(): run('configs/demo.yaml')
    return json.loads(p.read_text())

@app.get('/api/forecast/{colony_id}')
def get_forecast(colony_id): return forecast(ForecastRequest(colony_id=colony_id))
@app.post('/api/train')
def train(): return run('configs/demo.yaml')
@app.get('/api/metrics')
def metrics():
 p=Path('metrics/latest_run.json'); return json.loads(p.read_text()) if p.exists() else {}
@app.get('/api/explanations/{colony_id}')
def explanations(colony_id):
 p=Path('artifacts/explanations.json')
 if not p.exists(): run('configs/demo.yaml')
 return {'colony_id':colony_id,'method':'model-derived feature ablation','factors':json.loads(p.read_text())['global']}
@app.get('/api/lineage/{prediction_id}')
def lineage(prediction_id):
 p=Path('artifacts/lineage.json'); return json.loads(p.read_text()) if p.exists() else {'prediction_id':prediction_id,'status':'not_generated'}
@app.get('/api/validation')
def validation(): return validate(pd.read_csv(DATA))
@app.post('/api/data/validate')
def data_validate(req:IngestRequest): return validate(pd.DataFrame(req.records))
@app.post('/api/data/ingest')
def ingest(req:IngestRequest):
 df=pd.DataFrame(req.records); v=validate(df)
 if not v['valid']: raise HTTPException(422,v)
 df.to_csv(DATA,index=False); return {'status':'accepted','rows':len(df)}
