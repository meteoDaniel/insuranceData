import dash
import os
from datetime import datetime
from src.dash.layoutInsuranceRequest import generate_html_layout
from src.RequestHandler.requestHandler import RequestHandler
from src.RequestHandler.requesHandlerServices import RequestConfig

app = dash.Dash()

locations = ['PALMA_DE_MALLORCA']
current_dir = os.getcwd()
app.layout = generate_html_layout(locations)
BASE_PATH_DATA = current_dir+"/../../data/probability_data/"



@app.callback(dash.dependencies.Output('solution', 'children'),
              [dash.dependencies.Input('date-picker', 'date'),
               dash.dependencies.Input('trip-duration', 'value'),
               dash.dependencies.Input('select-destination', 'value'),
               dash.dependencies.Input('criterion-sunshine-hours-day', 'value'),
               dash.dependencies.Input('criterion-num-days', 'value')])
def calculate_probability(trip_start_date, trip_duration, destination,
                          crit_sun_hours_day, crit_num_days):
    parsed_request = RequestConfig(destination,
                                   datetime.strptime(trip_start_date, '%Y-%m-%d'),
                                   trip_duration,
                                   crit_num_days,
                                   crit_sun_hours_day,
                                   BASE_PATH_DATA
                                   )
    prob_calculator = RequestHandler(parsed_request)
    prob = prob_calculator.calculate_poisson_probability()

    return "Die Wahrscheinlichkeit beträgt " + str(round(prob*100, 2)) + '%'


if __name__ == '__main__':
    app.run_server(debug=False, host="0.0.0.0", port=80)