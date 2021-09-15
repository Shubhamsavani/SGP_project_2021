# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
url='https://online-learning.harvard.edu/catalog?keywords=&subject%5B%5D=100&max_price=&start_date_range%5Bmin%5D%5Bdate%5D=&start_date_range%5Bmax%5D%5Bdate%5D='
response=requests.get(url)
if response.status_code != 200:
    raise Exception('Failed to load page{}'.format(url))


# %%
soup=BeautifulSoup(response.text,'html.parser')
def get_topics_url():
    name_div=soup.find_all('div',class_='field field-name-title-qs')
    course_title=[]
    course_url=[]
    for i in range(len(name_div)):
        h3=name_div[i].find('h3')
        name=h3.find('a')
        course_url.append("https://online-learning.harvard.edu"+name['href'])
        course_title.append(name.text)
    return course_title,course_url


# %%
ret=get_topics_url()
course_title=ret[0]
course_url=ret[1]


# %%
def get_details(x):
    sc_url=course_url[x]
    response = requests.get(sc_url)
    if response.status_code != 200:
        raise Exception('Failed to load page this {}'.format(url))
    soup=BeautifulSoup(response.text,'html.parser')
    duration=soup.find('div',class_='field field-name-field-duration')
    temp_div=soup.find('div',class_='field field-name-field-difficulty field-type-list-text field-label-inline clearfix')
    diff=temp_div.find('div',class_='field')
    te_div=soup.find('div',class_='field field-name-field-credit field-type-list-text field-label-inline clearfix')
    audit=te_div.find('div',class_='field')
    return duration.text,diff.text,audit.text


# %%
duration=[]
difficulty=[]
audit=[]
for j in range(len(course_url)):
    reply=get_details(j)
    duration.append(reply[0])
    difficulty.append(reply[1])
    audit.append(reply[2])
all_dict={
    'name':course_title,
    'difficulty':difficulty,
    'audit':audit,
    'duration':duration,
    'url':course_url
}
# converting to dataframe 
all_dataframe=pd.DataFrame(all_dict)
all_dataframe.to_csv('Harvard_info.csv',index=None)


# %%



