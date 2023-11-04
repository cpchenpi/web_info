import os

with open("lab1/Movie_id.csv", "r") as idlist_file:
    for id in [s.strip() for s in idlist_file.readlines()]:
        movie_path = "lab1/movies_data/" + id
        s = False
        with open(movie_path, "r", encoding="utf-8") as file:
            if "页面不存在" in file.read():
                print(id)
                s = True
        if s:
            os.remove(movie_path)
            os.remove("lab1/movies_staff_data/" + id)
