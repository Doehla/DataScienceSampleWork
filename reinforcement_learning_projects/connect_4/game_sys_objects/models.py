import os
import logging
import numpy as np
import tensorflow.keras as keras


class StrategyModel:
    def __init__(self, v_name=None):
        self.logger = logging.getLogger('game.model')

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
