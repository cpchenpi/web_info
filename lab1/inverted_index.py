from split_words import split_words, synonym_pivot
from print_info import print_info
from math import sqrt
import struct


def varilen_encode(x: int) -> list:
    s = bin(x)[2:]
    ret = bytearray()
    if len(s) % 7 != 0:
        ret.append(int(s[0 : len(s) % 7], base=2))
    for i in range(len(s) % 7, len(s), 7):
        ret.append(int(s[i : i + 7], base=2))
    ret[-1] += 1 << 7
    return ret


def varilen_decode(ls: list) -> int:
    ret = 0
    for x in ls:
        if x >= 1 << 7:
            ret = (ret << 7) + x - (1 << 7)
        else:
            ret = (ret << 7) + x
    return ret


class InvertedIndex:
    def __init__(self, genre="book") -> None:
        self.table = dict()
        self.genre = genre

    def update_from_id(self, id: int):
        for word in split_words(id, method="jieba", genre=self.genre):
            if word in self.table:
                self.table[word].append(id)
            else:
                self.table[word] = [id]

    def build_from_idlist(self, idlist: str):
        with open(idlist, "r") as idlist_file:
            for id in [int(s.strip()) for s in idlist_file.readlines()]:
                self.update_from_id(id)
        print("Build inverted index succeed!")

    def save(self, path: str):
        # 1.22 MB 1,287,056 bytes
        with open(path, "wb") as file:
            for word, ls in self.table.items():
                bytes = word.encode(encoding="utf-8")
                file.write(struct.pack(">h", len(bytes)))
                file.write(bytes)
                file.write(struct.pack(">i", len(ls)))
                for x in ls:
                    file.write(struct.pack(">i", x))
        print("Save to file " + path + " succeed!")

    def save_compressed(self, path):
        # 951 KB 974,417 bytes
        with open(path, "wb") as file:
            for word, ls in self.table.items():
                bytes = word.encode(encoding="utf-8")
                file.write(struct.pack(">h", len(bytes)))
                file.write(bytes)
                file.write(struct.pack(">i", len(ls)))
                last = 0
                for x in ls:
                    file.write(varilen_encode(x - last))
                    last = x
        print("Save(compressed) to file " + path + " succeed!")

    def load(self, path: str):
        table = dict()
        with open(path, "rb") as file:
            while True:
                name_len_raw = file.read(2)
                if len(name_len_raw) == 0:
                    break
                name_len = struct.unpack(">h", name_len_raw)[0]
                bytes = file.read(name_len)
                key = bytes.decode(encoding="utf8")
                ls_len = struct.unpack(">i", file.read(4))[0]
                ls = [struct.unpack(">i", file.read(4))[0] for _ in range(ls_len)]
                table[key] = ls
        # assert self.table == table  # for testing correctness
        self.table = table
        print("Load from file " + path + " succeed!")

    def load_compressed(self, path: str):
        table = dict()
        with open(path, "rb") as file:
            while True:
                name_len_raw = file.read(2)
                if len(name_len_raw) == 0:
                    break
                name_len = struct.unpack(">h", name_len_raw)[0]
                bytes = file.read(name_len)
                key = bytes.decode(encoding="utf8")
                ls_len = struct.unpack(">i", file.read(4))[0]
                last = 0
                ls = []
                while ls_len > 0:
                    bytes = bytearray()
                    while True:
                        bytes.append(file.read(1)[0])
                        if bytes[-1] >= 1 << 7:
                            break
                    x = last + varilen_decode(bytes)
                    ls.append(x)
                    last = x
                    ls_len -= 1
                table[key] = ls
        # assert self.table == table  # for testing correctness
        self.table = table
        print("Load(compressed) from file " + path + " succeed!")

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
    l = InvertedIndex(genre="book")
    l.build_from_idlist("lab1/Book_id.csv")
    # l.save("lab1/Book_inverted.bin")
    # l.load("lab1/Book_inverted.bin")
    l.save_compressed("lab1/Book_inverted_compressed.bin")
    l.load_compressed("lab1/Book_inverted_compressed.bin")

    def query(s: str):
        for id in l.query(s):
            print("找到匹配项，id：" + str(id))
            print_info(id)
        pass

    # top39 基督山伯爵
    # top139 阿勒泰的角落
    query("(法国 or 新疆 or 北京) and (大仲马 or 李娟 or 老舍) and (复仇 or 日常 or 骆驼)")
