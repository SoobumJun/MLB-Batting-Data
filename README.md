
# MLB-Batting-Data-Analysis

This is program that scraps data from espn.com basebasll page. 
2017 batting data and create database.

# Data sources

The column of data including Ranking, Player name, Team, Ab, Run, Hit, 
2B, 3B, HR, RBI, SB, CS, BB, SO, AVG, OBP, SLG, OPS, and WAR. 
And each page has 40 players and there are total 140 players. 


After database is automatically created, 
it will offer interactive searching function that 
user can searh stats by playername or teamname. 
In addtiion, this program also offer the function that
compare either two teams or two players. 

All the function will offer function of plotting. 
if you type 'plot' after the command it will automatically plotting 
either table, barchart or radar chart depend of search criteria.


structure of data base 
DBname : 2017_batting.db

table 'Players' : primary key = Id

table 'Stats' : primary key = Rank.Id

### Note : the program use cache. Once you run the program, the cache file will be created




# Code structure 

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
  
