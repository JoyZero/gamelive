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

    def format_game_by_name(self):
        games = self.game_data('detail')


if __name__ == '__main__':
    data_getter = SinaGameDataGetter()
    formater = DataFormater(data_getter)
    print formater.format_title()
    print formater.format_gamelist()
