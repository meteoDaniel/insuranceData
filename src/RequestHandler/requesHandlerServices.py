import typing
from datetime import datetime

RequestConfig = typing.NamedTuple('Config', [
    ('destination', str),
    ('arrival', datetime),
    ('trip_duration', int),
    ('criterion_num_days', int),
    ('criterion_sunshine_hours_per_day', list),
    ('base_path_data', str),
])