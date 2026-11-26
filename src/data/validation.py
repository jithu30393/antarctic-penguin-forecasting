import pandas as pd, numpy as np
REQUIRED=['colony_id','species','latitude','longitude','survey_date','population_count','survey_method','survey_quality','sea_surface_temperature','sea_ice_concentration','air_temperature','chlorophyll_concentration','ocean_condition','source_id','observation_uncertainty']
def validate(df):
    errors=[]
    miss=[c for c in REQUIRED if c not in df.columns]
    if miss: errors.append(f'missing columns: {miss}'); return {'valid':False,'errors':errors,'rows':0}
    if pd.to_datetime(df.survey_date,errors='coerce').isna().any(): errors.append('invalid dates')
    if (df.population_count<0).any(): errors.append('negative population')
    if not df.latitude.between(-90,90).all() or not df.longitude.between(-180,180).all(): errors.append('invalid coordinates')
    if df.colony_id.duplicated().any() and df[['colony_id','survey_date']].duplicated().any(): errors.append('duplicate observation')
    for c in ['sea_ice_concentration']:
        if not df[c].between(0,1).all(): errors.append(f'{c} out of range')
    return {'valid':not errors,'errors':errors,'rows':len(df)}
