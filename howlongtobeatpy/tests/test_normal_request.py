from unittest import TestCase
from howlongtobeatpy import HowLongToBeat


class TestNormalRequest(TestCase):

    @staticmethod
    def getMaxSimilarityElement(list_of_results):
        max_sim = -1
        best_element = None
        for element in list_of_results:
            if element.similarity > max_sim:
                max_sim = element.similarity
                best_element = element
        return best_element

    @staticmethod
    def getSimpleNumber(time_string):
        if time_string is None:
            return 0
        if not time_string.isdigit():
            return int(time_string.strip().replace("½", " "))
        else:
            return int(time_string)

    def test_simple_game_name(self):
        results = HowLongToBeat().search("Celeste")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("Celeste", best_result.game_name)
        self.assertAlmostEqual(12, self.getSimpleNumber(best_result.gameplay_main_extra), delta=5)

    def test_game_name(self):
        results = HowLongToBeat().search("A way out")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("A Way Out", best_result.game_name)
        self.assertAlmostEqual(7, self.getSimpleNumber(best_result.gameplay_completionist), delta=3)

    def test_game_name_with_numbers(self):
        results = HowLongToBeat().search("The Witcher 3")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertAlmostEqual(50, self.getSimpleNumber(best_result.gameplay_main), delta=5)

    def test_no_real_game(self):
        results = HowLongToBeat().search("asfjklagls")
        self.assertEqual(0, len(results))

    def test_empty_game_name(self):
        results = HowLongToBeat().search("")
        self.assertEqual(None, results)

    def test_null_game_name(self):
        results = HowLongToBeat().search(None)
        self.assertEqual(None, results)
