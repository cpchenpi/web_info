'''
Author: Ashton
Date: 2023-11-05 11:07:06
LastEditors: Ashton
LastEditTime: 2023-11-09 12:19:54
Description: 
'''
from Data_process import data_split
import Model
import Evaluate
from tqdm import tqdm
import torch
from torch.utils.data import DataLoader


def fit(path, genre, user_num, item_num, lr = 0.005, dropout = 0, size = 2048, factor = 20, num_epochs = 20):
    train, test, mean = data_split(path, user_num, genre)
    if genre == 'book':
        train_set = Model.BookDataset(train)
    else:
        train_set = Model.MovieDataset(train)
    train_loader = DataLoader(train_set, batch_size = size, shuffle = True)
    model = Model.MF(user_num, item_num, mean, factor, dropout)
    optimizer = torch.optim.Adam(model.parameters(), lr = lr)
    total_loss = 0

    for epoch in range(num_epochs):
        model.train()
        n = 0
        for user, item, rank in tqdm(train_loader):
            predict = model(user, item)
            loss = Evaluate.loss(predict, rank)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            n += 1
        model.eval()

        test_NDCG = Evaluate.metrics(model, test)
        tqdm.write(f'Epoch {epoch}: test ndcg is {test_NDCG}')
        if not epoch:
            Evaluate.rank_out(model, test, genre)
    

print('Book')
fit('data/book_score_clean.csv', user_num = 4419, item_num = 1200, genre = 'book')
print('Movie')
fit('data/movie_score_clean.csv', user_num = 1023, item_num = 1200, genre = 'movie')