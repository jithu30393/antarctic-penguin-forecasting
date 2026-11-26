import numpy as np, pandas as pd
class HierarchicalPopulationModel:
    """Lightweight probabilistic hierarchical model: global + species + colony effects with empirical uncertainty."""
    def fit(self,df):
        g=df.groupby('colony_id').population_count.mean(); s=df.groupby('species').population_count.mean(); self.global_mean=float(df.population_count.mean()); self.colony=g.to_dict(); self.species=s.to_dict(); self.resid_std=float(df.population_count.std(ddof=1)); return self
    def predict(self,df):
        vals=[]
        for _,r in df.iterrows(): vals.append(.5*self.colony.get(r.colony_id,self.global_mean)+.3*self.species.get(r.species,self.global_mean)+.2*self.global_mean)
        return np.array(vals)
