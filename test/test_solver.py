import unittest
import src.solver as solver
import src.parse_data as parser
import filecmp
import sys
import os


class TestSolver(unittest.TestCase):
    answer = parser.decode_data('{ "bypass": [] }')
    answer.bypass.extend([{'c': '00:00'}, {'a': '00:05'}, {'b': '00:15'}, {'c': '00:27'}])

    def setUp(self):
        self.original_stdout = sys.stdout
        sys.stdout = None
        if not os.path.isfile("temp.ans"):
            with open("temp.ans", "w+") as f:
                pass

    def tearDown(self):
        sys.stdout = self.original_stdout
        if os.path.isfile("temp.ans"):
            os.remove("temp.ans")

    def test_create_answer(self):
        answer = solver.calculate_solution(solver.init_data("test_inputs/test_1.dat"))
        solver.create_answer("temp.ans", answer)
        self.assertTrue(filecmp.cmp("test_outputs/test_1.ans", "temp.ans", shallow=False))

    def test_solve_problem(self):
        solver.solve_problem("test_inputs/test_2.dat", "temp.ans")
        self.assertTrue(filecmp.cmp("test_outputs/test_2.ans", "temp.ans", shallow=False))
