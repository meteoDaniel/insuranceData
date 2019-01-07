from datetime import datetime
from src.DataHandler.aemetDataHandler import get_aemet_climate_data, aemet_data_processor
from src.Statistics.statisticalCalculations import calculcate_mean_days_lower_than_table
import pickle
start_date = datetime(1988, 1, 1)
end_date = datetime(2018, 3, 1)

data = get_aemet_climate_data(start_date,
                              end_date,
                              'B278')
data = aemet_data_processor(data)
from IPython import embed
embed()
calculated = calculcate_mean_days_lower_than_table(data,
                                                   2018)

pickle.dump(calculated,
            open('/Users/imac/Desktop/Wetterberatung/insuranceDataProject/data/'
                 'probability_data/PALMA_DE_MALLORCA_2018.p', 'wb'))
