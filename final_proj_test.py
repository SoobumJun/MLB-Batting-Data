import unittest
from final_proj import *



class TestDatabase(unittest.TestCase):
    def test_player_table1 (self) :
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Players'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Jose Altuve',), result_list)
        self.assertEqual(len(result_list), 144) 

        conn.close()

    def test_player_table2 (self) : 
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT Name, Team
            FROM Players
            WHERE Team="LAD"
            ORDER BY Name ASC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 6)
        self.assertEqual(result_list[4][0], 'Justin Turner')   

        conn.close()

    def test_stats_table1(self) : 
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT AVG, OPS
            FROM Stats
            ORDER BY AVG DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 144)
        self.assertEqual(result_list[42][0], 0.285)   

        conn.close()

    def test_join (self) : 
        conn =sqlite.connect(DBNAME)
        cur = conn.cursor()
        sql = '''
            SELECT Name, HR, AVG
            FROM Players
            JOIN Stats
                ON Players.Id = Stats.[Rank.Id]
            WHERE HR >20
            ORDER BY HR DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 85)
        self.assertEqual(result_list[1][0], 'Aaron Judge')   

        conn.close()

class TestSearch(unittest.TestCase):
    def test_player_name(self) : 
        results = Search.player_names()
        self.assertEqual(results[1],'Charlie Blackmon')

    def test_team_names(self):
        results = Search.team_names()
        self.assertEqual(results[0],'ARI')

    def players_brief(self):
        results =Search.players_brief()
        self.assertEqual(results[0],[1, 'Jose Altuve', 204, 112, 24, 0.346, 0.957])


    def test_search_by_player(self) : 
        results = Search.by_player("Tim Anderson")
        self.assertIn(0.257, results)

    def test_search_by_team(self) : 
        results = Search.by_team("TOR")
        self.assertIn(525, results)

class TestCompare(unittest.TestCase) : 
    def test_compare_player(self) : 
        results = Compare.compare_players("Charlie Blackmon",'Tim Anderson')
        self.assertIn(137, results[0])
        self.assertEqual(72, results[1][1])

    def test_compare_team(self): 
        results = Compare.compare_teams("KC", "OAK")
        self.assertIn('KC', results[0])
        self.assertEqual(78.6, results[1][1])


class TestPlotly(unittest.TestCase) : 
    def test_table_plots(self):
        try:
            Plotly.players_table()
            Plotly.teams_table()
        except : 
            self.fail()

    def test_single_player_radar_plot(self):
        try:
            Plotly.single_player_radar('Tim Anderson')

        except:
            self.fail()

    def test_single_team_bar_plot(self):
        try : 
            Plotly.single_team_bar('HOU')

        except :
            self.fail()

    def test_compare_player_plot(self) : 
        try : 
            Plotly.compare_players("Charlie Blackmon",'Tim Anderson')

        except : 
            self.fail()

    def test_compare_team_plot(self) :
        try :
            Plotly.compare_teams("LAD", "DET")

        except : 
            self.fail()







print(Compare.compare_teams("KC",'OAK'))

unittest.main()