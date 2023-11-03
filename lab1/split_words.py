import jieba, json, thulac

stopwords_set = set({"\n", " "})

with open("lab1/cn_stopwords.txt", "r", encoding="utf-8") as stopwords_file:
    for line in stopwords_file.readlines():
        stopwords_set.add(line.strip())

thulac = thulac.thulac(seg_only=True, filt=True)


def split_words(id: int, method="jieba"):
    data = json.load(open("lab1/book_data/" + str(id) + ".json", "r", encoding="utf-8"))
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
    return ret - stopwords_set


print(split_words(1000280, method="jieba"))
print(split_words(1000280, method="thulac"))
