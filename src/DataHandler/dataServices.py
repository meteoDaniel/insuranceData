import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from src.time.timeHelper import monthly_date_range
import time

url_of_lists = {"wind_mean_hourly" : "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/wind/recent/FF_Stundenwerte_Beschreibung_Stationen.txt",
 "wind_daily":"ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/KL_Tageswerte_Beschreibung_Stationen.txt",
 "wind_vmax":"ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/zehn_min_fx_Beschreibung_Stationen.txt"}

url_of_data = {"wind_mean_hourly": {"path_recent": 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/wind/recent/stundenwerte_FF_',
                                    "path_historical" : 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/wind/historical/stundenwerte_FF_',
                                    "zip": 'stundenwerte_FF_',
                                    "all_names": ['STATIONS_ID', 'MESS_DATUM', 'QN_3',
                                                  'V_MEAN_HOUR', 'V_DIRECTION_MEAN_HOUR', 'eor'],
                                    "names": ['STATIONS_ID', 'MESS_DATUM',
                                              'V_MEAN_HOUR', 'V_DIRECTION_MEAN_HOUR'],
                                    "date_format": '%Y%m%d%H'
               },

               "wind_daily": {"path_recent": 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/recent/tageswerte_KL_',
                              "path_historical": 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/kl/historical/tageswerte_KL_',
                              "zip": 'tageswerte_KL_',
                              "all_names": ['STATIONS_ID', 'MESS_DATUM', 'QN_3', 'V_MAX_DAY', 'V_MEAN_DAY', 'QN_4',
                                            'PRECIP_SUM_DAY', 'PRECIP_TYPE', 'SDK', 'SNOW_DEPTH_DAY', 'NM', 'VPM', 'PM',
                                            'TEMPERATURE_MEAN_DAY', 'UPM', 'TEMPERATURE_MAX_DAY', 'TEMPERATURE_MIN_DAY',
                                            'TEMPERATURE_GROUND_MIN_DAY', 'eor'],
                              "names": ['STATIONS_ID', 'MESS_DATUM',
                                        'V_MAX_DAY', 'V_MEAN_DAY'],
                              "date_format": '%Y%m%d'},
               "wind_vmax": {"path_recent": 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/extreme_wind/recent/10minutenwerte_extrema_wind_',
                              "path_historical": 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/10_minutes/extreme_wind/historical/10minutenwerte_fx_',
                              "zip": '10minutenwerte_extrema_wind_',
                              "all_names": ['STATIONS_ID', 'MESS_DATUM', 'QN', 'wind_vmax', 'FNX_10', 'FMX_10', 'DX_10'],
                              "names": ['STATIONS_ID', 'MESS_DATUM',
                                        'wind_vmax'],
                             "date_format": '%Y%m%d%H%M'
               }}
def get_actual_stations_lists(type):

    url = url_of_lists[type]
    path_to_store = "../../data/stationsliste_"+type+".txt"
    os.system("wget " + url + "  -O " + path_to_store)

    return create_stations_dataframe(path_to_store)


def create_stations_dataframe(file_name):
    with open(file_name, errors='ignore') as f:
        station_data_klima = f.readlines()[2:-1]

    st_dataframe = pd.DataFrame(index=range(len(station_data_klima)), columns=['STATION_ID',
                                                                                     'BEGIN',
                                                                                     'END',
                                                                                     'HEIGHT',
                                                                                     'LAT',
                                                                                     'LON',
                                                                                     'NAME'])

    for i in range(len(station_data_klima)):
        st_dataframe.loc[i, 'STATION_ID'] = station_data_klima[i][:5].strip()
        st_dataframe.loc[i, 'BEGIN'] = datetime.strptime(station_data_klima[i][6:15].strip(), '%Y%m%d')
        st_dataframe.loc[i, 'END'] = datetime.strptime(station_data_klima[i][15:23].strip(), '%Y%m%d')
        st_dataframe.loc[i, 'HEIGHT'] = station_data_klima[i][23:38].strip()
        st_dataframe.loc[i, 'LAT'] = station_data_klima[i][42:50].strip()
        st_dataframe.loc[i, 'LON'] = station_data_klima[i][53:60].strip()
        st_dataframe.loc[i, 'NAME'] = station_data_klima[i][61:99].strip()

    return st_dataframe


def loader(url_request, output):
    os.system('wget ' + url_request + ' -O ' + output)


def stations_in_time(stations_list, start_date, end_date):
    return stations_list[np.logical_and(stations_list.BEGIN <= start_date,
                                        stations_list.END >= end_date)]


def get_data(st_list, type, start_date, end_date):
    today = datetime.utcnow()
    requested_data = pd.DataFrame()
    for idx, id in enumerate(st_list.STATION_ID):
        if start_date.year == today.year:

            url_file = url_of_data[type]['path_recent'] + id.zfill(5) + '_akt.zip'
            url_zip = url_of_data[type]['zip'] + id.zfill(5) + '_akt.zip'

        else:
            url_file = url_of_data[type]['path_historical'] + id.zfill(5) + \
                       '_' + str(st_list[st_list.STATION_ID == id].BEGIN.strftime('%Y%m%d')) + '_' + \
                       str(datetime(today.year - 1, 12, 31).strftime('%Y%m%d')) + '_hist.zip'
            url_zip = url_of_data[type]['zip'] + id.zfill(5) + \
                      '_' + str(st_list[st_list.STATION_ID == id].BEGIN.strftime('%Y%m%d')) + '_' + \
                      str(datetime(today.year - 1, 12, 31).strftime('%Y%m%d')) + '_hist.zip'

        os.system('wget ' + url_file)
        os.system('unzip ' + url_zip)
        os.system('mv produkt_* akt_data.txt')
        dateparse = lambda x: pd.datetime.strptime(x, url_of_data[type]['date_format'])
        data_klima = pd.read_csv('akt_data.txt', delimiter=';', skiprows=2, names=url_of_data[type]['all_names'],
                                 parse_dates=['MESS_DATUM'], date_parser=dateparse)

        data_klima = data_klima.loc[:, url_of_data[type]['names']]
        requested_data = pd.concat([requested_data,
                                    data_klima[np.logical_and(data_klima.MESS_DATUM >= start_date.replace(hour=0),
                                                              data_klima.MESS_DATUM <= end_date.replace(hour=0)+timedelta(days=1))]])
        os.system('rm akt_data.txt')
        os.system('rm tageswerte_*')
        os.system('rm Stationsmetadaten*')
        os.system('rm Protokoll_Fehldaten*')
        os.system('rm *.html')
        os.system('rm *.zip')
        os.system('rm Metadaten*')


    return requested_data





