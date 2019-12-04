# -*- coding: utf-8 -*-
import requests
from lxml import etree
from bs4 import BeautifulSoup
from lxml import html
from numpy import savetxt
import numpy as np
import pandas as pd

USERNAME = '' # put usename here
PASSWORD = '' # put password here

req_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
formdata = {
    'login': USERNAME,
    'password': PASSWORD,
    'exceededAttempts' : 'False'
}
req_headers2 = {
    'Host': 'schools.dnevnik.ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://dnevnik.ru/feed',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
req_headers3 = {
    'Host': 'schools.dnevnik.ru',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'https://schools.dnevnik.ru/marks.aspx?school=19034&index=2&tab=subject&homebasededucation=False',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}



LOGINURL = 'https://login.dnevnik.ru/login'
DATAURL = 'https://schools.dnevnik.ru/marks.aspx?school=19034&index=3&tab=subject'
session = requests.session()

r = session.post(LOGINURL, data=formdata, headers=req_headers, allow_redirects=False)


html_marks = session.get(DATAURL,  headers=req_headers2, allow_redirects=True).text
soup = BeautifulSoup(html_marks,features="lxml")
mark_list = soup.find_all('div', class_='cc')
mark_html = str(mark_list)
contents = []
values = []
for option in soup.find_all('option'):
    contents.append(option.text.strip().rstrip())
    values.append(option['value'])
contents.pop(0)
del contents[-2:]
contents[-1] = "Все предметы"
values.pop(0)
for i, content in zip(range(len(contents)), contents):
    print(i, content)
sub = int(input("Write the number "))
if 0 <= sub <= len(contents):
    value = values[sub]
else:
    print("Please re-enter your subject")
    quit()
url = "https://schools.dnevnik.ru/marks.aspx?school=19034&index=2&tab=subject&subject="+value+"&period=&homebasededucation=False"
html_third = session.get(url,  headers=req_headers3, allow_redirects=True).text
soup3 = BeautifulSoup(html_third,features="lxml")
mark_lists = soup3.find_all('table')
html_string = str(mark_lists)
df = pd.read_html(html_string)[0]
#df = dfs[0]
#print(dfs[0])
df = df.drop("Комментарий учителя",axis=1)
df = df.drop("Присутствие",axis=1)
df = df.dropna()
# print(df)
dates = df[['Дата и время']].to_numpy().ravel()
marks_temp = []
mark_lists = BeautifulSoup(str(mark_lists),features="lxml")
marks_temp=mark_lists.find_all("span")
marks = []
for mark in marks_temp:
    marks.append(mark.contents[0])
titles = []
for link in marks_temp:
    titles.append(link['title'])

old_date = df['Дата и время'].to_numpy()
old_marks = df['Оценки'].to_numpy()

new_date = []
new_marks = []

for i in range(len(old_marks)):
    if len(old_marks[i])>1:
        new_marks += list(map(str, old_marks[i].split()))
        for _ in range(len(list(map(str, old_marks[i].split())))):
            new_date.append(old_date[i].replace("\xa0", " "))
    else:
        new_marks.append(old_marks[i])
        new_date.append(old_date[i].replace("\xa0", " "))

df_new = pd.DataFrame({"Date":new_date, "Mark":new_marks, "Title": titles})
# print(df_new)
df_new.to_csv('marks'+str(values[sub])+'.csv',index=False, encoding='utf-8-sig')
print("Done")
