#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from pprint import pprint
import time
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
session = requests.session()
from pprint import pprint
from html import unescape
from bs4 import BeautifulSoup
import re
import time
import random
from collections import Counter


# In[ ]:


#NB! Фикбук банит по IP!!
proxies = ["122.50.5.148:10000",
"167.172.180.40:34291",
"34.90.194.216:3128", "185.206.175.24:80",
"35.178.190.5:8080",
"161.35.70.249:3128",
"182.237.18.6:82",
"59.124.224.180:3128",
"122.50.5.148:10000",
"167.172.180.40:34291",
"178.210.129.150:1234",
"185.35.101.17:8081",
"35.203.144.50:5597",
"167.172.180.46:37598",
"167.71.41.173:43667",
"157.230.103.189:34013",
"35.223.68.68:3333",
"213.142.218.226:40816",
"51.158.172.165:8811",
"94.189.133.93:8080",
"167.172.191.249:34327",
"103.114.53.2:8080",
"45.234.192.224:8080",
"167.172.109.12:32805",
"167.172.180.46:38971",
"43.227.129.193:83",
"37.187.96.66:8118",
"103.83.118.10:55443",
"103.46.233.190:81",
"139.180.131.23:3128",
"77.28.97.34:48458",
"199.247.16.136:8080",
"180.211.192.58:8080",
"88.220.104.178:8080",
"68.183.221.156:39800",
"46.36.74.60:8080",
"138.117.84.161:8080",
"84.42.4.170:8080",
"186.24.12.194:8080",
"129.232.134.107:3128",
"189.39.123.238:8080",
"49.156.35.22:8080",
"34.90.194.216:3128",
"178.62.108.207:3129",
"220.150.77.91:6000",
"45.7.255.74:999",
"35.223.68.68:3333"]


# In[ ]:


def parse_page(page_number):
    #сюда вставить ссылку с номером страниц
    url = f'https://ficbook.net/find?fandom_filter=fandom&fandom_group_id=1&fandom_ids%5B0%5D=435&deny_other=1&sizes%5B0%5D=1&sizes%5B1%5D=2&sizes%5B2%5D=3&sizes%5B3%5D=4&pages_min=&pages_max=&ratings%5B0%5D=5&ratings%5B1%5D=6&ratings%5B2%5D=7&ratings%5B3%5D=8&ratings%5B4%5D=9&directions%5B0%5D=4&likes_min=&likes_max=&date_create_min=2021-03-22&date_create_max=2021-03-22&date_update_min=2021-03-22&date_update_max=2021-03-22&title=&rnd=11530190&find=Найти!&p={page_number}#result'   
    headers = {'User-Agent': ua.random}
    for p in proxies:
        try:
            print(p)
            known_proxy_ip = p
            proxy = {'http': known_proxy_ip, 'https': known_proxy_ip}
            req = session.get(url, proxies=proxy, headers={'User-Agent': ua.random})
            page = req.text
            page_soup = BeautifulSoup(page, 'html.parser')
            title = page_soup.find_all('title')
            link = page_soup.find_all('section', {'class': 'fanfic-thumb-block'})
            if 'Проверка' in str(title):
                print('Проверка')
            else:
                break
        except Exception as e:
            print(e)
    return link


# In[ ]:


def parse_text(link):
    text = ''
    tags = []
    people = []
    fic_soup = BeautifulSoup(str(link), 'html.parser')
    title = fic_soup.find('h3').text
    my_people = fic_soup.find_all('a', {'class': 'pairing-link'})
    my_tags = fic_soup.find_all('a', {'class': 'tag'})
    for t in my_tags:
        print(t.text)
        tags.append(t.text)
    for p in my_people:
        print(p.text)
        people.append(p.text)    
    return people, tags, title


# In[ ]:


already_read = []
#all_tags = []
#all_people = []


# In[ ]:


all_tags = []
all_people = []


# In[ ]:


def write_tags(tags, title, file):
    with open(file, encoding = 'utf-8', mode = 'a') as corpus:
        corpus.write('# ')
        corpus.write(str(title))
        corpus.write('\n')
        for t in tags:
            corpus.write(t)
            corpus.write('\n')


# In[ ]:


#Тут надо переделать словарь, но я не разбираюсь в персонажах
p_and_p_dict = {
    'Элизабет': 'Элизабет Беннет',
    'Элизабет Беннет': 'Элизабет Беннет',
    'Лиззи': 'Элизабет Беннет',
    'Дарси': 'Мистер Дарси',
    'Мистер Дарси': 'Мистер Дарси', 
    'Фицуильям Дарси': 'Мистер Дарси', 
    'мистер Дарси': 'Мистер Дарси'
}


# In[ ]:


def clean(p):
    clean_people = []
    pp = p.split('/')
    #print('pp', pp)
    for pp_two in pp:
        #print(pp_two)
        pp_three = pp_two.split('\\')
        #print('three', pp_three)
        for pp_four in pp_three:
            #if ' и ' in pp_four:
            #print(' и ')
            #    
            pp_five = pp_four.split(' и ')
            #else:
                #pp_five = pp_four
            #print(5, pp_five)
            for pp_six in pp_five:
            #if '|' in pp_six:
                pp_seven = pp_six.split('|')
                for pp_eight in pp_seven:
                    pp_nine = pp_eight.split(', ')
                    #print(9, pp_nine)
                    for n in pp_nine:
                        if n != '':
                            if ']' in n:
                                nn = n.split(']')[1]
                            elif '!' in n:
                                nn = n.split('!')[1]
                            else:
                                nn = n
                            if nn != '':
                                if nn[0] == ' ':
                                    nn = nn[1:]
                            clean_people.append(nn)
    return clean_people


# In[ ]:


def write_people(people, title, file, dictionary, all_people):
    new_people = []
    with open(file, encoding = 'utf-8', mode = 'a') as corpus:
        corpus.write('# ')
        corpus.write(title)
        corpus.write('\n')
        for person in people:
            p = clean(person)
            for new_p in p:
                print(new_p)
                if new_p in dictionary.keys():
                    new_p = dictionary[new_p]
                new_people.append(new_p)
                #print(set(new_people))
        for p_p in set(new_people):
            corpus.write(p_p)
            corpus.write('\n')
            all_people.append(p_p)
        print(all_people)
        return all_people


# In[ ]:


titles = []
for x in range(9, 10):
    print('page', x)
    link = parse_page(x)
    for l in link:
        people, tags, title = parse_text(l)
        #all_people.extend(people)
        if title not in already_read:
            already_read.append(title)
            all_tags.extend(tags)
            write_tags(tags, title, 'file_taga.txt')
            all_people = write_people(people, title, 'file_people.txt', p_and_p_dict, all_people)


# In[ ]:


print(Counter(all_tags))


# In[ ]:


print(Counter(all_people))

