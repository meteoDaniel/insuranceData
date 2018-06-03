import sys
from src.DataHandler.dataServices import get_actual_stations_lists, stations_in_time, get_data
from src.geo.geoServices import stations_in_range
from datetime import datetime
from IPython import embed
from src.plot.plotCreatorPlotly import *
from src.Report.reportServices import create_report, create_report_table


def main():
    embed()

    lat = 53.598400
    lon = 8.047977
    start_date = datetime(2017, 1, 1)
    end_date = datetime(2017, 12, 31)
    type_list = ['wind_daily']
    measurement_type = 'wind_daily'
    distance = 40

    st_list = get_actual_stations_lists(measurement_type)
    st_list = stations_in_range(st_list, lat, lon, distance)
    st_list = stations_in_time(st_list, start_date, end_date)

    data = get_data(st_list, measurement_type, start_date, end_date)
    data[measurement_type] = data[measurement_type] * 3.6

    plot = PlotCreator('lines', len(st_list))
    for idx, id in enumerate(st_list.STATION_ID):
        plot.add_timeseries_to_plot(data[data.STATIONS_ID == int(id)].MESS_DATUM,
                                    data[data.STATIONS_ID == int(id)][measurement_type],
                                    idx,
                                    label_string=st_list[st_list.STATION_ID == id].NAME.values[0])
    plot.proceed_timeseries_plot('../../data/wind_gutachten_plot',
                                 'WIND MESSUNGEN IM RADIUS VON '+ str(distance) + 'km im Zeitraum von '+start_date.strftime('%d.%m.%Y') + ' bis ' + end_date.strftime('%d.%m.%Y'),
                                 ylab='Windspitzen in km/h', yrange=[0, 180], theme='white')
    measurement_table = create_report_table(data, st_list, measurement_type)

    create_report(start_date, end_date, lat, lon, measurement_table)


if __name__ == '__main__':
    sys.exit(main())
