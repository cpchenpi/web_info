'''
Author: Ashton
Date: 2023-10-30 09:11:03
LastEditors: Ashton
LastEditTime: 2023-11-04 19:41:57
Description: 
'''
from bs4 import BeautifulSoup
import re

def movie_ex(id: str):
    movie_path = 'lab1/movies_data/' + id
    context = open(movie_path)
    tags = []
    contents = dict()
    soup = BeautifulSoup(context, 'html.parser')
    movie_title = str(soup.find('span', property = 'v:itemreviewed').text)
    tags.append('title')
    contents['title'] = movie_title
    movie_score = soup.find('strong', property = 'v:average').text
    tags.append('score')
    contents['score'] = movie_score
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
        elif temp == '官方小站':
            continue
        else:
            tmp = i.next_sibling
            if tmp.text.replace(' ', '') == ':' or tmp.text.replace(' ', '') == '':
                tmp = tmp.next_sibling
            content = str(tmp.text).replace(' ', '').replace('\n', ' ')
        contents[temp] = content
    movie_intro = soup.find('div', {'class': 'related-info'})
    tags.append('summary')
    content = movie_intro.find('span', property = 'v:summary').text.replace(' ', '').replace('\u3000', '')
    contents['summary'] = content

    staff_path = 'lab1/movies_staff_data/' + id
    content = open(staff_path)
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
    contents['author'] = staff

    tags_ = []
    content_ = dict()
    for tag in contents:
        if tag == 'score' or tag == '上映日期' or tag == '片长' or tag == 'IMDb':
            continue
        tags_.append(tag)
        temp = contents[tag]
        if tag == 'author':
            tmp = dict()
            for j in temp:
                key = re.sub(u'[a-zA-Z]', '', j).replace(' ', '').replace('-', '')
                value = re.sub(u'[a-zA-Z]', '', temp[j]).replace(' ', '')
                tmp[key] = value
            temp = tmp
        else:
            temp = re.sub(u'[a-zA-Z]', '', temp).replace('-', '')
            temp = re.sub(u'\\(.*?\\)', '', temp).replace(' ', '').replace('/', ',')
        content_[tag] = temp
    return content_