from src.DataHandler.aemetDataBaseConfig import *
from src.time.timeHelper import monthly_date_range
from src.DataHandler.dataServices import loader
import pandas as pd
import time
import os
from datetime import datetime, timedelta


def aemet_data_processor(data: pd.DataFrame) -> pd.DataFrame:
    """
        optimzes the aemet data table
    """
    data = data.drop_duplicates('fecha')
    data.index = pd.to_datetime(data.fecha, format='%Y-%m-%d')
    data['sol'] = [x.replace(',', '.') for x in data['sol'].values.astype(str)]
    data['sol'] = data['sol'].astype(float)
    return data


def get_aemet_climate_data(start_date: datetime,
                           end_date: datetime,
                           national_station_id: str) -> pd.DataFrame:
    """
        handles table creation and download for aemet climate data
    """
    station_id_str = '/estacion/' + national_station_id
    request_json = 'server_answer.json'
    dates = monthly_date_range(start_date, end_date)
    data = pd.DataFrame()
    for month in dates:
        outfile = AEMET_STORAGE + 'AEMET_CLIM_DAILY_' + national_station_id +\
                  '_' + month.strftime('%Y%m')
        if os.path.isfile(outfile):
            try:
                data = pd.concat([data, pd.read_json(outfile)])
            except ValueError:
                continue
        else:
            url_request = AEMET_BASE_URL + month.strftime('%Y-%m-%dT00:00:00UTC') + \
                          AEMET_MID_URL_2 + (month+timedelta(days=32)).replace(
                day=1).strftime('%Y-%m-%dT00:00:00UTC') + station_id_str \
                          + AEMET_MID_URL + AEMET_API_KEY
            loader(url_request, request_json)
            try:
                answer = pd.read_json(request_json, typ='series')
            except ValueError:
                continue
            loader(answer.datos, outfile)
            data = pd.concat([data, pd.read_json(outfile)])
            time.sleep(60)
    return data


def get_aemet_reference_data():
    """ parse in the climate data reference table from aemet """
    return pd.read_csv(AEMET_STORAGE + 'reference_data/'
                                       'valoresclimatologicos_palma-de-'
                                       'mallorca-aeropuerto.csv',
                       header=1)
