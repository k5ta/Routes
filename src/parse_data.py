from json import loads, dumps
from collections import namedtuple


def decode_data(data):
    return loads(data, object_hook=lambda l: namedtuple('X', l.keys())(*l.values()))


def encode_data(solution):
    return dumps(solution._asdict(), indent=4)
