from unittest import TestCase
from howlongtobeatpy import HowLongToBeat


class TestNormalRequest(TestCase):

    @staticmethod
    def getMaxSimilarityElement(list_of_results):
        if list_of_results is not None and len(list_of_results) > 0:
            return max(list_of_results, key=lambda element: element.similarity)
        else:
            return None

    @staticmethod
    def getSimpleNumber(time_string):
        if time_string is None:
            return 0
        if isinstance(time_string, int):
            return time_string
        if not time_string.isdigit():
            return int(time_string.strip().replace("½", " "))
        else:
            return int(time_string)

    def test_simple_similarity_value(self):
        results_all = HowLongToBeat(0.0).search("Grip")
        results_default = HowLongToBeat().search("Grip")
        results_impossible = HowLongToBeat(1.0).search("Grip")
        self.assertTrue(len(results_all) > len(results_default))
        self.assertTrue(len(results_impossible) == 0)

    def test_simple_game_name(self):
        results = HowLongToBeat().search("Celeste")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("Celeste", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(12, self.getSimpleNumber(best_result.gameplay_main_extra), delta=5)

    def test_game_name_with_colon(self):
        results = HowLongToBeat().search("Half-Life: Opposing Force")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("Half-Life: Opposing Force", best_result.game_name)

    def test_game_name(self):
        results = HowLongToBeat().search("A way out")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("A Way Out", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(7, self.getSimpleNumber(best_result.gameplay_completionist), delta=3)

    def test_game_name_with_numbers(self):
        results = HowLongToBeat().search("The Witcher 3")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(50, self.getSimpleNumber(best_result.gameplay_main), delta=5)

    def test_game_with_no_all_values(self):
        results = HowLongToBeat().search("Battlefield 2142")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Battlefield 2142", best_result.game_name)
        self.assertEqual(None, best_result.gameplay_main_label)
        self.assertEqual("Co-Op", best_result.gameplay_main_extra_label)
        self.assertEqual("Vs.", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(80, TestNormalRequest.getSimpleNumber(best_result.gameplay_completionist), delta=5)
        self.assertEqual("Hours", best_result.gameplay_completionist_unit)
        self.assertEqual(None, best_result.gameplay_main_unit)
        self.assertEqual(None, best_result.gameplay_main_extra_unit)
        self.assertEqual(-1, TestNormalRequest.getSimpleNumber(best_result.gameplay_main))
        self.assertEqual(-1, TestNormalRequest.getSimpleNumber(best_result.gameplay_main_extra))

    def test_no_real_game(self):
        results = HowLongToBeat().search("asfjklagls")
        self.assertEqual(0, len(results))

    def test_empty_game_name(self):
        results = HowLongToBeat().search("")
        self.assertEqual(None, results)

    def test_null_game_name(self):
        results = HowLongToBeat().search(None)
        self.assertEqual(None, results)
