'''
Author: Ashton
Date: 2023-11-04 19:48:14
LastEditors: Ashton
LastEditTime: 2023-11-04 20:09:52
Description: 
'''
import json
from movie_ex import movie_ex


def print_info_book(id: int):
    data = json.load(open("lab1/book_data/" + str(id) + ".json", "r", encoding="utf-8"))
    print("书名：" + data["title"])
    print("作者：", end="")
    print(*data["author"], sep="，")
    if len(data["translator"]):
        print("译者：", end="")
        print(*data["translator"], sep="，")
    print("内容简介：" + data["summary"])
    print("作者简介：" + data["author_intro"])
    print("详情页：" + "https://book.douban.com/subject/" + str(id))
    print()


def print_info_movie(id: int):
    data = movie_ex(str(id), show = True)
    print("电影名：" + data["title"])
    print("导演：" + data["导演"])
    print("编剧：" + data["编剧"])
    print("主演：" + data["主演"])
    print("类型：" + data["类型"])
    print("内容简介：" + data["summary"])
    print("详情页：" + "https://movie.douban.com/subject/" + str(id))
    print()


def print_info(id: int, genre="book"):
    if genre == "book":
        return print_info_book(id)
    else:
        return print_info_movie(id)


if __name__ == "__main__":
    print_info(1043815, genre="book")
    print_info(1291850, genre="movie")
