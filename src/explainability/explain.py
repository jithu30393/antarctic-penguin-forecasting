import numpy as np
FEATURES=['recent population','sea surface temperature','sea ice concentration','air temperature','chlorophyll concentration','ocean condition','time since previous survey','observation availability']
def permutation_importance(model_predict,X,adj,repeats=3):
    base=np.asarray(model_predict(X,adj))[:,0]; out=[]; rng=np.random.default_rng(42)
    for j,f in enumerate(FEATURES):
        scores=[]
        for _ in range(repeats):
            z=X.copy(); z[:,:,j]=rng.permutation(z[:,:,j].reshape(-1)).reshape(z[:,:,j].shape); scores.append(float(np.mean(np.abs(base-np.asarray(model_predict(z,adj))[:,0]))))
        out.append({'factor':f,'importance':float(np.mean(scores))})
    return sorted(out,key=lambda x:x['importance'],reverse=True)
