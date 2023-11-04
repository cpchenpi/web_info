'''
Author: Ashton
Date: 2023-10-30 09:11:03
LastEditors: Ashton
LastEditTime: 2023-11-04 17:49:40
Description: 
'''
from bs4 import BeautifulSoup
import re

movie_id = 1291545
context = open('lab1/movies_data/1291545')
tags = []
contents = []
soup = BeautifulSoup(context, 'html.parser')
movie_title = str(soup.find('span', property = 'v:itemreviewed').text)
tags.append('title')
contents.append(movie_title)
movie_score = soup.find('strong', property = 'v:average').text
tags.append('score')
contents.append(movie_score)
movie_info = soup.find('div', id = 'info')
movie_span = movie_info.find_all('span', {'class': 'pl'})
for i in movie_span:
    temp = str(i.text).replace(':', '')
    tags.append(temp)
    if temp == '类型':
        movie_types = movie_info.find_all('span', property = 'v:genre')
        movie_type = ''
        for j in movie_types:
            tmp = str(j.text)
            movie_type += (tmp + '/')
        content = movie_type
    else:
        tmp = i.next_sibling
        if tmp.text.replace(' ', '') == ':' or tmp.text.replace(' ', '') == '':
            tmp = tmp.next_sibling
        content = str(tmp.text).replace(' ', '').replace('\n', ' ')
    contents.append(content)
movie_intro = soup.find('div', {'class': 'related-info'})
tags.append('summary')
content = movie_intro.find('span', property = 'v:summary').text.replace(' ', '').replace('\u3000', '')
contents.append(content)

content = open('lab1/movies_staff_data/1291543')
staff_soup = BeautifulSoup(content, 'html.parser')
staff_names = []
staff_works = []
staff_info = staff_soup.find_all('span', {'class': 'name'})
for i in staff_info:
    staff_names.append(str(i.a.text))
    temp = str(i.find_next_sibling().text)
    staff_works.append(temp)
staff = dict(zip(staff_names, staff_works))
tags.append('author')
contents.append(staff)
print(tags)
print(contents)

tags_ = []
content_ = []
for i in range(len(contents)):
    if tags[i] == 'score' or tags[i] == '上映日期' or tags[i] == '片长' or tags[i] == 'IMDb':
        continue
    tags_.append(tags[i])
    temp = contents[i]
    if tags[i] == 'author':
        tmp = dict()
        for j in temp:
            key = re.sub(u'[a-zA-Z]', '', j).replace(' ', '')
            value = re.sub(u'[a-zA-Z]', '', temp[j]).replace(' ', '')
            tmp[key] = value
        temp = tmp
    else:
        temp = re.sub(u'[a-zA-Z]', '', temp)
        temp = re.sub(u'\\(.*?\\)', '', temp).replace(' ', '').replace('/', ',')
    content_.append(temp)