from pathlib import Path
import numpy as np, pandas as pd

def generate(path='data/fixtures/penguin_observations.csv', seed=42):
    rng=np.random.default_rng(seed); rows=[]
    colonies=[('COLONY_001','Adelie',-64.2,-56.7),('COLONY_002','Adelie',-64.5,-56.1),('COLONY_003','Chinstrap',-62.1,-58.4),('COLONY_004','Chinstrap',-62.3,-58.0),('COLONY_005','Gentoo',-64.8,-62.3),('COLONY_006','Gentoo',-65.0,-62.0)]
    dates=pd.date_range('2018-01-01','2025-01-01',freq='180D')
    base={c[0]:9000+i*1200 for i,c in enumerate(colonies)}
    for i,(cid,species,lat,lon) in enumerate(colonies):
        for d in dates:
            if rng.random() < (0.18 if cid in ['COLONY_002','COLONY_006'] else 0.05): continue
            t=(d.year-2018)+(d.dayofyear/365)
            sst=-1.2+0.10*t+0.25*np.sin(t)+rng.normal(0,.08)
            ice=0.75-0.035*t+0.05*np.cos(t)+rng.normal(0,.03); ice=float(np.clip(ice,0.05,.95))
            air=-10+0.7*np.sin(t)+0.2*t+rng.normal(0,.4)
            chl=1.8+0.15*np.cos(t/2)+rng.normal(0,.1)
            ocean=0.4*sst-0.5*ice+0.2*chl
            method=rng.choice(['aerial','ground','drone'],p=[.45,.35,.20])
            quality=rng.choice(['high','medium','low'],p=[.6,.3,.1])
            trend=base[cid]*(1+0.012*t)+180*ice-120*sst+rng.normal(0,180)
            count=max(100,trend)
            rows.append([cid,species,lat,lon,d.date(),round(count),method,quality,round(sst,4),round(ice,4),round(air,4),round(chl,4),round(ocean,4),f'FIXTURE-{d.year}',round(max(50,count*(.03 if quality=='high' else .08)),2)])
    df=pd.DataFrame(rows,columns=['colony_id','species','latitude','longitude','survey_date','population_count','survey_method','survey_quality','sea_surface_temperature','sea_ice_concentration','air_temperature','chlorophyll_concentration','ocean_condition','source_id','observation_uncertainty'])
    df['survey_date']=pd.to_datetime(df.survey_date); df=df.sort_values(['colony_id','survey_date']); df['time_delta']=df.groupby('colony_id').survey_date.diff().dt.days.fillna(0).astype(int); df['observation_mask']=1
    Path(path).parent.mkdir(parents=True,exist_ok=True); df.to_csv(path,index=False); return df
if __name__=='__main__': generate()
