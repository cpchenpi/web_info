'''
Author: Ashton
Date: 2023-10-30 09:11:03
LastEditors: Ashton
LastEditTime: 2023-11-04 00:33:32
Description: 
'''
from bs4 import BeautifulSoup
import requests

movie_id = 1291545
context = open('lab1/movies_data/1291545')
tags = []
contents = []
soup = BeautifulSoup(context, 'html.parser')
movie_title = str(soup.find('span', property = 'v:itemreviewed').text)
tags.append('标题')
contents.append(movie_title)
movie_score = soup.find('strong', property = 'v:average')
tags.append('评分')
contents.append(movie_score)
movie_info = soup.find('div', id = 'info')
movie_span = movie_info.find_all('span', {'class': 'pl'})
for i in movie_span:
    temp = str(i.text).replace(':', '')
    tags.append(temp)
    if temp == '类型':
        movie_types = i.find_all('span', roperty = 'v:genre')
        movie_type = ''
        for j in movie_types:
            tmp = str(j)
            movie_type += (tmp + '/')
        content = movie_type
    else:        
        content = str(i.next_sibling.text).replace(' ', '').replace('\n', ' ')
    contents.append(content)
movie_intro = soup.find('div', {'class': 'related-info'})
tags.append('剧情简介')
content = movie_intro.find('span', property = 'v:summary').text
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
tags.append('演职员表')
contents.append(staff)