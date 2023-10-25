'''
Author: Ashton
Date: 2023-10-25 17:07:09
LastEditors: Ashton
LastEditTime: 2023-10-25 17:08:10
Description: 
'''
import requests
import os

with open('lab1/Book_id.csv') as file:
    flag = True
    str = file.readlines()
    for i in range(len(str)):
        id = str[i][:-1]
        path = 'lab1/books/' + id
        if os.path.exists(path):
            continue
        flag = False
        url = 'https://book.douban.com/subject/' + id
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.115'}
        responce = requests.get(url, headers = headers)
        content = responce.content.decode('utf-8')
        f = open(path, mode = 'x')
        f.write(content)
        f.close()
    if flag:
        print('Finish')