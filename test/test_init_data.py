import unittest
import os
import src.solver as solver
from json import JSONDecodeError


class TestInitData(unittest.TestCase):
    def test_file_not_exist(self):
        filename = "some_name_for_file_that_is_not_there"
        if not os.path.isfile(filename):
            self.assertRaises(FileNotFoundError, solver.init_data, filename)

    def test_bad_json_format(self):
        filename = "./test_inputs/bad_json_format.dat"
        self.assertRaises(JSONDecodeError, solver.init_data, filename)
