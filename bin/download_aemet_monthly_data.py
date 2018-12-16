from datetime import datetime
from src.DataHandler.aemetDataHandler import get_aemet_climate_data

start_date = datetime(1988, 2, 1)
end_date = datetime(1999, 12, 1)

get_aemet_climate_data(start_date,
                       end_date,
                       'B278')
