import unittest
import src.data_validation as validation


class Conditions(object):
    def __init__(self):
        pass


class TestDataValidation(unittest.TestCase):
    conditions = Conditions()
    conditions.initial = ""
    conditions.time = ""
    conditions.clients = ""
    conditions.vertices = ""
    conditions.graph = ""

    def test_initials(self):
        self.assertEqual(validation.check_initials(self.conditions), "wrong initial vertex")
        self.conditions.initial = "c"

        self.assertEqual(validation.check_initials(self.conditions), "wrong initial time")
        self.conditions.time = "10:00"

        self.assertEqual(validation.check_initials(self.conditions), "wrong clients array")
        self.conditions.clients = []

        self.assertEqual(validation.check_initials(self.conditions), "the clients array shouldn't be empty")
        self.conditions.clients = ["a", "b"]

        self.assertEqual(validation.check_initials(self.conditions), "wrong vertices array")
        self.conditions.vertices = ["a", "b", "c", "d"]

        self.assertEqual(validation.check_initials(self.conditions),
                         "the length of the clients array should be 1 less than the length of the vertices array")
        self.conditions.vertices = ["a", "b", "c"]

        self.assertEqual(validation.check_initials(self.conditions), None)

    def test_matrix(self):
        self.conditions.clients = ["a", "c"]
        self.assertEqual(validation.check_matrix(self.conditions),
                         "the vertices array should be like clients array with initial vertex")

        self.conditions.clients = ["a", "b", "c"]
        self.assertEqual(validation.check_matrix(self.conditions),
                         "the number of rows of the matrix must be equal to the length of the vertices array")

        self.conditions.graph = [
            [float("Inf"), 10, 5],
            [10, float("Inf"), 12],
        ]
        self.assertEqual(validation.check_matrix(self.conditions),
                         "the number of rows of the matrix must be equal to the length of the vertices array")

        self.conditions.graph.append([5, 12])
        self.assertEqual(validation.check_matrix(self.conditions),
                         "the length of each row of the matrix must be equal to the length of the vertices array")

    def test_matrix_values(self):
        self.assertEqual(1, 1)

        self.conditions.graph = [
            ["-", 10, -5],
            [10, "-", 12],
            [5, 12, "-"],
        ]
        self.assertEqual(validation.check_matrix_values(self.conditions.graph),
                         "the distance between the vertices must be non-negative")

        self.conditions.graph[0][2] = 5
        validation.check_matrix_values(self.conditions.graph)
        self.assertEqual([
            [float("Inf"), 10, 5],
            [10, float("Inf"), 12],
            [5, 12, float("Inf")],
        ], self.conditions.graph)

        self.conditions.graph[0][2] = "some string"
        self.assertEqual(validation.check_matrix_values(self.conditions.graph),
                         "wrong time format in the matrix. Please, set all distances in minutes")
