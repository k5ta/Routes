import json
from collections import namedtuple


def decode_data(data):
    conditions = json.loads(data, object_hook=lambda l: namedtuple('X', l.keys())(*l.values()))
    return conditions


def encode_data(solution):
    return json.dumps(solution._asdict(), indent=4, separators=(',', ': '))
