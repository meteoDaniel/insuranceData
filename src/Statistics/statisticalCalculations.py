import pandas as pd
from src.time.timeHelper import monthly_date_range, num_days_per_month, daily_date_range
import numpy as np
from datetime import datetime, timedelta


def create_reference_table(year: int) -> pd.DataFrame:
    index = daily_date_range(datetime(year, 1, 1), datetime(year, 12, 31))
    duration_of_trip = np.arange(7, 22)
    return pd.DataFrame(index=index, columns=duration_of_trip)


def mean_sunshine_duration_per_day(data: pd.DataFrame):
    return data.groupby([data.index.month, data.index.day]).mean()


def monthly_to_daily_mean_sunduration(reference_data: pd.DataFrame) -> pd.DataFrame:
    """
        calculates daily values of mean sunshine duration based on monthly climate data
    :param reference_data:
    :return:
    """
    days_per_month = np.zeros(12)

    for i in np.arange(1, 13):
        days_per_month[i - 1] = num_days_per_month(i)

    daily_sunshine_mean_reference = reference_data.I[:-1].values / days_per_month
    ref_data_sun = pd.DataFrame(daily_sunshine_mean_reference,
                                index=monthly_date_range(datetime(2018, 1, 1), datetime(2018, 12, 1)))
    ref_data_sun.index = ref_data_sun.index + pd.DateOffset(days=15)
    interpolated_reference_data = pd.DataFrame(index=daily_date_range(datetime(2018, 1, 1), datetime(2018, 12, 31)))
    interpolated_reference_data[0] = 0
    interpolated_reference_data = interpolated_reference_data + ref_data_sun
    interpolated_reference_data.iloc[0, 0] = (daily_sunshine_mean_reference[0] + daily_sunshine_mean_reference[-1]) / 2
    interpolated_reference_data.iloc[-1, 0] = (daily_sunshine_mean_reference[0] + daily_sunshine_mean_reference[-1]) / 2
    return interpolated_reference_data.interpolate(method='linear')


def calculcate_mean_days_lower_than_table(data: pd.DataFrame, year:int) -> pd.DataFrame:
    mean_days_lower_day_per_year = create_reference_table(year)
    for day in mean_days_lower_day_per_year.index:
        for trip_duration in mean_days_lower_day_per_year.columns:
            for day_of_trip in range(trip_duration):
                all_sunshine_hours = pd.concat([all_sunshine_hours,
                                                data[np.logical_and(data.index.month == (day+timedelta(days=day_of_trip)).month, data.index.day == (day+timedelta(days=day_of_trip)).day)].sol])
            num_of_years = len(data[np.logical_and(data.index.month == (day+timedelta(days=day_of_trip)).month, data.index.day == (day+timedelta(days=day_of_trip)).day)].sol)
            mean_days_lower = {'1': all_sunshine_hours[all_sunshine_hours <= 1.0].count() / num_of_years,
                              '2': all_sunshine_hours[all_sunshine_hours <= 2.0].count() / num_of_years,
                              '3': all_sunshine_hours[all_sunshine_hours <= 3.0].count() / num_of_years,
                              '4': all_sunshine_hours[all_sunshine_hours <= 4.0].count() / num_of_years,
                              '5': all_sunshine_hours[all_sunshine_hours <= 5.0].count() / num_of_years,
                              '6': all_sunshine_hours[all_sunshine_hours <= 6.0].count() / num_of_years}
            mean_days_lower_day_per_year.loc[day, trip_duration] = [mean_days_lower]
            all_sunshine_hours = pd.DataFrame()
    return mean_days_lower_day_per_year


def calculcate_num_days_lower_than_table(data: pd.DataFrame) -> pd.DataFrame:
    num_days_lower_day_per_year = create_reference_table()
    for day in num_days_lower_day_per_year.index:
        for trip_duration in num_days_lower_day_per_year.columns:
            for day_of_trip in range(trip_duration):
                all_sunshine_hours = pd.concat([all_sunshine_hours,
                                                data[np.logical_and(data.index.month == (day+timedelta(days=day_of_trip)).month, data.index.day == (day+timedelta(days=day_of_trip)).day)].sol])
            mean_days_lower = {'1': all_sunshine_hours[all_sunshine_hours <= 1.0].count(),
                              '2': all_sunshine_hours[all_sunshine_hours <= 2.0].count(),
                              '3': all_sunshine_hours[all_sunshine_hours <= 3.0].count(),
                              '4': all_sunshine_hours[all_sunshine_hours <= 4.0].count(),
                              '5': all_sunshine_hours[all_sunshine_hours <= 5.0].count(),
                              '6': all_sunshine_hours[all_sunshine_hours <= 6.0].count()}
            num_days_lower_day_per_year.loc[day, trip_duration] = [mean_days_lower]
            all_sunshine_hours = pd.DataFrame()
    return num_days_lower_day_per_year


def poisson_probability(u, n):
    return ((u ** n) / np.prod(range(1, n+1))) * np.exp(-u)
