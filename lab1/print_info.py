import json


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


def print_info(id: int, genre="book"):
    if genre == "book":
        return print_info_book(id)
    else:
        pass


if __name__ == "__main__":
    print_info(1043815, genre="book")
