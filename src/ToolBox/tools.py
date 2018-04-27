import sys
from src.DataHandler.aemetDataHandler import get_aemet_climate_data, aemet_data_processor, get_aemet_reference_data
from datetime import datetime, timedelta
from src.plot.plotCreatorPlotly import *
from src.time.timeHelper import daily_date_range, num_days_per_month, monthly_date_range
import pandas as pd
from src.Statistics.statisticalCalculations import mean_sunshine_duration_per_day,\
    monthly_to_daily_mean_sunduration, calculcate_mean_days_lower_than_table, calculcate_num_days_lower_than_table
from src.RequestHandler.requestHandler import prepare_data


def create_reference_table(year: int) -> pd.DataFrame:
    index = daily_date_range(datetime(year, 1, 1), datetime(year, 12, 31))
    duration_of_trip = np.arange(7, 22)
    return pd.DataFrame(index=index, columns=duration_of_trip)


def main():
    start_date = datetime(2000, 1, 1)
    end_date = datetime(2018, 4, 1)
    days = daily_date_range(start_date, end_date)
    from IPython import embed
    embed()
    prepare_data('PALMA_DE_MALLORCA', datetime(2018, 6, 9), 7, 1, 5)
    # -> The probability for a trip to PALMA_DE_MALLORCA with a duration of 7 days with arrival on 9.6.2018 for 1 day with less than 5 hours sunshine per day


    ########
    data = get_aemet_climate_data(start_date, end_date, 'B278')
    data = aemet_data_processor(data)
    n_missing_days = len(days)-len(data)
    year = 2018
    mean_days_lower_than = calculcate_mean_days_lower_than_table(data, year)
    path = '/home/d.lassahn/Schreibtisch/Wetterberatung/insuranceDataProject/data/probability_data/'
    mean_days_lower_than.to_pickle(path+'PALMA_DE_MALLORCA_'+str(year)+'.p')



    ###################
    reference_data = get_aemet_reference_data()
    mean_sun_per_day = mean_sunshine_duration_per_day(data.sol)
    interpolated_reference_data = monthly_to_daily_mean_sunduration(reference_data)
    reference_mean_sunshine_per_trip = create_reference_table()
    for day in reference_mean_sunshine_per_trip.index:
        for trip_duration in reference_mean_sunshine_per_trip.columns:
            reference_mean_sunshine_per_trip.loc[day, trip_duration] = interpolated_reference_data.loc[day:(day+timedelta(days=trip_duration)), :].mean().values[0]



if __name__ == '__main__':
    sys.exit(main())
