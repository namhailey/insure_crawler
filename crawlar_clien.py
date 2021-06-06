# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#필요한 모듈 임포트하기
!pip install selenium
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os 
from selenium import webdriver #import requests #request+bs4 조합만으로도 crawling가능 
import time
import re

#크롬드라이버, 파싱 도구인 뷰티풀수프를 한번에 진행할 drive함수 만들기
def drive(url):
    driver = webdriver.Chrome(r'C:\\Users\\n_kh\\Downloads\\chromedriver_win32 (1)\\chromedriver') #크롬드라이버를 driver에 저장
    driver.implicitly_wait(3) 
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return driver, soup

#####1.html 가져올 사이트 지정하기
#가져온 html 파싱데이터에서 id 추출


def id_and_pages(num):
    t_ids = []
    for i in range(num):
        base_url = 'https://www.clien.net/service/group/insure?&od=T31&category=0&po={0}'.format(i)
        driver, soup = drive(base_url)
        driver.close
        title = soup.select(".list_subject")
        len_title = len(title)
        for j in range(len_title):
            if title[j].get('href').find('insure_qna') != -1:
                ids = title[j].get('href').split('/service/board/insure_qna/')[1].split('?')[0]
                t_ids.append((ids,i))
        print("완료")
    return t_ids

#제목, 내용, 댓글, 날짜 추출
def clien(ID, page):
    url = 'https://www.clien.net/service/board/insure_qna/{0}?od=T31&po={1}&category=0&groupCd=insure'.format(ID,page) 
    #print(url) 
    driver, soup = drive(url)
    driver.close()
    clien_title = soup.select_one('.post_subject > span').get_text()
    contents = str(soup.find_all('div', 'post_article'))
    contents.split('<img')[0]
    contents=re.sub('<.+?>', '', contents).strip()
    contents=re.sub('\n', '', contents).strip()
    contents = contents.replace("[","")
    contents = contents.replace("]","")
    date = str(soup.select_one('.post_author > span').get_text())
    date = re.sub('\n', '', date).strip()
    
    #댓글   
    try: 
        comments_name = str(soup.select('.comment_info > .post_contact > .contact_name > .nickname >span'))
        comments_name = comments_name.replace("[<span>","")
        comments_name = comments_name.replace("</span>]","")
        comments = soup.select_one('.comment_view > input')
        comments = comments['value']
        comments= re.sub('\n', '', comments).strip()
    except:
        comments_name = ''
        comments = ''
    
    return clien_title, contents, comments_name, comments, date
#https://www.clien.net/service/board/insure_qna/16139706?od=T31&po=0&category=0&groupCd=insure
#16139706번 실행
#contents

#수정
from pandas import Series, DataFrame

raw_data = {'clien_title': [],
            'contents': [],
            'comments_name': [],
            'comments' : [],
            'date' : []}

data2 = DataFrame(raw_data)

#data_frame만들어서 한줄한줄 삽입하기.
#clien_title_ = [] 
#contents_ = []
#comments_name_ = [] 
#comments_ = []
#len(t_ids)

t_ids = id_and_pages(29)
t_ids = t_ids[227:]

for i in range(len(t_ids)):
    clien_title,contents, comments_name, comments, date = clien(t_ids[i][0],t_ids[i][1])
    data2.loc[len(data2)] = clien_title,contents, comments_name, comments, date
    print("{0}완료".format(i))

data2
##############################################

#내보내기

data, data2
    
import pandas as pd
data_all = pd.concat([data,data2], ignore_index=True)
data_all = data_all.drop_duplicates(['contents'], ignore_index = True)
len(data_all)

data_all.clien_title

with open(r"C:\\Users\\n_kh\\Desktop\\남경혜_개인과제\\코드\\data_clien.pickle", 'wb') as f:
    pickle.dump(data_all, f, pickle.HIGHEST_PROTOCOL)
    
data_all.to_excel(r"C:\\Users\\n_kh\\Desktop\\남경혜_개인과제\\코드\\data_clien.xlsx", encoding = 'utf-8')
