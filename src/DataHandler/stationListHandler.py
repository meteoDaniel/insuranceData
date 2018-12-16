import pandas as pd
from src.DataHandler.aemetDataBaseConfig import AEMET_STATION_LIST


def parse_aemet_stationlist():
    """
        create a csv from AEMET json station list
    """
    station_list = pd.read_json(AEMET_STATION_LIST, encoding='ISO-8859-1')
    station_list.columns = ['HEIGHT_ABOVE_NN',
                            'NATIONAL_ID',
                            'WMO_ID',
                            'LATITUDE',
                            'LONGITUDE',
                            'STATION_NAME',
                            'REGION']
    station_list['WMO_ID'] = [i.zfill(6) for i in station_list['WMO_ID']]
    station_list['LATITUDE'] = [float(i[:2]+'.'+i[3:6]) for i in station_list['LATITUDE']]
    station_list['LONGITUDE'] = [float(i[:2]+'.'+i[3:6]) for i in station_list['LONGITUDE']]
    station_list['COUNTRY_SHORT'] = 'ES'
    station_list['COUNTRY'] = 'SPAIN'

    station_list.to_csv('/data/stations_list/stations_spain.csv', sep=';')