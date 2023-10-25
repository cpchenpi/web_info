'''
Author: Ashton
Date: 2023-10-25 17:30:11
LastEditors: Ashton
LastEditTime: 2023-10-25 18:02:30
Description: 
'''
import os

def read_files(path, flag):
    file_list = os.listdir(path)
    for file_name in file_list:
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            f = open(file_path)
            s = f.readline()
            f.close()
            print(s)
            if s != '<!DOCTYPE html>\n':
                os.remove(file_path)
                flag = False

flag = True
read_files('lab1/movies', flag)
read_files('lab1/books', flag)
if flag:
    print('Finish')