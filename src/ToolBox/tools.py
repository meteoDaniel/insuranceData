import sys
from datetime import datetime
from src.time.timeHelper import daily_date_range
from datetime import datetime
from src.RequestHandler.requestHandler import RequestHandler
from src.RequestHandler.requesHandlerServices import RequestConfig
from src.RestAPI.config import VALID_API_KEYS, BASE_PATH_DATA
import pandas as pd


def main():
    from IPython import embed
    embed()

    parsed_request = RequestConfig('PALMA_DE_MALLORCA',
                                   datetime(2018, 6, 10),
                                   7,
                                   2,
                                   5,
                                   BASE_PATH_DATA
                                   )

    prob_calculator = RequestHandler(parsed_request)
    prob = prob_calculator.calculate_poisson_probability()

if __name__ == '__main__':
    sys.exit(main())
