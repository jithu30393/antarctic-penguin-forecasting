import numpy as np
def metrics(y,p,lo=None,hi=None):
    y=np.asarray(y);p=np.asarray(p); e=y-p; mae=float(np.mean(np.abs(e))); rmse=float(np.sqrt(np.mean(e**2))); smape=float(np.mean(2*np.abs(e)/(np.abs(y)+np.abs(p)+1e-9))*100); r2=float(1-np.sum(e**2)/(np.sum((y-y.mean())**2)+1e-9)); d={'mae':mae,'rmse':rmse,'smape':smape,'r2':r2}
    if lo is not None: d['interval_coverage']=float(np.mean((y>=lo)&(y<=hi))*100); d['mean_interval_width']=float(np.mean(np.asarray(hi)-np.asarray(lo)))
    return d
def normalized_score(mae,baseline_mae): return float(np.clip(100*(1-mae/(baseline_mae+1e-9)),0,100))
