import requests
import time
import os
import json

s = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def get_data(url):
    try:
        response = s.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Success!")
            return json.loads(response.text)
        else:
            print("Failed!")
            print(response.text)
            if "book_not_found" in response.text:
                return "book_not_found"
            return None
    except requests.RequestException as e:
        print("Failed!")
        return None


with open("lab1/Book_id.csv", "r") as book_id:
    for line in book_id.readlines():
        id = line.rstrip()
        url = (
            "https://api.douban.com/v2/book/"
            + id
            + "?apikey=0ac44ae016490db2204ce0a042db2916"
        )
        print(url)
        path = "lab1/book_data/" + id + ".json"
        if os.path.exists(path):
            continue
        print("Try getting...")
        data = None
        while data is None:
            data = get_data(url)
            time.sleep(1)
        if data == "book_not_found":
            print("Book not found!")
            continue
        data = json.dumps(data, indent=4, ensure_ascii=False)
        save_data = open(path, "w", encoding="utf-8")
        save_data.write(data)
        time.sleep(1)
