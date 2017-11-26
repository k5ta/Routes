import unittest
import src.littles_algorithm as algo
import src.parse_data as parser


class SomeObject(object):
    def __init__(self):
        pass


def get_solution_template():
    return parser.decode_data('{ "bypass": [] }')


class TestLittlesAlgorithm(unittest.TestCase):
    conditions = SomeObject()
    conditions.initial = "a"
    conditions.time = "00:00"
    conditions.clients = ["b", "c"]
    conditions.vertices = ["a", "b", "c"]
    conditions.graph = [
        [float("Inf"), 5, 100],
        [100, float("Inf"), 15],
        [10, 100, float("Inf")],
    ]

    def test_best_answer_and_solutions(self):
        solution = get_solution_template()
        solution.bypass.extend([{"a": "00:00"}, {"b": "00:05"}, {"c": "00:20"}, {"a": "00:30"}])
        # with such conditions, the algorithm gives an unambiguous result
        self.assertEqual(algo.get_solution(self.conditions), solution)
        solution_template = get_solution_template()
        solution_template.bypass.extend([{"a": "00:00"}])
        answers = [{0: 1, 1: 2, 2: 0, 'additive_time': 30}, {0: 2, 2: 1, 1: 0, 'additive_time': 300}]
        self.assertEqual(algo.get_best_answer(answers, solution_template, self.conditions), solution)

    def test_calculate(self):
        some_answer = [{0: 1, 1: 2, 2: 0, 'additive_time': 30}, {0: 1, 1: 2, 2: 0, 'additive_time': 30}]
        self.assertEqual(algo.calculate(self.conditions), some_answer)

    def test_small_matrix(self):
        full_matrix = SomeObject()
        full_matrix.rows = ["a"]
        full_matrix.cols = ["b"]
        full_matrix.matrix = [[float("Inf")]]
        answers = algo.small_matrix_answer(full_matrix, [])
        self.assertEqual(answers, [])
        full_matrix.matrix = [[10]]
        answers = algo.small_matrix_answer(full_matrix, [])
        self.assertEqual(answers, [{"a": "b"}])
        answers = algo.small_matrix_answer(full_matrix, [{"b": "a"}])
        self.assertEqual(answers, [{"a": "b", "b": "a"}])

    def test_prepare_matrix(self):
        full_matrix = SomeObject()
        full_matrix.matrix = [
            [float("Inf"), 1, 5],
            [3, float("Inf"), 8],
            [2, 11, float("Inf")],
        ]
        full_matrix.additive_time = 0
        algo.prepare_matrix(full_matrix)
        self.assertEqual(full_matrix.matrix, [
            [float("Inf"), 0, 0],
            [0, float("Inf"), 1],
            [0, 9, float("Inf")],
        ])
        self.assertEqual(full_matrix.additive_time, 10)

        full_matrix.matrix = [
            [0, 0],
            [1, float("Inf")],
        ]
        full_matrix.additive_time = 0
        algo.prepare_matrix(full_matrix)
        self.assertEqual(full_matrix.matrix, [
            [float("Inf"), 0],
            [0, float("Inf")],
        ])
        self.assertEqual(full_matrix.additive_time, 1)

    def test_zeros_and_coefficients(self):
        some_matrix = [
            [float("Inf"), 0, 0],
            [2, float("Inf"), 2],
            [3, 0, float("Inf")],
        ]
        zeros = algo.find_zeros(some_matrix)
        self.assertEqual(zeros, [(0, 1), (0, 2), (2, 1)])
        coefficients = algo.calculate_coefficients(some_matrix, zeros)
        self.assertEqual(coefficients, [(0, (0, 1)), (2, (0, 2)), (3, (2, 1))])
