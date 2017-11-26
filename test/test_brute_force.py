import unittest
import src.brute_force as brute
import src.parse_data as parser


class Conditions(object):
    def __init__(self):
        pass


class TestBruteForce(unittest.TestCase):
    conditions = Conditions()
    conditions.initial = "c"
    conditions.time = "00:00"
    conditions.vertices = ["a", "b", "c"]
    conditions.graph = [
        [float("Inf"), 10, 5],
        [10, float("Inf"), 12],
        [5, 12, float("Inf")]
    ]

    def test_get_answer(self):
        answer = parser.decode_data('{ "bypass": [] }')
        answer.bypass.extend([{'c': '00:00'}, {'a': '00:05'}, {'b': '00:15'}, {'c': '00:27'}])
        self.assertEqual(brute.get_exact_solution(self.conditions), answer)

    def test_full_search(self):
        self.assertEqual(set(brute.full_search(self.conditions.graph, self.conditions.vertices,
                                               self.conditions.initial)), {0, 1, 2})

    def test_route_length(self):
        self.assertEqual(brute.get_route_length(self.conditions.graph, [0, 1, 2]), 27)
