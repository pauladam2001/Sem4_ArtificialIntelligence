import torch
import torch.nn.functional as F
import myModel
import numpy as np

def f(x1, x2):
    return np.sin(x1 + x2/np.pi)

filepath = "myNet.pt"
nn = myModel.Net(n_feature=2, n_hidden1=128, n_hidden2=64, n_hidden3=32, n_hidden4=16, n_output=1).float()

nn.load_state_dict(torch.load(filepath))
nn.eval()

x1 = float(input("x1 = "))
x2 = float(input("x2 = "))
x = torch.tensor([x1, x2])
print(f"Predicted: {nn(x).tolist()}; Real value: {f(x1, x2)}")