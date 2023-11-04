from split_words import split_words, synonym_pivot
from math import sqrt


class InvertedIndex:
    def __init__(self) -> None:
        self.table = dict()

    def update_from_id(self, id: int):
        for word in split_words(id, method="jieba"):
            if word in self.table:
                self.table[word].append(id)
            else:
                self.table[word] = [id]

    def build_from_idlist(self, idlist: str):
        with open(idlist, "r") as idlist_file:
            for id in [int(s.strip()) for s in idlist_file.readlines()]:
                self.update_from_id(id)

    def save(self, path: str):
        pass

    def save_compressed(self, path):
        pass

    def load(self, path: str):
        pass

    def load_compressed(self, path: str):
        pass

    def query_word(self, word: str):
        return self.table[word] if word in self.table else []

    def and_combine(self, ls1: list, ls2: list):
        n, m = len(ls1), len(ls2)
        b1, b2 = int(sqrt(n)), int(sqrt(m))
        res = []
        i, j = 0, 0
        while i != n and j != m:
            if i % b1 == 0 and i + b1 < n and ls1[i + b1] < ls2[j]:
                i += b1
            if j % b2 == 0 and j + b2 < m and ls2[j + b2] < ls1[i]:
                j += b2
            if ls1[i] == ls2[j]:
                res.append(ls1[i])
                i += 1
                j += 1
            elif ls1[i] < ls2[j]:
                i += 1
            else:
                j += 1
        return res

    def or_combine(self, ls1: list, ls2: list):
        n, m = len(ls1), len(ls2)
        b1, b2 = int(sqrt(n)), int(sqrt(m))
        res = []
        i, j = 0, 0
        while i != n and j != m:
            if i % b1 == 0 and i + b1 < n and ls1[i + b1] < ls2[j]:
                res += ls1[i : i + b1]
                i += b1
            if j % b2 == 0 and j + b2 < m and ls2[j + b2] < ls1[i]:
                res += ls2[j : j + b2]
                j += b2
            if ls1[i] == ls2[j]:
                res.append(ls1[i])
                i += 1
                j += 1
            elif ls1[i] < ls2[j]:
                res.append(ls1[i])
                i += 1
            else:
                res.append(ls2[j])
                j += 1
        if i != n:
            res += ls1[i:]
        if j != m:
            res += ls2[j:]
        return res

    def and_combine_list(self, ls: list):
        if len(ls) == 1:
            return ls[0]
        res = self.and_combine(ls[0], ls[1])
        for i in range(2, len(ls)):
            res = self.and_combine(res, ls[i])
        return res

    def or_combine_list(self, ls: list):
        if len(ls) == 1:
            return ls[0]
        res = self.or_combine(ls[0], ls[1])
        for i in range(2, len(ls)):
            res = self.or_combine(res, ls[i])
        return res

    def query(self, s: str):
        # requires statements like "(A or B) and (C or D or E or ...) and F and ..."
        or_items = [w.strip() for w in s.split("and")]
        or_items = [w[1:-1] if w[0] == "(" else w for w in or_items]
        or_items = [[synonym_pivot(o.strip()) for o in w.split("or")] for w in or_items]
        or_items.sort(key=lambda ls: sum([len(self.query_word(word)) for word in ls]))
        and_items = [
            self.or_combine_list([self.query_word(word) for word in ls])
            for ls in or_items
        ]
        return self.and_combine_list(and_items)


if __name__ == "__main__":
    l = InvertedIndex()
    l.build_from_idlist("lab1/Book_id.csv")
    # top39 基督山伯爵
    # top139 阿勒泰的角落
    print(l.query("(法国 or 新疆 or 北京) and (大仲马 or 李娟 or 老舍) and (复仇 or 日常 or 生活)"))