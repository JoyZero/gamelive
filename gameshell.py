#! /usr/bin/python
#--*-- coding: utf-8--*--
from gameData import *
from gameFormater import *

if __name__ == '__main__':
    game_data_getter = SinaGameDataGetter()
    game_formater = DataFormater(game_data_getter)
    print game_formater.format_title()
    while True:
        print '>>>'
        command = raw_input()
        if command == '':
            continue
        elif command == 'ls':
            print game_formater.format_gamelist()
        else:
            game_detail = game_formater.format_game_by_name(command)
            if game_detail == None:
                print 'command not support'
            else:
                print game_detail
