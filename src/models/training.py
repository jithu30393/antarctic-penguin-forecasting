from pathlib import Path
import torch, numpy as np
from .stgnn import STGNN
def train_model(X,y,adj,epochs=20,lr=.01,hidden=32,seed=42,out='models/stgnn.pt'):
    torch.manual_seed(seed); m=STGNN(X.shape[-1],hidden); opt=torch.optim.Adam(m.parameters(),lr=lr); lossfn=torch.nn.MSELoss()
    X=torch.tensor(X,dtype=torch.float32); y=torch.tensor(y,dtype=torch.float32); adj=torch.tensor(adj,dtype=torch.float32)
    for _ in range(epochs): opt.zero_grad(); pred=m(X,adj)[:,0]; loss=lossfn(pred,y); loss.backward(); opt.step()
    Path(out).parent.mkdir(exist_ok=True); torch.save(m.state_dict(),out); return m,float(loss.detach())
