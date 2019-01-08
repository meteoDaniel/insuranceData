import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from datetime import datetime, timedelta
import plotly.graph_objs as go
ACCESS_TOKEN_MAPBOX = 'pk.eyJ1IjoibWV0ZW9kYW5pZWwiLCJhIjoiY2pqOXZ1eWFvMnFvbj' \
                      'N2b2g5M3NkN3RjaCJ9.R4gXCX8qzxBwbj7eeMoJlQ'


def generate_table(dataframe, max_rows=10):
    return html.Table(

        # Header
        [html.Thead(html.Tr([html.Th(col) for col in dataframe.columns]))] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        , className='ui striped table')


def generate_html_layout(locations: list):
    return html.Div([

        html.Div([
            html.Div([
                html.A(
                    [],
                    href="#",
                    className="header item"
                ),
                html.A(
                    ['Insurance Data Calculator'],
                    href="#",
                    className="header item"
                )

            ], className="ui container")
        ], className="ui fixed inverted menu"),

        html.Div([
            html.Div([
                html.Div([
                    html.H1(children='Probability calculation sunshine guarantee',
                            style={'align': 'center'}),
                ], className="six wide column"),
                html.Div([
                    html.Img(src="assets/ewb_logo.png",
                             className="ui small image")
                    # dcc.RadioItems(
                    #     options=[
                    #         {'label': 'Dark Theme', 'value': 'dark'},
                    #     ],
                    #     value='white', className='ui radio checkbox',
                    #     style={'marginTop': 10}
                    # )
                ], className="six wide column"),

            ], className="two colum row"),

            html.Div([
                html.Div(
                    [html.P('Destination'),
                     dcc.Dropdown(
                         id='select-destination',
                         options=[{'label': i, 'value': i} for i in locations],
                         value=locations[0]
                     ),
                     ], className="three wide column"),
                html.Div(
                    [
                        html.P('Anreise Datum'),
                        html.Div(style={'fontSize': 16,
                                        'border-radius': 10,
                                        'height': 50}, children=
                                dcc.DatePickerSingle(
                                     id='date-picker',
                                     min_date_allowed=datetime(2018, 1, 1),
                                     max_date_allowed=datetime(2019, 1, 1),
                                     initial_visible_month=datetime.now(),
                                     display_format='DD.MM.YYYY'
                                 ))
                    ], className="three wide column"),
                html.Div(
                    [html.P('Reisedauer'),
                        dcc.Dropdown(
                         id='trip-duration',
                         options=[{'label': i, 'value': i} for i in range(7, 22)],
                         value=7
                     ),], className="three wide column"),
                html.Div(
                    [html.P('Sonnenscheindauer pro Tag'),
                     dcc.Dropdown(
                         id='criterion-sunshine-hours-day',
                         options=[{'label': i, 'value': i} for i in
                                  range(2, 8)],
                         value=4
                     ), ], className="three wide column"),
                html.Div(
                    [html.P('Anzahl Tage mit mind.'),
                     dcc.Dropdown(
                         id='criterion-num-days',
                         options=[{'label': i, 'value': i} for i in
                                  range(2, 20)],
                         value=2
                     ), ], className="three wide column")

            ], className="five column row"),
            html.Div([
                html.Div(
                    [html.P('Ergebnis'),
                     html.Div([], id='solution', className="ui text"
                     ), ], className="three wide column")

            ], className="one column row"),

        ], className="ui padded grid")
    ])