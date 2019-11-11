from unittest import TestCase
from howlongtobeatpy import HowLongToBeat
from .test_normal_request import TestNormalRequest


class TestNormalRequestById(TestCase):

    def test_simple_game_name(self):
        result = HowLongToBeat().search_from_id(42818)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Celeste", result.game_name)
        self.assertEqual("Main Story", result.gameplay_main_label)
        self.assertEqual("Main + Extra", result.gameplay_main_extra_label)
        self.assertEqual("Completionist", result.gameplay_completionist_label)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(result.gameplay_main_extra), delta=5)

    def test_game_name(self):
        result = HowLongToBeat().search_from_id(46386)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("A Way Out", result.game_name)
        self.assertEqual("Main Story", result.gameplay_main_label)
        self.assertEqual("Main + Extra", result.gameplay_main_extra_label)
        self.assertEqual("Completionist", result.gameplay_completionist_label)
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(result.gameplay_completionist), delta=3)

    def test_game_name_with_numbers(self):
        result = HowLongToBeat().search_from_id(10270)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("The Witcher 3: Wild Hunt", result.game_name)
        self.assertEqual("Main Story", result.gameplay_main_label)
        self.assertEqual("Main + Extra", result.gameplay_main_extra_label)
        self.assertEqual("Completionist", result.gameplay_completionist_label)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(result.gameplay_main), delta=5)

    def test_game_with_no_all_values(self):
        result = HowLongToBeat().search_from_id(936)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Battlefield 2142", result.game_name)
        self.assertEqual(None, result.gameplay_main_label)
        self.assertEqual("Co-Op", result.gameplay_main_extra_label)
        self.assertEqual("Vs.", result.gameplay_completionist_label)
        self.assertAlmostEqual(80, TestNormalRequest.getSimpleNumber(result.gameplay_completionist), delta=5)
        self.assertEqual("Hours", result.gameplay_completionist_unit)
        self.assertEqual(None, result.gameplay_main_unit)
        self.assertEqual(None, result.gameplay_main_extra_unit)
        self.assertEqual(-1, TestNormalRequest.getSimpleNumber(result.gameplay_main))
        self.assertEqual(-1, TestNormalRequest.getSimpleNumber(result.gameplay_main_extra))

    def test_no_real_game(self):
        result = HowLongToBeat().search_from_id(123)
        self.assertEqual(None, result)

    def test_empty_game_name(self):
        result = HowLongToBeat().search_from_id(0)
        self.assertEqual(None, result)

    def test_null_game_name(self):
        result = HowLongToBeat().search_from_id(None)
        self.assertEqual(None, result)
