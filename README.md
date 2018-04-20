# MLB-Batting-Data-Analysis

I create program that scraps Baseball data from ESPN.COM. Explaining the data, it is MLB Players Batting Stats for 2017(http://www.espn.com/mlb/stats/batting). The column of data including Ranking, Player name, Team, Ab, Run, Hit, 2B, 3B, HR, RBI, SB, CS, BB, SO, AVG, OBP, SLG, OPS, and WAR. And each page has 40 players and there are total 144 players.


After create the data base the program will offer interactive searching function that 
user can searh stats by playername or teamname.

Among 17 features of stat I selected certain featurs that seems important to check players or teams ability.

In addition, this program also offer the function thatcompare either two teams or two players. All the function will offer function of plotting. if you add 'plat' after the command it will automatically plotting either table, barchart or radar chart 


structure of data base 
DBname : 2017_batting.db
table 'Players' : primary key = Id
table 'Stats' : primary key = Rank.Id

#note : the program use cache. Once you run the program the cache file will be created





##code structure 

1.line [0:140]
  : code for scraping data and append it to lists 
 
2.line[143:252]
  : create database and table, then append data to tables
  
3.Class Search 
  :SQL Query that extract data from database 

4.Class Compare
  :SQL Query that extract data from database for compare two teams or two players
  

5.Class Ploty 
  : the code that create table/barchart/radarchart/compare barchart/ compare radar chart using Plotly
  

6.line[595:] 
  : code for interactive search function 
  


Explanation of search function  
    *list <choose 'players' or 'teams'> 
        available anytime
        list all avilable players or teams
        valid inputs: "players" or "Teams"
        (e.g. list players or list teams)

    *player <playername>
        available only if there is an active result set list 
        valid inputs : specific player name 
        (e.g. player Chris Davis)

    *team <teamname>
        available only if there is an active result set list
        vaild inputs : specific team abbreviation
        (e.g. team LAD)

    *compare <players> <playername1> <playername 2>
            or  
            <teams> <team abbr1> <team abbr2>
        available only if there is an active result set list 
        vaild inputs : two specific player name or two specific team abbr
        (e.g. compare players Chris Davis Adam Johns)
        or
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
  
