import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from src.time.timeHelper import monthly_date_range
import time

def loader(url_request, output):
    os.system('wget ' + url_request + ' -O ' + output)





