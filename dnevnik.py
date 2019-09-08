# -*- coding: utf-8 -*-
import requests
from lxml import etree
from bs4 import BeautifulSoup
from lxml import html
from numpy import savetxt
import numpy as np
import pandas as pd
USERNAME = 'login' # put usename here
PASSWORD = 'password' # put password here

USERNAME = 'dimaokoneshnikov22'
PASSWORD = 'nfgbs7h635l'

LOGINURL = 'https://login.dnevnik.ru/login'
DATAURL = 'https://schools.dnevnik.ru/marks.aspx?school=19034&index=2&tab=subject&homebasededucation=False'
session = requests.session()
req_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
formdata = {
    'login': USERNAME,
    'password': PASSWORD,
    'exceededAttempts' : 'False'
}

r = session.post(LOGINURL, data=formdata, headers=req_headers, allow_redirects=False)
req_headers2 = {
    'Host': 'schools.dnevnik.ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://dnevnik.ru/feed',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}

r2 = session.get(DATAURL,  headers=req_headers2, allow_redirects=True)
html_marks=r2.text
soup = BeautifulSoup(html_marks,features="lxml")
mark_list = soup.find_all('div', class_='cc')
mark_html = str(mark_list)
contents = []
values = []
for option in soup.find_all('option'):
    contents.append(option.text.strip().rstrip())
    values.append(option['value'])
contents.pop(0)
values.pop(0)
for content in contents:
    print(content+"\n")
sub = input("Write the subject ")
if sub in contents:
    index = contents.index(sub)
    value = values[index]
else:
    print("Please re-enter your subject")
    quit()
req_headers3 = {
    'Host': 'schools.dnevnik.ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://schools.dnevnik.ru/marks.aspx?school=19034&index=2&tab=subject&homebasededucation=False',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
url = "https://schools.dnevnik.ru/marks.aspx?school=19034&index=2&tab=subject&subject="+value+"&period=&homebasededucation=False"
r3 = session.get(url,  headers=req_headers3, allow_redirects=True)
html_third = r3.text
soup3 = BeautifulSoup(html_third,features="lxml")
mark_lists = soup3.find_all('table')
html_string = str(mark_lists)
dfs = pd.read_html(html_string)
df = dfs[0]
df = df.drop("Комментарий учителя",axis=1)
df = df.drop("Присутствие",axis=1)
df = df.dropna()
dates = df[['Дата и время']].to_numpy()
dates = dates.ravel()
marks_temp = []
mark_lists = BeautifulSoup(str(mark_lists),features="lxml")
marks_temp=mark_lists.find_all("span")
marks = []
for mark in marks_temp:
    marks.append(int(mark.contents[0]))
titles = []
for link in marks_temp:
    titles.append(link['title'])
indexes=[]
q=0
for i in df['Оценки']:
    if len(str(i).split())>1:
        indexes.append(q)
    q+=1
for j in range(len(titles)-len(indexes)):
    if j in indexes:
        titles[j]=titles[j]+", "+titles[j+1]
        titles.pop(j+1)
df['Titles'] = titles
df.to_csv('marks'+sub+'.csv',index=False, encoding='utf-8-sig')
