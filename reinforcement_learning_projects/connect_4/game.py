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

    # Random player set up:
    rando = game_sys_objects.players.RandomPlayer('rando')
    game.add_player(rando)

    # # Second random player set up:
    # dumbo = game_sys_objects.players.RandomPlayer('dumbo')
    # game.add_player(dumbo)

    # # Human set up:
    # human = game_sys_objects.players.HumanPlayer('human')
    # human.set_board_print_function(game.print_special)
    # game.add_player(human)

    learner = game_sys_objects.players.StrategyPlayer(
        'learner',
        model=game_sys_objects.models.CNN_Model()
    )
    game.add_player(learner)




    # Execute the game:
    game.run_game()
