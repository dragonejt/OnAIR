
from src.data_driven_components.pomdp.pomdp_util import mass_load_data, stratified_sampling, split_by_lookback, dict_sort_data, list_to_dictionary_with_headers
from src.data_driven_components.pomdp.ppo import PPO
from src.data_driven_components.data_learners import DataLearner
import os


class PPOModel(DataLearner):

    def __init__(self, headers, window_size):
        """
        :param window_size: (int) length of time agent examines
        :param config_path: (optional String) path to PPO config
        """
        self.frames = {}
        self.headers = headers
        self.window_size = window_size
        self.agent = PPO()

    def apriori_training(self, data, use_stratified=True):
        split_data = split_by_lookback(data, self.window_size)
        data_train = dict_sort_data(self.agent.config, split_data)
        if use_stratified:
            split_data_train = stratified_sampling(self.agent.config, data_train)
        #Data should be in the format of { Time : [ 0, 1, 2] , Voltage : [5, 5, 5] } at this point
        self.agent.train_ppo(split_data_train, batch_size=1090)

    def update(self, frame):
        """
        :param frame: (list of floats) input sequence of len (input_dim)
        :return: None
        """
        self.frames = list_to_dictionary_with_headers(frame, self.headers, self.frames, self.window_size)

    def render_diagnosis(self):
        """
        System should return its diagnosis
        """

        #A stub for once ppo is fully integrated
        #reward, correct, actions, states = self.agent.diagnose_frames(self.frames)
        # potentially the the library-less runner?
        pass