"""
Author: Ashton
Date: 2023-10-30 09:11:03
LastEditors: Ashton
LastEditTime: 2023-11-04 20:06:28
Description: 
"""
from bs4 import BeautifulSoup
import re


def movie_ex(id: str, show=False):
    movie_path = "lab1/movies_data/" + id
    context = open(movie_path, "r", encoding="utf-8")
    contents = dict()
    soup = BeautifulSoup(context, "html.parser")
    movie_title_e = soup.find("span", property="v:itemreviewed")
    if movie_title_e:
        movie_title = str(movie_title_e.text)
        contents["title"] = movie_title
    movie_score_e = soup.find("strong", property="v:average")
    if movie_score_e:
        movie_score = movie_score_e.text
        contents["score"] = movie_score
    movie_info = soup.find("div", id="info")
    movie_span = movie_info.find_all("span", {"class": "pl"})
    for i in movie_span:
        temp = str(i.text).replace(":", "")
        if temp == "类型":
            movie_types = movie_info.find_all("span", property="v:genre")
            content = ""
            for movie_type in movie_types:
                content += str(movie_type.text) + "，"
            content = content[: len(content) - 1]
        elif temp == "官方小站":
            continue
        else:
            tmp = i.next_sibling
            if tmp.text.replace(" ", "") == ":" or tmp.text.replace(" ", "") == "":
                tmp = tmp.next_sibling
            content = str(tmp.text).replace(" ", "").replace("\n", " ")
        contents[temp] = content
    movie_intro = soup.find("div", {"class": "related-info"})
    if movie_intro.find("span", property="v:summary"):
        content = (
            movie_intro.find("span", property="v:summary")
            .text.replace(" ", "")
            .replace("\u3000", "")
        )
        contents["summary"] = content

    staff_path = "lab1/movies_staff_data/" + id
    content = open(staff_path, "r", encoding="utf-8")
    staff_soup = BeautifulSoup(content, "html.parser")
    staff_names = []
    staff_works = []
    staff_info = staff_soup.find_all("span", {"class": "name"})
    for i in staff_info:
        staff_names.append(str(i.a.text))
        temp = str(i.find_next_sibling().text)
        staff_works.append(temp)
    staff = dict(zip(staff_names, staff_works))
    contents["author"] = staff

    contents_ = dict()
    for tag in contents:
        if tag == "score" or tag == "上映日期" or tag == "片长" or tag == "IMDb":
            continue
        temp = contents[tag]
        if tag == "author":
            tmp = dict()
            for j in temp:
                key = re.sub("[a-zA-Z]", "", j).replace(" ", "").replace("-", "")
                value = re.sub("[a-zA-Z]", "", temp[j]).replace(" ", "")
                tmp[key] = value
            temp = tmp
        else:
            temp = re.sub("[a-zA-Z]", "", temp).replace("-", "")
            temp = re.sub("\\(.*?\\)", "", temp).replace(" ", "").replace("/", "，")
        contents_[tag] = temp
    if show:
        return contents
    else:
        return contents_
