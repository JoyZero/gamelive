#--*-- coding: utf-8 --*--
'this is a module to get game data'

import requests, json
from time import strftime, localtime

class GameDataGetter(object):
    """a base class to get game data"""

    def get_games_summary(self, args):
        """an unimplement method of get games data summary"""
        data = {
            'result': False,
            'data': {
                'error': "unimplement"
            }
        }
        return data

    def get_game_data(self, params):
        """an unimplement method of get one particular game data"""
        data = {
            'result': False,
            'data': {
                'error': "unimplement"
            }
        }
        return data

class SinaGameDataGetter(GameDataGetter):
    """a game data getter of sina sport"""
    url = "http://api.sports.sina.com.cn/?p=nba&s=match&a=dateMatches&format=json&callback=NBA_JSONP_CALLBACK&date=%s&dpc=1"
    date = strftime("%Y-%m-%d", localtime())
    all_end = False
    all_data = None
    summary_data = None

    def __init__(self, date=None):
        """format the url with local time"""
        #defaultly, the data param is today
        if date != None:
            self.date = date
        self.url = self.url % self.date
        # self.raw_data = self.get_games_summary()
        # self.extract_summary_data(self.raw_data)

    def get_games_summary(self):
        """get data summary from sina sport"""
        #if all games end, don't need to get data from internet again
        if self.all_end == True:
            return summary_data
        #get data from internet and extract useful information
        try:
            #send request to get data
            raw_data = requests.get(self.url).text
            #extract json data from raw string data
            begin = raw_data.index('(') + 1
            end = raw_data.rindex(')')
            #convert string json data to python dict
            self.all_data = json.loads(raw_data[begin:end])
            #etract useful data
            summary = self.extract_summary_data(self.all_data)
            summary_data = summary
        except Exception as e:
            #print 'meetin error with get games summary data'
            print e
            summary = {
                'result': False,
                'data': {
                    'error': "get data error"
                }
            }
        return summary

    def extract_summary_data(self, data):
        """extract useful information from param 'data' which is a dict"""
        games = data['result']['data']
        summary = {}
        #present the games playing and ended
        play_count, end_count, wait_count = 0, 0, 0
        summary['total'] = len(games)
        games_detail = []
        #look up every game
        for game in games:
            game_data = {}
            #game status
            game_data['status'] = game['status_cn']
            #away team name
            game_data['a_team'] = game['team1_name']
            #home team name
            game_data['h_team'] = game['team2_name']
            #away team short name
            game_data['a_short'] = game['team1_alias']
            #home team short name
            game_data['h_short'] = game['team2_alias']
            #away team score
            game_data['a_score'] = int(game['team1_score'])
            #home team score
            game_data['h_score'] = int(game['team2_score'])
            if u'完场'.encode('utf-8') == game['status_cn'].encode('utf-8'):
                end_count += 1
            elif game_data['a_score'] == 0 and game_data['h_score'] == 0:
                wait_count += 1
            else:
                play_count += 1
            games_detail.append(game_data)
        summary['end'] = end_count
        summary['wait'] = wait_count
        summary['play'] = play_count
        summary['detail'] = games_detail
        #set the flag True when all games over
        if end_count == summary['total']:
            all_end = True
        return summary

    def write_file(self):
        # print type(self.all_data)

        with open('./raw_data.json', 'w') as f:
            f.write(json.dumps(self.all_data))

if __name__ == "__main__":
    """main method for test"""
    game = SinaGameDataGetter()
    game.get_games_summary()
    game.write_file()
