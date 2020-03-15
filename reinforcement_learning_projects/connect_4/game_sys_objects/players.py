import logging
import numpy as np


class PlayerTemplate:
    output_range = 7
    max_itter = 10


    def __init__(self):
        self.logger = logging.getLogger('game.player')


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
    def pick_move(self, env):
        return np.random.randint(0, self.output_range)
