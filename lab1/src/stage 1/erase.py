'''
Author: Ashton
Date: 2023-10-25 17:30:11
LastEditors: Ashton
LastEditTime: 2023-11-09 13:44:39
Description: 
'''
'''
Author: Ashton
Date: 2023-10-25 17:30:11
LastEditors: Ashton
LastEditTime: 2023-10-25 18:02:30
Description: 
'''
import os

with open("lab1/data/Movie_id.csv", "r") as idlist_file:
    for id in [s.strip() for s in idlist_file.readlines()]:
        movie_path = "lab1/data/movies_data/" + id
        s = False
        with open(movie_path, "r", encoding="utf-8") as file:
            if "页面不存在" in file.read():
                print(id)
                s = True
        if s:
            os.remove(movie_path)
            os.remove("lab1/data/movies_staff_data/" + id)