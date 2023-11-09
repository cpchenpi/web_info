'''
Author: Ashton
Date: 2023-11-05 00:07:49
LastEditors: Ashton
LastEditTime: 2023-11-09 12:48:28
Description: 
'''
import torch
from math import log2
import numpy as np
import pandas as pd


def loss(predict, target):
    return torch.sum((target - predict)**2)

def metrics(model, evaluate):
    NDCG = 0
    n = 0
    for user_id, item_dic in enumerate(evaluate):
        DCG = 0
        IDCG = 0
        item_key = list(item_dic.keys())
        user = torch.full((len(item_key), ), user_id, dtype = torch.int64)
        item = torch.tensor(item_key, dtype = torch.int64)
        predict = model(user, item).detach().numpy()[: , np.newaxis]
        temp = np.array(list(item_dic.values()))[: , np.newaxis]
        ranks = np.concatenate([predict, temp], axis = 1).tolist()
        ranks.sort(reverse = True)
        for i, (tmp, rank) in enumerate(ranks):
            DCG += (2**rank - 1) / log2(i + 2)
        item_value = list(item_dic.values())
        item_value.sort(reverse = True)
        for i, rank in enumerate(item_value):
            IDCG += (2**rank - 1) / log2(i + 2)
        if IDCG:
            NDCG += DCG / IDCG
            n += 1
    return NDCG / n if n else 0

def rank_out(model, test, genre):
    path = 'data/' + genre + '_rank.csv'
    result = []
    col = ['user', 'rank', 'rank_predict']
    for user_id, item_dic in enumerate(test):
        temp = dict()
        temp['user'] = user_id
        temp['rank'] = []
        temp['rank_predict'] = []

        item_key = list(item_dic.keys())
        user = torch.full((len(item_key), ), user_id, dtype = torch.int64)
        item = torch.tensor(item_key, dtype = torch.int64)
        predict = model(user, item).detach().numpy()[: , np.newaxis]

        item_key = np.array(item_key)[: , np.newaxis]
        score = np.array(list(item_dic.values()))[: , np.newaxis]
        rank = np.concatenate([score, item_key], axis = 1).tolist()
        rank.sort(reverse = True)
        rank_predict = np.concatenate([predict, item_key, score], axis = 1).tolist()
        rank_predict.sort(reverse = True)
        for sc, key in rank:
            temp['rank'].append(f'{int(key)} {int(sc)}')
        for predict, key, sc in rank_predict:
            temp['rank_predict'].append(f'{int(key)} {int(sc)}')
        result.append(temp)
    pd.DataFrame(result, columns = col).to_csv(path, index = False)