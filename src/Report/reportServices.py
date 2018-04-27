from jinja2 import Environment, FileSystemLoader
import numpy as np

def create_report(start_date, end_date, lat, lon, measurement_table):
    loader=FileSystemLoader('/home/d.lassahn/Schreibtisch/Wetterberatung/insuranceDataProject/')
    env = Environment(loader=loader)
    template = env.get_template("insurance_request_dwd_report.html")
    template_vars = {"report_type" : "Wind",
                     "start": start_date.strftime('%d.%m.%Y'),
                     "end": end_date.strftime('%d.%m.%Y'),
                     "lat":lat,
                     "lon": lon,
                     "plot_measurements": "/home/d.lassahn/Schreibtisch/Wetterberatung/insuranceDataProject/data/wind_gutachten_plot.html",
                     "table_entries": measurement_table}
    html_out = template.render(template_vars)
    with open("../../data/report.html", "w") as report_file:
        report_file.write(html_out)


def create_report_table(data, st_list, type):
    html_str=''
    for idx, id in enumerate(st_list.STATION_ID):
        html_str += '<tr ><td>' +str(st_list[st_list.STATION_ID == id].NAME.values[0])+ \
                    '</td ><td>' +str(round(st_list[st_list.STATION_ID == id].DISTANCE.values[0]))+\
                    ' </td ><td>' +str(data[data.STATIONS_ID == int(id)][type].max())+ \
                    '</td ><td>' +data.iloc[np.where(data[data.STATIONS_ID == int(id)][type]== data[data.STATIONS_ID == int(id)][type].max())[0][0], 1].strftime('%d.%m.%Y %H:%M')+\
                    ' </td ></tr>'
    return html_str


