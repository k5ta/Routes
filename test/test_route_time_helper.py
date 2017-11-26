import unittest
import src.route_time_helper as time_helper


class TestRouteTimeHelper(unittest.TestCase):
    def test_calc_time(self):
        self.assertEqual(time_helper.calc_time("00:00", 67), "01:07")
        self.assertEqual(time_helper.calc_time("00:00", "5"), "00:05")
        self.assertEqual(time_helper.calc_time("01:00", "23:59"), "1-00:59")
