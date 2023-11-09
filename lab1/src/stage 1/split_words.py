"""
Author: Ashton
Date: 2023-11-04 19:10:12
LastEditors: Ashton
LastEditTime: 2023-11-04 19:44:17
Description: 
"""
import jieba, json, thulac
from movie_ex import movie_ex


def get_stopwords():
    stopwords_set = set({"\n", " "})
    with open("lab1/data/cn_stopwords.txt", "r", encoding="utf-8") as stopwords_file:
        for line in stopwords_file.readlines():
            stopwords_set.add(line.strip())
    return stopwords_set


stopwords_set = get_stopwords()


thulac = thulac.thulac(seg_only=True, filt=True)


def get_synonyms():
    synonym_dict = dict()
    with open("lab1/data/dict_synonym.txt", "r", encoding="utf-8") as synonym_file:
        for line in synonym_file.readlines():
            ls = line.split()[1:]
            if len(ls) >= 2:
                for i in range(1, len(ls)):
                    synonym_dict[ls[i]] = ls[0]
    return synonym_dict


synonym_dict = get_synonyms()


def synonym_pivot(word: str):
    if word in synonym_dict:
        return synonym_dict[word]
    else:
        return word


def split_words_book(id: int, method="jieba"):
    data = json.load(open("lab1/data/book_data/" + str(id) + ".json", "r", encoding="utf-8"))
    ret = set()
    for s in [data["title"], data["author_intro"], data["summary"]]:
        if method == "jieba":
            for word in jieba.cut_for_search(s):
                ret.add(word)
        elif method == "thulac":
            for word in thulac.cut(s, text=True).split():
                ret.add(word)
    for dc in data["tags"]:
        ret.add(dc["title"])  # use tag as a word
    for key in ["translator", "author"]:
        for name in data[key]:
            ret.add(name)
    ret = set(
        map(
            synonym_pivot,
            ret,
        )
    )
    return ret - stopwords_set


def split_words_movie(id: int, method="jieba"):
    data = movie_ex(str(id))
    ret = set()
    for key in ["title", "summary", "类型", "又名", "语言", "制片国家/地区"]:
        if key not in data:
            continue
        s = data[key]
        if method == "jieba":
            for word in jieba.cut_for_search(s):
                ret.add(word)
        elif method == "thulac":
            for word in thulac.cut(s, text=True).split():
                ret.add(word)
    for name in data["author"]:
        ret.add(name)
    for key in ["导演", "编剧"]:
        if key in data:
            ret.add(data[key])
    ret = set(
        map(
            synonym_pivot,
            ret,
        )
    )
    return ret - stopwords_set


def split_words(id: int, method="jieba", genre="book"):
    if genre == "book":
        return split_words_book(id, method)
    else:
        return split_words_movie(id, method)


if __name__ == "__main__":
    print(split_words(1000280, method="jieba"))
    print(split_words(1000280, method="thulac"))
    print(split_words(1291543, method="jieba", genre="movie"))
    print(split_words(1291543, method="thulac", genre="movie"))
