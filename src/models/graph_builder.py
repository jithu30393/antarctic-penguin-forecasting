import numpy as np, pandas as pd
def haversine(a,b):
    R=6371; lat1,lon1=np.radians(a); lat2,lon2=np.radians(b); dlat=lat2-lat1;dlon=lon2-lon1
    x=np.sin(dlat/2)**2+np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2; return 2*R*np.arcsin(np.sqrt(x))
def build_edges(df,k=3):
    c=df[['colony_id','latitude','longitude']].drop_duplicates().reset_index(drop=True); edges=[]
    for i,r in c.iterrows():
        ds=[(j,haversine((r.latitude,r.longitude),(x.latitude,x.longitude))) for j,x in c.iterrows() if j!=i]
        for j,_ in sorted(ds,key=lambda z:z[1])[:min(k,len(ds))]: edges.append((i,j))
    return c,edges
