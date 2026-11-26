import torch
from torch import nn
class GraphConv(nn.Module):
    def __init__(self,dim): super().__init__(); self.lin=nn.Linear(dim,dim)
    def forward(self,x,adj):
        deg=adj.sum(-1,keepdim=True).clamp_min(1); agg=adj@x/deg; return torch.relu(self.lin(agg+x))
class STGNN(nn.Module):
    def __init__(self,in_dim,hidden=32):
        super().__init__(); self.temporal=nn.GRU(in_dim,hidden,batch_first=True); self.gconv=GraphConv(hidden); self.head=nn.Sequential(nn.Linear(hidden,hidden),nn.ReLU(),nn.Linear(hidden,2))
    def forward(self,x,adj):
        h,_=self.temporal(x); h=h[:,-1]; h=self.gconv(h,adj); return self.head(h)
