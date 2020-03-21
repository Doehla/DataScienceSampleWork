import os
import logging
import itertools
import numpy as np
import tensorflow.keras as keras
from collections import deque


class StrategyModel:
    row_cnt = 6
    col_cnt = 7

    def __init__(self, v_name=None):
        self.logger = logging.getLogger('game.model')
        self.history = deque(maxlen=10**4)

        if v_name is None:
            self.model = self.create()
        else:
            self.model = self.load_model(v_name)


    def create(self):
        """Create a new model to use"""
        pass


    def export_model(self, version):
        """Export current model to use again later"""
        f_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'models'
            'v{}.h5'.format(verion)
        )
        self.model.save(f_name)
        self.logger.info('Exported model to: {}'.format(f_name))


    def import_model(self, version):
        """Import previously exported model for use"""
        f_name = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'models'
            'v{}.h5'.format(verion)
        )
        self.model = keras.models.load_model(f_name)
        self.logger.info('Imported model from: {}'.format(f_name))


    def _reshape_for_model_input(self, env):
        return env.reshape([-1, 6, 7, 1])


    def _parse_move_probability(self, probabilities):
        action = np.argmax(probabilities)
        self.logger.debug('Given: {}, Do: {}'.format(
            probabilities,
            action
        ))
        return action


    def get_move(self, env):
        use_env = self._reshape_for_model_input(env)
        prob_vector = self.model.predict(use_env)
        action = self._parse_move_probability(prob_vector)

        self.history.append((
            env.copy(),
            action
        ))

        return action


class CNN_Model(StrategyModel):
    def create(self):
        """Create a new model to use"""
        model = keras.models.Sequential()
        model.add(keras.layers.InputLayer(input_shape=(6,7,1)))
        model.add(keras.layers.Conv2D(16, (4,4), activation='sigmoid'))
        model.add(keras.layers.Dense(10, activation='sigmoid'))
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(7))

        model.compile(optimizer='adam', loss=keras.losses.CategoricalCrossentropy())

        return model


    def _fetch_sets(self, env):
        for i in range(self.col_cnt):
            yield env[:,i]
        for i in range(self.row_cnt):
            yield env[i,:]
        for i in range(-self.row_cnt + 1, self.col_cnt):
            yield np.diag(env, k=i)
        for i in range(-self.row_cnt + 1, self.col_cnt):
            yield np.diag(np.fliplr(env), k=i)


    def score(self, env):
        """Define the score to be based on the connectiveness found:
            + the amount of connectiveness for the agent
            - the amount of connectiveness for the opponent agent
        Single tokens do not contribute to connectiveness
        Longer chains of connectiveness are much more import
        If find a wining chain, add an additional significant factor
        """
        t_score = 0
        for score_set in self._fetch_sets(env):
            score_set = np.trim_zeros(score_set)
            for k, g in itertools.groupby(score_set):
                cnt = int(sum(1 for _ in g))
                t_score += ((cnt-1)**3) * k
                if cnt >= 4:
                    t_score += 50 * k
        return t_score


    def reward(self, env, action):
        use_env = env.copy()
        initial_score = self.score(use_env)
        try:
            i = int(next(idx for idx, x in enumerate(use_env[:,action]) if x == 0))
        except Exception:
            # Apply penalty for invalid move submission:
            final_score = -100
            return final_score

        # Update to look at the resulting environment:
        use_env[i, action] = 1
        final_score = self.score(use_env)
        return final_score - initial_score


    def show_history(self):
        for env, action in self.history:
            r = self.reward(env, action)
            use_env = self._reshape_for_model_input(env)
            print('Action: {} -> reward: {}'.format(action, r))
