#--*-- coding: utf-8 --*--
from gameData import *

class DataFormater(object):
    """format the dat in the dict to a human friendly string"""
    all_end = False

    def __init__(self, game_data):
        self.game_data = game_data.get_games_summary()

    def format_title(self):
        data = self.game_data
        title = '''Today we have %d games.
%d games is playing.
%d games aleady ended.
%d games is coming.
        ''' % (data['total'], data['play'], data['end'], data['wait'])
        return title

    def format_gamelist(self):
        data = self.game_data
        result = ''
        for game in data['detail']:
            game_str = '[%s]%s  VS  %s[%s] %s\n'
            game_str = game_str % (game['a_short'], game['a_score'], game['h_score'], game['h_short'], game['status'])
            result += game_str
        return result

    def format_game_by_name(self, name):
        target = None
        games = self.game_data['detail']
        for game in games:
            if name == game['a_short'] or name == game['h_short'] or name == game['a_team'] or name == game['h_team']:
                target = game
        if target == None:
            result = 'Game not found'
        else:
            title = '[%s %s]%d  VS %d[%s %s]\n' % (target['a_short'], target['a_team'], target['a_score'], target['h_score'], target['h_team'], target['h_team'])
            bar = '------------------%s----------------------\n'
            line = '%s\t%s\t%s\n'
            away_bar = bar % target['a_short']
            away = target['statics']['away']
            a_score = line % ('score', away['score']['number'], away['score']['player'])
            a_assist = line % ('assist', away['assist']['number'], away['assist']['player'])
            a_rebound = line % ('rebound', away['rebound']['number'], away['rebound']['player'])
            home_bar = bar % target['h_short']
            home  = target['statics']['home']
            h_score = line % ('score', home['score']['number'], home['score']['player'])
            h_assist = line % ('assist', home['assist']['number'], home['assist']['player'])
            h_rebound = line % ('rebound', home['rebound']['number'], home['rebound']['player'])
            result = away_bar + a_score + a_assist + a_rebound + home_bar + h_score + h_assist + h_rebound
        return result


if __name__ == '__main__':
    data_getter = SinaGameDataGetter()
    formater = DataFormater(data_getter)
    print formater.format_title()
    print formater.format_gamelist()
