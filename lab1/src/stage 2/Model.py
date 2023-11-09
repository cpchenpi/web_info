'''
Author: Ashton
Date: 2023-11-04 23:16:43
LastEditors: Ashton
LastEditTime: 2023-11-06 14:47:43
Description: 
'''
import torch
from torch import nn
from torch.utils.data import Dataset


class BookDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data.loc[index, 'User'], self.data.loc[index, 'Book'], self.data.loc[index, 'Rate']


class MovieDataset(Dataset):
    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data.loc[index, 'User'], self.data.loc[index, 'Movie'], self.data.loc[index, 'Rate']


class MF(nn.Module):
    def __init__(self, user_num, item_num, mean, size, dropout):
        super(MF, self).__init__()
        self.user_ebds = nn.Embedding(user_num, size)
        self.item_ebds = nn.Embedding(item_num, size)
        self.user_bias = nn.Embedding(user_num, 1)
        self.item_bias = nn.Embedding(item_num, 1)
        self.mean = nn.Parameter(torch.FloatTensor([mean]), False)

        self.dropout = nn.Dropout(dropout)

    def forward(self, user_id, item_id):
        user_ebd = self.user_ebds(user_id)
        item_ebd = self.item_ebds(item_id)
        user_b = self.user_bias(user_id).squeeze()
        item_b = self.item_bias(item_id).squeeze()
        return self.dropout((user_ebd * item_ebd).sum(1) + user_b + item_b + self.mean)
    
    