from flask import Flask, request
from datetime import datetime
from src.RequestHandler.requestHandler import prepare_data
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/request')
def my_route():
    try:
        param = {
            'destination': request.args.get('destination', default='PALMA_DE_MALLORCA', type=str),
            'trip_duration': request.args.get('trip_duration', default=7, type=int),
            'start_date': datetime.strptime(request.args['trip_start'], '%Y%m%d'),
            'criterion_num_days': request.args.get('criterion_num_days', default=1, type=int),
            'criterion_sunshine_day': request.args.get('criterion_sunshine_day', default=5, type=int)
        }
    except BaseException as e:
        return json.dumps(e)

    prob, u = prepare_data(**param)

    return json.dumps({'Probability': prob.values[0],
                      'Mean of Days criterion is True': u.values[0]})


if __name__ == '__main__':
    app.run()
