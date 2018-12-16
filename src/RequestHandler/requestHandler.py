from src.Statistics.statisticalCalculations import poisson_probability
import pandas as pd
import numpy as np


class RequestHandler:
    """
        this class procedes a request about the probability of an event
        with the information from the request config
    """
    def __init__(self, request_config):
        self.request_config = request_config

    def __get_prepared_data(self):
        """
            get the right file from the file system where the pre calculated values are in a
            pd.DataFrame. The DataFrame contains dictionaries
        """
        self.data = pd.read_pickle('{base_path}{destination}_{year}.p'.format(
            base_path=self.request_config['base_path_data'],
            destination=self.request_config['destination'],
            year=self.request_config['arrival'].strftime('%Y')
        ))

    def receive_mean_amount_days_lt(self):
        """
            provides the pre calculated mean amount of days that are lower than
            the criterion in request_config
        """
        self.__get_prepared_data()
        self.mean_amount_days_lt = self.data.loc[
            self.request_config['arrival'],
            self.request_config['trip_duration']][0][str(
            self.request_config['criterion_sunshine_hours_per_day'])]

    def calculate_poisson_probability(self):
        """
            return the cumulated poisson probability for all requested days
        """
        self.receive_mean_amount_days_lt()
        prob = []
        for num_day in range(1, self.request_config['criterion_num_days']+1):
            prob.append(poisson_probability(self.mean_amount_days_lt, num_day))
        return np.prod(np.array(prob))