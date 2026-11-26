import numpy as np, pandas as pd, torch
from .stgnn import STGNN
FEATURES=['population_count','sea_surface_temperature','sea_ice_concentration','air_temperature','chlorophyll_concentration','ocean_condition','time_delta','observation_mask']
def prepare_latest(df):
    rows=[]
    for cid,g in df.sort_values('survey_date').groupby('colony_id'):
        r=g.iloc[-1].copy(); r['observation_mask']=1; rows.append(r)
    return pd.DataFrame(rows)
def build_tensor(df):
    vals=[]
    for cid,g in df.sort_values('survey_date').groupby('colony_id'):
        gg=g.tail(4); a=gg[FEATURES].astype(float).to_numpy();
        if len(a)<4: a=np.vstack([np.repeat(a[:1],4-len(a),axis=0),a])
        vals.append(a)
    return np.array(vals,dtype='float32')
def predict(model,X,adj):
    with torch.no_grad(): return model(torch.tensor(X),torch.tensor(adj)).numpy()
