import sys
import logging

import game_sys_objects

# Set up logging for the game:
root = logging.getLogger('game')
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


# Run the game:
if __name__ == '__main__':
    # Class initialization:
    game = game_sys_objects.environment.Environment()
    rando = game_sys_objects.players.RandomPlayer('rando')
    dumbo = game_sys_objects.players.RandomPlayer('dumbo')

    # Game Set Up:
    game.add_player(rando)
    game.add_player(dumbo)

    # Execute the game:
    game.run_game()
