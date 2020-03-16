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


    def get_move(self, env) -> int:
        itter = 0
        while True:
            itter += 1
            move = self.pick_move(env)
            if self.validate_move_option(env, move):
                break
            if itter > self.max_itter:
                break
        return move


    def validate_move_option(self, env, slot) -> bool:
        valid = True
        try:
            i = int(next(idx for idx, x in enumerate(self.grid[:,slot]) if x == 0))
        except Exception as e:
            valid = False
        return valid


    def pick_move(self, env):
        return 0


class RandomPlayer(PlayerTemplate):
    """Random Player
    Pick move slot at random.
    """
    def pick_move(self, env):
        return np.random.randint(0, self.output_range)


class StrategyPlayer(PlayerTemplate):
    def pick_move(self, env):
        pass
