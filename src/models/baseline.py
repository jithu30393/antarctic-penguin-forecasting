import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def persistence(train,horizon): return np.repeat(float(train.iloc[-1]),horizon)
def exponential_smoothing(train,horizon):
    try: return ExponentialSmoothing(train.astype(float),trend='add',damped_trend=True).fit(optimized=True).forecast(horizon).to_numpy()
    except Exception: return persistence(train,horizon)
def evaluate(df):
    rows=[]
    for cid,g in df.sort_values('survey_date').groupby('colony_id'):
        if len(g)<5: continue
        cut=max(3,int(len(g)*.8)); tr=g.population_count.iloc[:cut]; te=g.population_count.iloc[cut:]
        for name,fn in [('persistence',persistence),('exponential_smoothing',exponential_smoothing)]:
            pred=fn(tr,len(te)); err=te.to_numpy()-pred
            rows.append({'colony_id':cid,'model':name,'mae':float(np.mean(np.abs(err))),'rmse':float(np.sqrt(np.mean(err**2)))})
    return pd.DataFrame(rows)
