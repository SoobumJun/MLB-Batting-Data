import requests
import requests_cache
import json
import re
import numpy as np
import pandas as pd
import plotly.plotly as py
from bs4 import BeautifulSoup
import sqlite3 as sqlite


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
        #player_total_info_list.append(player_info_list)    


    return player_total_info_list


player_info_list = get_player_info(soup_list)
# print(player_info_list)
# print(player_info_list)

def get_col_name(url) : 
    html = requests.get(url).text
    colname = []
    soup = BeautifulSoup(html,'html.parser')
    find_colname = soup.find('tr',class_='colhead')
    for col in find_colname:
        colname.append(col.text)
    return colname
    
col_name = get_col_name(url)
print(col_name) # column 이름 잘 뽑힘

## data ## 
stats = np.reshape(player_info_list, (144,19))
# print(stats)
player_data = []


for item in stats :
    temp_dic = {}
    temp_dic['Rank'] = item[0]
    temp_dic['Player'] = item[1]
    temp_dic['Team'] = item[2]
    temp_dic['AB'] = item[3]
    temp_dic['Run'] = item[4]
    temp_dic['Hit'] =item[5]
    temp_dic['2B'] = item[6]
    temp_dic['3B'] = item[7]
    temp_dic['HR'] = item[8]
    temp_dic['RBI'] = item[9]
    temp_dic['SB'] = item[10]
    temp_dic['CS'] = item[11]
    temp_dic['BB'] = item[12]
    temp_dic['SO'] = item[13]
    temp_dic['AVG'] = item[14]
    temp_dic['OBP'] = item[15]
    temp_dic['SLG'] = item[16]
    temp_dic['OPS'] = item[17]
    temp_dic['WAR'] = item[18]
    player_data.append(temp_dic)


print(player_data) 
        


## 
######### Create database ########### 

DBNAME = '2017_batting.db'

def create_players_db(data):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()


    ####### create plyer info table ######## 
    statement =''' 
        DROP TABLE IF EXISTS 'Players' ; 
    '''
    
    statement = '''
        CREATE TABLE 'Players' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'Name' TEXT NOT NULL,
        'Team' TEXT NOT NULL
        );
    '''
    

    cur.execute(statement)

    insert_list = [] 
    for item in data : 
        temp_list = []
        temp_list.append(item['Player'])
        temp_list.append(item['Team'])
        insert_list.append(temp_list)

    for item in insert_list : 
        insertion =(None,item[0], item[1])
        statement = '''INSERT INTO Players VALUES (?,?,?)'''
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def create_stats_db(data):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    ####### creat stat table ###### 
    statement =''' 
        DROP TABLE IF EXISTS 'Stats' ; 
    '''
    
    statement = '''
        CREATE TABLE 'Stats' (
        'Rank.Id' INTEGER PRIMARY KEY,
        'AB' INTEGER,
        'Run' INTEGER,
        'Hit' INTEGER,
        '2B' INTEGER,
        '3B' INTEGER,
        'HR' INTEGER,
        'RBI' INTEGER,
        'SB' INTEGER,
        'CS' INTEGER,
        'BB' INTEGER,
        'SO' INTEGER,
        'AVG' REAL NOT NULL,
        'OBP' REAL NOT NULL,
        'SLG' REAL NOT NULL,
        'OPS' REAL NOT NULL,
        'WAR' REAL NOT NULL
         );
    '''
    cur.execute(statement)

    insert_list2 = [] 
    for item in data : 
        temp_list2 = []
        temp_list2.append(item['Rank'])
        temp_list2.append(item['AB'])
        temp_list2.append(item['Run'])
        temp_list2.append(item['Hit'])
        temp_list2.append(item['2B'])
        temp_list2.append(item['3B'])
        temp_list2.append(item['HR'])
        temp_list2.append(item['RBI'])
        temp_list2.append(item['SB'])
        temp_list2.append(item['CS'])
        temp_list2.append(item['BB'])
        temp_list2.append(item['SO'])
        temp_list2.append(item['AVG'])
        temp_list2.append(item['OBP'])
        temp_list2.append(item['SLG'])
        temp_list2.append(item['OPS'])
        temp_list2.append(item['WAR'])
        insert_list2.append(temp_list2)

    for item in insert_list2 : 
        insertion2 = (item[0], item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],item[13],item[14],item[15],item[16])
        print(insertion2)
        statement2 = '''INSERT INTO Stats VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        cur.execute(statement2, insertion2)
    
    


    conn.commit()
    conn.close()

create_players_db(player_data)
create_stats_db(player_data)























