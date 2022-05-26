# -*- coding: utf-8 -*-

import torch
import torch.nn.functional as F

class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden1, n_hidden2, n_hidden3, n_hidden4, n_output):
        super(Net, self).__init__()
        self.hidden1 = torch.nn.Linear(n_feature, n_hidden1)
        self.hidden2 = torch.nn.Linear(n_hidden1, n_hidden2)
        self.hidden3 = torch.nn.Linear(n_hidden2, n_hidden3)
        self.hidden4 = torch.nn.Linear(n_hidden3, n_hidden4)
        self.output = torch.nn.Linear(n_hidden4, n_output)

    def forward(self, x):
        # a function that implements the forward propagation of the signal
        # observe the relu function applied on the output of the hidden layer
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))     
        x = F.relu(self.hidden3(x))
        x = F.relu(self.hidden4(x))
        x = self.output(x)             
        return x
