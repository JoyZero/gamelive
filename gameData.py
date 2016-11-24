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

    def __init__(self, date=None):
        """format the url with local time"""
        #defaultly, the data param is today
        if date != None:
            self.date = date
        self.url = self.url % self.date

    def get_games_summary(self, time=None):
        """get data summary from sina sport"""
        try:
            #send request to get data
            raw_data = requests.get(self.url).text
            #extract json data from raw string data
            begin = raw_data.index('(') + 1
            end = raw_data.rindex(')')
            #convert string json data to python dict
            json_data = json.loads(raw_data[begin:end])
            #etract useful data
            summary = self.extract_summary_data(json_data)
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
        on_count, off_count = 0, 0
        summary['total'] = len(games)
        games_detail = []
        #look up every game
        for game in games:
            game_data = {}
            game_data['status'] = game['status_cn']
            game_data['a_team'] = game['team1_name']
            game_data['h_team'] = game['team2_name']
            game_data['a_short'] = game['team1_alias']
            game_data['a_short'] = game['team2_alias']
            game_data['a_score'] = game['team1_score']
            game_data['h_score'] = game['team2_score']
            if game['status_cn'] == '完场':
                off_count += 1
            else:
                on_count += 1
            games_detail.append(game_data)
        summary['on'] = on_count
        summary['off'] = off_count
        summary['detail'] = games_detail
        return summary

game = SinaGameDataGetter()
print game.get_games_summary()
