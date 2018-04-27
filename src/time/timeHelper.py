from calendar import monthrange
from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import time
from dateutil.parser import parse

# class TimeHelper:
#
#     def __init__(self, database, host='ew'):
#         self.__connect = self.__get_connect(database, host)
#         self.__cursor = self.__get_cursor(self.__connect)


def cross_timeseries(series1, series2):
    """
        this function is depricated in evaluation part of the code ,
        please use cross_time_index
        only keep values that are in both timeseries with same timestamp
    :param series1:
    [values, datetime]
    :param series2:
    [values, datetime]
    :return:
    [values, datetime] , [values, datetime]

    """

    ts_new1 = []
    val_new1 = []

    ts_new2 = []
    val_new2 = []

    for i in range(len(series1[1])):
        # for j in range(len(series2[1])):
        if series1[1][i] in series2[1]:
            ts_new1.append(series1[1][i])
            val_new1.append(series1[0][i])
            ts_new2.append(series2[1][series2[1].index(series1[1][i])])
            val_new2.append(series2[0][series2[1].index(series1[1][i])])

    return [val_new1, ts_new1], [val_new2, ts_new2]


def cross_time_index(df1, df2):
    """
        cross Index of Dataframe or Series to get same timestamps in both variables
    :param df1:
        pandas.Dataframe or pd.Series
    :param df2:
        pandas.Dataframe or pd.Series
    :return:
    """
    series = pd.core.series.Series
    crossed_index = df1.index.intersection(df2.index)

    if type(df1) == series and type(df2) == series:
        df1 = df1[crossed_index]
        df2 = df2[crossed_index]
    elif type(df1) == series and type(df2) != series:
        df1 = df1[crossed_index]
        df2 = df2.loc[crossed_index, :]
    elif type(df1) != series and type(df2) == series:
        df1 = df1.loc[crossed_index, :]
        df2 = df2[crossed_index]
    else:
        df1 = df1.loc[crossed_index, :]
        df2 = df2.loc[crossed_index, :]
    return df1, df2


def monthdelta(date1, date2):
    """
        get number of months between date1 and date2
    :param date1:
    :param date2:
    :return:
    """
    delta = 0
    while True:
        mdays = monthrange(date1.year, date1.month)[1]
        date1 += timedelta(days=mdays)
        if date1 <= date2:
            delta += 1
        else:
            break
    return delta


def yearly_date_range(date1: datetime, date2: datetime):
    """
        creates a numpy.array of yearly timestamp between date1 and date2 (with month and hour of date1)
    :param date1:
        datetime.datetime
    :param date2:
        datetime.datetime
    :return:
        np.array of datetime.datetime objects
    """
    ctr = date1
    list = [ctr]

    while ctr < date2:
        ctr += timedelta(days=366)
        list.append(datetime(ctr.year, date1.month, 1))
        ctr = datetime(ctr.year, date1.month, 1)
    return list


def monthly_date_range(date1: datetime, date2: datetime):
    """
        creates a numpy.array of monthly timestamp between date1 and date2 (with day and hour of date1)
    :param date1:
        datetime.datetime
    :param date2:
        datetime.datetime
    :return:
        np.array of datetime.datetime objects
    """
    ctr = date1
    list = [ctr]

    while ctr <= date2:
        ctr += timedelta(days=32)
        list.append(datetime(ctr.year, ctr.month, 1))
    return list


def daily_date_range(date1, date2):
    """
        creates a numpy.array of daily timestamp between date1 and date2
    :param date1:
        datetime.datetime
    :param date2:
        datetime.datetime
    :return:
        np.array of datetime.dateteim objects
    """
    num_days = (date2-date1).days
    return np.array([datetime(date1.year, date1.month, date1.day, 0)+timedelta(days=i) for i in range(num_days)])


def time_string2dt(time_string: str)-> datetime:
    """
        converts several time strings to datetime object like php function strtotime
    :param time_string:
    :return:
    """
    return parse(time_string, fuzzy=True)


def latest_synop_time()-> datetime:
    """
    calculates the latest synoptic date [00, 06, 12, 18]
    :return:
     datetime object
    """
    utc = datetime.utcnow()

    if utc.hour < 1:
        utc = utc - timedelta(days=1)
        utc = utc.replace(hour=18)
    elif utc.hour < 7:
        utc = utc.replace(hour=0)
    elif utc.hour < 13:
        utc = utc.replace(hour=6)
    elif utc.hour < 19:
        utc = utc.replace(hour=12)
    else:
        utc = utc.replace(hour=18)

    utc.replace(minute=0, second=0)
    return utc


def from_gfs_archive(requested_time):
    """
    :param requested_time:
        datetime object of requested Data
    :return:
    """
    return requested_time < datetime.utcnow() - timedelta(days=2)


def leading_zeros(fct_hour, num_leading_zeros):

    return str(fct_hour).zfill(num_leading_zeros)


def quarterhourly_timestamp_range(start, ndays):
    return np.array([start + timedelta(minutes=15*i) for i in range(ndays*96)])


def num_days_per_month(month: int):
    if month == 12:
        return (datetime(2013, 1, 1) - datetime(2012, month, 1)).days
    else:
        return (datetime(2012, month+1, 1) - datetime(2012, month, 1)).days