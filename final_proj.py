import requests
import requests_cache
import json
import re
import numpy as np
import pandas as pd
import plotly.plotly as py
from bs4 import BeautifulSoup

BASEURL ='http://www.espn.com/mlb/stats/batting/_/year/2017/count/'

CACHE_FNAME = 'cache_espn.json'

try:
    f = open(CACHE_FNAME, "r")
    fileread = f.read()
    CACHE_DICT = json.loads(fileread)
    f.close()
except:
    CACHE_DICT = {}



##get url_list before request
def get_page_list(baseurl):
    res = [] 
    url_list=[]
    page_num = [1,41,81,121]
    for k in page_num :
        res.append("{}/qualified/true".format(k))

    for p in res :
        url_list.append(baseurl+p)

    return url_list


# x=parm_unique_comb(BASEURL)
# print(x)


url_list = get_page_list(BASEURL)
url=url_list[0]

def get_soup(url_list):
    total_soup_list =[]
    total_soup_dic = {}
    global CACHE_DICT
    global CACHE_FNAME
    
    for url in url_list :
        if url not in CACHE_DICT:
            print('Creating cache file...')
            each_page_soup_list = []
            html = requests.get(url).text
            CACHE_DICT[url] = html
            dumped_json_cache = json.dumps(CACHE_DICT)
            fw=open(CACHE_FNAME,'w')
            fw.write(dumped_json_cache)
            fw.close()
            soup = BeautifulSoup(html,'html.parser')
            each_page_soup_list.append(soup)
            total_soup_list.append(each_page_soup_list)
            

        else : 
            print("Getting cached data...")
            each_page_soup_list = []
            html = CACHE_DICT[url]
            soup = BeautifulSoup(html,'html.parser')
            each_page_soup_list.append(soup)
            total_soup_list.append(each_page_soup_list)


    return total_soup_list

soup_list = get_soup(url_list)
print(type(soup_list[0]))


def get_player_info(soup_list): 
    #search player statfield(tr->td)
    player_total_info_list=[]
    player_info_list = []
    for i in range(len(soup_list)):
        for soup in soup_list[i]:
            find_tr = soup.find_all('tr', re.compile('row'))
            for tr in find_tr:
                for item in tr:
                    player_total_info_list.append(item.text)
        # player_total_info_list.append(player_info_list)    


    return player_total_info_list


player_info_list = get_player_info(soup_list)
# print(player_info_list)

# print(player_info_list)


stat_by_player = np.reshape(player_info_list, (144,19))
print(stat_by_player[143])


## get cloumn name 
def get_col_name(url) : 
    html = requests.get(url).text
    colname=[]
    soup = BeautifulSoup(html,'html.parser')
    find_colname = soup.find('tr',class_='colhead')
    for col in find_colname:
        colname.append(col.text)
    return colname
    
print(get_col_name(url)) # column 이름 잘 뽑힘







# for i
# for elem in player_info_list : 






### request and get htmlinfo
# for url in url_list : 
#     # request
#     page_text = requests.get(url).text
#     soup = BeautifulSoup(page_text,'html.parser')

#     html_info_dic.append(soup)
#     batting_info =soup.find(id='my-players-table')
#     table = batting_info.find('table',{'class': 'tablehead'}) ## 여기에는 정보 다 나옴 (페이지 전체가 이터레이팅
#     tr = table.find_all('tr')
    
#     #td = tr.find('td')
#     tr_list.append(tr)


# print(tr_list)

# for tr in tr_list :
#     td = tr.find("td")
#     td_list=append(td)




















