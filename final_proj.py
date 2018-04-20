import requests
import requests_cache
import json
import re
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
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


def get_col_name(url) : 
    html = requests.get(url).text
    colname = []
    soup = BeautifulSoup(html,'html.parser')
    find_colname = soup.find('tr',class_='colhead')
    for col in find_colname:
        colname.append(col.text)
    return colname
    
col_name = get_col_name(url)


## data ## 
stats = np.reshape(player_info_list, (144,19))
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
try :
    create_players_db(player_data)
    create_stats_db(player_data)
except: 
    pass
#### SQL QUERYS ###

class Search : 
    global DBNAME
    def player_names():
        
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Name 
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]     
        '''

        cur.execute(statement)

        data_list =[]
        for items in cur : 
            for item in items:
                data_list.append(item)
        
        return data_list

        conn.commit()
        conn.close()

    def team_names():
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT Team
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id] 
            GROUP BY Team    
        '''

        cur.execute(statement)

        data_list =[]
        for items in cur : 
            for item in items:
                data_list.append(item)

        return data_list

        conn.commit()
        conn.close()

    def players_brief():
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT Id, Name, Hit, Run, HR, AVG, OPS
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]     
        '''

        cur.execute(statement)

        data_list =[]
        for items in cur : 
            stats = []
            for item in items:
                stats.append(item)
            data_list.append(stats)

        return data_list

        conn.commit()
        conn.close()

    def teams_brief() : 
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        
        statement = '''
            SELECT Team, SUM(Hit), SUM(Run), SUM(HR), AVG(AVG), AVG(OPS)
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]
            GROUP BY Team     
        '''

        cur.execute(statement)

        data_list =[]
        for items in cur : 
            stats = []
            for item in items:
                stats.append(item)
            data_list.append(stats)

        return data_list

        conn.commit()
        conn.close()

    def by_player(playername): 
        global DBNAME
        
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Name, AVG, OBP , SLG, OPS
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]     
        '''
        statement = statement + " WHERE Players.Name ='" + str(playername)+"'"

        

        cur.execute(statement)

        data_list =[]
        for items in cur : 
            for item in items:
                data_list.append(item)
        
        return data_list

        conn.commit()
        conn.close()

    def by_team(teamname):
        conn = sqlite.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Team, SUM(Hit), SUM(Run), SUM(HR), SUM(BB), SUM(SO)
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]     
        '''
        statement = statement + " WHERE Team ='" + str(teamname)+"'"
        statement = statement + " GROUP BY Team"
        
        cur.execute(statement)

        data_list =[]
        for items in cur : 
            for item in items:
                data_list.append(item)
        
        return data_list

        conn.commit()
        conn.close()


class Compare : 

    def compare_players(player1, player2) : 
        global DBNAME
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Name, Run, Hit, HR, BB, SO
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]     
        '''

        statement += " WHERE Name ='"+ str(player1)+"'"+  " OR Name='"+ str(player2)+"'"
        # print(statement)
        cur.execute(statement)
        # print(cur)

        data_list =[]
        for items in cur :
            stats =[]
            for item in items :  
                stats.append(item)
            data_list.append(stats)

        return data_list # 각각의 리스트 두개로 리턴됨 (어레이)

        conn.commit()
        conn.close()


    def compare_teams(team1, team2) : 
        global DBNAME
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()

        statement = '''
            SELECT Team, AVG(Run), AVG(Hit), AVG(HR), AVG(BB), AVG(SO)
            FROM Players
            JOIN Stats
            ON Players.Id = Stats.[Rank.Id]
        '''
        statement += " WHERE Players.Team ='"+ str(team1)+"'"+  " OR Players.Team='"+ str(team2)+"'"
        statement += " GROUP BY Team"
        cur.execute(statement)

        data_list =[]
        for items in cur :
            stats =[]
            for item in items :  
                stats.append(item)
            data_list.append(stats)

        return data_list # 각각의 리스트 두개로 리턴됨 (어레이)

###### Plot #### 

class Plotly : 
    global colname
    ### first choose players? or Teams? 
    def players_table(): 
        x = Search.players_brief()
        df_players =pd.DataFrame(x,columns=['Rank','Name','Hit','Run','HR','AVG','OPS'])

        trace = go.Table(
            header=dict(values=df_players.columns,
                        fill = dict(color='#C2D4FF'),
                        align = ['left'] * 5),
            cells=dict(values=[df_players.Rank, df_players.Name, df_players.Hit, df_players.Run, df_players.HR, df_players.AVG, df_players.OPS],
                       fill = dict(color='#F5F8FF'),
                       align = ['left'] * 5))

        data = [trace] 
        py.iplot(data, filename = 'pandas_table')

    def teams_table():
        x = Search.teams_brief()
        df_teams = pd.DataFrame(x, columns = ['Team', 'Hit_Total', 'Run_Total', 'HR_Total', 'AVG', 'OPS' ])
        # print(df_teams)
        trace = go.Table(
            header=dict(values=df_teams.columns,
                        fill = dict(color='#C2D4FF'),
                        align = ['left'] * 5),
            cells=dict(values=[df_teams.Team, df_teams.Hit_Total, df_teams.Run_Total, df_teams.HR_Total, df_teams.AVG, df_teams.OPS],
                       fill = dict(color='#F5F8FF'),
                       align = ['left'] * 5))
        data = [trace] 
        py.iplot(data, filename = 'pandas_table')

    ## select specific team and player (radar chart)

    def single_player_radar(playername):
        x = Search.by_player(playername)
        data = [go.Scatterpolar(
            r = x[-4:],
            theta = ['AVG','OBP','SLG', 'OPS'],
            fill = 'toself'
        )]

        layout = go.Layout(
            polar = dict(
                radialaxis = dict(
                    visible = True,
                    range = [0, 1]
                )
            ),
            showlegend = False
        )

        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename = "player_radar_chart")


    def single_team_bar(teamname): 
        stats = Search.by_team(teamname)[-5:]
        # print(stats)

        data = [go.Bar(
                    x= ['Hit','Run','Homerun','Strike Out','Base on Balls'],
                    y = stats
            )]

        py.iplot(data, filename='basic-bar')




    def compare_players(player1, player2): 

        data_list = Compare.compare_players(player1, player2)
        
        data = [
            go.Scatterpolar(
              r = data_list[0][-5:],
              theta = ['Run','Hit','Homerun','Base on Balls','Strike Out'],
              fill = 'toself',
              name = player1
            ),
            go.Scatterpolar(
              r = data_list[1][-5:],
              theta = ['Run','Hit','Homerun','Base on Balls','Strike Out'],
              fill = 'toself',
              name = player2
            )
        ]

        layout = go.Layout(
          polar = dict(
            radialaxis = dict(
              visible = True,
              range = [0, 200]
            )
          ),
          showlegend = False
        )

        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename = "compare_player_radar")


    def compare_teams(team1, team2):
        data_list = Compare.compare_teams(team1, team2)

        trace1 = go.Bar(
            x=['Run','Hit','Homerun','Base on Balls','Strike Out'],
            y=data_list[0][-5:],
            name=team1
        )
        trace2 = go.Bar(
            x=['Run','Hit','Homerun','Base on Balls','Strike Out'],
            y=data_list[1][-5:],
            name=team2
        )

        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename='compare_team_bar')


def interactive_command():
    menu = '''help
    *`````list <choose 'players' or 'teams'> 
        available anytime
        list all avilable players or teams
        valid inputs: "players" or "Teams"
        (e.g. list players or list teams)

    *player <playername>
        available only if there is an active result set list 
        valid inputs : specific player name (e.g. player Chris Davis)

    *team <teamname>
        available only if there is an active result set list
        vaild inputs : specific team abbreviation(e.g. team LAD)

    *compare <players> <playername1> <playername 2>
            or  
            <teams> <team abbr1> <team abbr2>
        available only if there is an active result set list 
        vaild inputs : two specific player name or two specific team abbr
        (e.g. compare players Chris Davis Adam Johns)
        (e.g. compare teams LAD KC)

    *plot 
        this command is optional that you can choose either plot or not
        aviailable only after each command
        if you want to plot the data you should enter plot end of command
        then it wil display the current results.
        (e.g. player Chirs Davis plot)
        (e.g. team HOU plot)
        (e.g. list players plot)
        (e.g. compare players Chirs Davis Adam Johns plot)
    '''
    print(menu)
    command = ''
    # is_list_active = False
    is_players_active = False
    is_teams_active = False
    is_single_player_active = False
    is_single_team_active = False 
    is_plot_active = False
    is_compare_player_active = False
    is_compare_team_active = False

    while(command != 'exit'):
        try : 
            command = input("Please enter a command: ")
            command_list = command.split()

            if 'help' in command : 
                print(menu)
            
            if command_list[0] == "list":
                if 'players' in command_list[1]: # 스트링 전체에 있는 일부내용도 검색되는지 확인
                    p = Search.player_names()
                    df_players =pd.DataFrame(p,columns=['Name'])
                    print(df_players)
                    is_list_active = True
                    is_players_active = True
                    is_plot_active = True
                    if command_list[-1] =='plot':
                        Plotly.players_table()
                        print('players table has been created')
                    else :
                        pass

                elif 'teams' in command_list[1]:
                    t = Search.team_names()
                    df_players =pd.DataFrame(t,columns=['Team'])
                    print(df_players)

                    if command_list[-1] =='plot':
                        Plotly.teams_table()
                        print('teams table has been created')
                    else :
                        pass
           

            if 'player' in command_list[0]:
                playername = command_list[1] +" " + command_list[2] # get full name 
                stats = Search.by_player(playername)
                df_player =pd.DataFrame(columns = ['Name','AVG', 'OBP','SLG','OPS'])
                df_player.loc[0] = stats
                print(df_player)
                # slugger 나옴
                if command_list[-1] =='plot':
                    Plotly.single_player_radar(playername) 
                    print(playername +"'single player radar chart has been created")
                else :
                    pass
                
            elif 'team' in command_list[0]:
                teamname = command_list[1]
                stats = Search.by_team(teamname)
                df_team = pd.DataFrame(columns = ['Team', 'Hit', 'Run', 'HR','BB', 'SO'])
                df_team.loc[0]=stats
                print(df_team)

                if command_list[-1] =='plot' :
                    Plotly.single_team_bar(teamname)
                    print(teamname +"'single team bar chart has been created")
                else : 
                    pass
    

            elif 'compare' == command_list[0] : 
                if 'players' == command_list[1]:
                    player1 = command_list[2]+" "+command_list[3]
                    player2 = command_list[4]+" "+command_list[5]
                    stats = Compare.compare_players(player1, player2)
                    df_comp_player = pd.DataFrame(columns = ['Name', 'Run','Hit','HR','BB','SO'])

                    df_comp_player.loc[0] = stats[0]
                    df_comp_player.loc[1] = stats[1] 
                    print(df_comp_player)
                    
                    if command_list[-1] =='plot' :
                        Plotly.compare_players(player1,player2)
                        print("{} and {}'s comparision radar chart has been created ".format(player1, player2))
                    else : 
                        pass

                elif 'teams' == command_list[1]:
                    team1 = command_list[2]
                    team2 = command_list[3]
                    stats = Compare.compare_teams(team1, team2)
                    df_comp_team = pd.DataFrame(columns = ['Team', 'Run','Hit','HR','BB','SO'])
                    df_comp_team.loc[0] = stats[0]
                    df_comp_team.loc[1] = stats[1] 
                    print(df_comp_team)

                    if command_list[-1] =='plot' :
                        Plotly.compare_teams(team1,team2)
                        print("{} and {}'s comparision bar chart has been created".format(team1, team2))
                    else : 
                        pass

                else : 
                    pass    
            
            else : 
                pass
             
        except :
            continue

            

        
if __name__ =='__main__':
    interactive_command() 













