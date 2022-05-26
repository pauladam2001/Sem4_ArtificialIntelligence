import torch
import numpy as np

def f(x1, x2):
    return np.sin(x1 + x2/np.pi)

def create_dataset(n = 1000, l1 = -10, r1 = 10, l2 = -10, r2 = 10, file='dataset.dat'):
    points = np.random.uniform(low=[l1, l2], high=[r1, r2], size=(n, 2))
    data = torch.tensor([(p[0], p[1], f(p[0], p[1])) for p in points])
    torch.save(data, file)

create_dataset()