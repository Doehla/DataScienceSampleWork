import logging
import numpy as np


class PlayerTemplate:
    """Base class for player unit for the game.
    Provide logging, some basic move validation, and a hook option for picking moves.
    """
    output_range = 7
    max_itter = 10


    def __init__(self, name):
        self.logger = logging.getLogger('game.player')
        self.name = name


    def act(self, env) -> int:
        itter = 0
        while True:
            itter += 1
            move = self.pick_move(env)
            self.logger.debug('Requested move action: {}'.format(move))
            if self.validate_move_option(env, move):
                break
            if itter > self.max_itter:
                break
        self.logger.debug('Returning to game environment action: {}'.format(move))
        return move


    def validate_move_option(self, env, slot) -> bool:
        valid = True
        try:
            i = int(next(idx for idx, x in enumerate(env[:,slot]) if x == 0))  # TODO: this makes an assuption on the rules -- ideally this would be in the environment object and not here, so decoupling is needed...
        except Exception as e:
            valid = False

        self.logger.debug('Action found to be valid: {}'.format(valid))
        return valid


    def pick_move(self, env):
        return 0


class RandomPlayer(PlayerTemplate):
    """Random Player
    Pick move slot at random.
    """
    def pick_move(self, env):
        return np.random.randint(0, self.output_range)


class HumanPlayer(PlayerTemplate):
    print_board = None

    def set_board_print_function(self, func):
        self.print_board = func

    def pick_move(self, env):
        print(self.print_board(1))
        while True:
            move = input('Enter move (0-6): ')
            if move in ('0','1','2','3','4','5','6'):
                move = int(move)
                break

        self.logger.debug('Selected player move: {}'.format(move))
        return move


class StrategyPlayer(PlayerTemplate):
    def pick_move(self, env):
        pass
