import numpy as np
def conformal_interval(pred,residuals,alpha=.05,uncertainty_multiplier=1.0):
    q=float(np.quantile(np.abs(residuals),1-alpha)) if len(residuals) else max(1,float(abs(pred))*0.1)
    q*=uncertainty_multiplier; return max(0,pred-q),pred+q,q

def multiplier(n_obs,time_delta,quality):
    m=1.0+max(0,5-n_obs)*.18+max(0,time_delta-365)/365*.25+({'high':0,'medium':.12,'low':.25}.get(quality,.3)); return m
