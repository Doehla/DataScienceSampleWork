import sys
import logging

import game_sys_objects

# create logger
root = logging.getLogger('game')
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)




if __name__ == '__main__':
    game = game_sys_objects.environment.Environment()
    rando1 = game_sys_objects.players.RandomPlayer()


    game.add_player('rando', rando1)
    game.add_player('dumbo', rando1)
    game.run_game()
