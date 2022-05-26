
import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

import myModel

loss_function = torch.nn.MSELoss()
nn = myModel.Net(n_feature=2, n_hidden1=128, n_hidden2=64, n_hidden3=32, n_hidden4=16, n_output=1).float()
optimizer_batch = torch.optim.SGD(nn.parameters(), lr=0.005)
data = torch.load('dataset.dat')

loss_list = []
avg_loss_list = []

batch_size = 32
n_batches = len(data) // batch_size

data_points = torch.tensor([(x[0], x[1]) for x in data])
data_values = torch.unsqueeze(torch.tensor([x[2] for x in data]), dim = 1)

split_data_points = torch.split(data_points, batch_size)
split_data_values = torch.split(data_values, batch_size)


for epoch in range(1500):
  for batch in range(n_batches):
    batch_points = split_data_points[batch].float()
    batch_values = split_data_values[batch].float()

    pred = nn(batch_points)
    loss = loss_function(pred, batch_values)
    loss_list.append(loss.item())
    avg_loss_list.append(loss.item()/batch_size)

    optimizer_batch.zero_grad()
    
    loss.backward()

    optimizer_batch.step()
  
  if epoch % 100 == 99:
    y_pred = nn(data_points.float())
    loss = loss_function(y_pred, data_values)
    print(f"Epoch {epoch+1}: loss {loss}")

plt.plot(loss_list)
plt.savefig("loss.png")

plt.plot(avg_loss_list)
plt.savefig("avg_loss.png")

torch.save(nn.state_dict(), 'myNet.pt')