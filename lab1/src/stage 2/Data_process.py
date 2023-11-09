'''
Author: Ashton
Date: 2023-11-04 23:36:10
LastEditors: Ashton
LastEditTime: 2023-11-08 22:28:01
Description: 
'''
import pandas as pd
import numpy as np
import csv


def data_clean(genre):
    data_path = 'data/' + genre + '_score.csv'
    target_path = 'data/' + genre + '_score_clean.csv'
    user_idx = dict()
    item_idx = dict()
    data_clean = []
    with open(data_path, mode = 'r') as file:
        data = csv.reader(file)
        info = next(data)
        data_clean.append(info)
        user_id = 0
        item_id = 0
        for line in data:
            temp = line
            if line[0] not in user_idx.keys():
                user_idx[line[0]] = user_id
                user_id += 1
            if line[1] not in item_idx.keys():
                item_idx[line[1]] = item_id
                item_id += 1
            temp[0] = user_idx[temp[0]]
            temp[1] = item_idx[temp[1]]
            data_clean.append(temp)

    with open(target_path, mode = 'w') as file:
        target = csv.writer(file)
        for line in data_clean:
            target.writerow(line)
    
    return user_id, item_id


def data_split(path, user_num, genre):
    data = pd.read_csv(path)
    type = genre.capitalize()
    data.loc[:, ['User', type, 'Rate']].reset_index()
    n = data.shape[0]
    rate = np.array(list(data.loc[:, 'Rate']))
    mean = np.mean(rate)

    train = data.loc[: int(0.5 * n) - 1]
    test = data.loc[int(0.5 * n): ]
    test_dic = [dict() for i in range(user_num)]
    for user in range(user_num):
        items = test.loc[test['User'] == user]
        for i, item in items.iterrows():
            test_dic[user][int(item[type])] = int(item['Rate'])
    return train, test_dic, mean


if __name__ == 'main':
    print(data_clean('book'))
    print(data_clean('movie'))