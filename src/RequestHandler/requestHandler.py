from src.Statistics.statisticalCalculations import poisson_probability
import pandas as pd
import datetime


def prepare_data(destination: str, start_date: datetime.datetime,
                 trip_duration: int, criterion_num_days: int, criterion_sunshine_day: int):
    """

    :param destination:
    :param start_date:
        datetime.datetime
    :param trip_duration:
    :param criterion_num_days:
        Number of days where the criterion should be true
    :param criterion_sunshine_day:
        Criterion for Sunshine hours per day
        [1: <=1, 2:<=2, 3:<=3, 4:<=4, 5:<=5, 6:<=6]
    :return:
    """
    path = '/home/d.lassahn/Schreibtisch/Wetterberatung/insuranceDataProject/data/probability_data/'
    mean_days_lower_than = pd.read_pickle(path+destination + start_date.strftime('%Y') +'.p')
    u = mean_days_lower_than.loc[start_date, trip_duration][0][str(criterion_sunshine_day)]
    prob = poisson_probability(u, criterion_num_days) * 100

    return prob, u
