import numpy as np


def deg2rad(deg):
    """
    :param deg:
    :return:
    """
    return deg * (np.pi / 180)


def getdistancefromlatloninkm(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray):
    """

    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return:
    """
    R = 6371
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(deg2rad(lat1)) * np.cos(deg2rad(lat2)) * np.sin(dLon / 2) * np.sin(
        dLon / 2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    d = R * c
    return d


def stations_in_range(station_list, lat, lon, range):

    distances = getdistancefromlatloninkm(lat, lon, station_list.LAT.values.astype('float'),
                                          station_list.LON.values.astype('float'))

    station_list['DISTANCE'] = distances
    station_list = station_list[station_list.DISTANCE <= range]

    return station_list