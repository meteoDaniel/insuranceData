from flask import Flask, request, jsonify
from datetime import datetime
from src.RequestHandler.requestHandler import prepare_data
from config import VALID_API_KEYS
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/request')
def my_route():
    if request.args.get('api_key', type=str) in VALID_API_KEYS:
        print(request.args.get('trip_duration', type=int))
        try:
            param = {
                'destination': request.args.get('destination', type=str),
                'trip_duration': request.args.get('trip_duration', type=int),
                'arrival': datetime.strptime(request.args.get('arrival', type=str), '%Y%m%d'),
                'criterion_num_days': request.args.get('criterion_num_days', type=int),
                'criterion_sunshine_hours_per_day': request.args.get('criterion_sunshine_hours_per_day', type=int)
            }
        except BaseException as e:
            return jsonify(e)

        prob, u = prepare_data(**param)

        return jsonify({'result': {'probability': {'value': round(prob.values[0], 2),
                                                      'unit': '%',
                                                      'type': 'float'},
                                      'Mean number of days where criterion is True in hist.Dataset': {'value': u.values[0],
                                                                       'unit': 'days',
                                                                       'type': 'float'}},
                           'request': {'destination': {'value': param['destination'],
                                                       'unit': 'None',
                                                       'type': 'str'},
                                       'trip_duration': {'value': param['trip_duration'],
                                                         'unit': 'days',
                                                         'type': 'int'},
                                       'arrival': {'value': param['arrival'].strftime('%Y%m%d'),
                                                   'unit': 'date',
                                                   'type': 'datetime'},
                                       'criterion_num_days': {'value': param['criterion_num_days'],
                                                              'unit': 'days',
                                                              'type': 'int'},
                                       'criterion_sunshine_hours_per_day': {'value': param['criterion_sunshine_hours_per_day'],
                                                                            'unit': 'hours',
                                                                            'type': 'int'}}})
    else:
        return jsonify('Wrong Api-key, please contact: daniel.lassahn@event-wetter.com')


if __name__ == '__main__':
    app.run()
