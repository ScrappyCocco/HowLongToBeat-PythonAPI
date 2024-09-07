from unittest import TestCase
from howlongtobeatpy import HowLongToBeat
from howlongtobeatpy.HTMLRequests import SearchModifiers


class TestNormalRequest(TestCase):

    @staticmethod
    def getMaxSimilarityElement(list_of_results):
        if list_of_results is not None and len(list_of_results) > 0:
            return max(list_of_results, key=lambda element: element.similarity)
        return None

    @staticmethod
    def getSimpleNumber(time_string):
        if time_string is None:
            return 0
        if isinstance(time_string, float):
            return time_string
        if isinstance(time_string, int):
            return time_string
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
        self.assertAlmostEqual(12, self.getSimpleNumber(best_result.main_extra), delta=5)

    def test_game_name_with_colon(self):
        results = HowLongToBeat().search("Half-Life: Opposing Force")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("Half-Life: Opposing Force", best_result.game_name)

    def test_game_name_and_dev(self):
        results = HowLongToBeat().search("Crysis Warhead")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("Crysis Warhead", best_result.game_name)
        if best_result.profile_dev is not None:
            self.assertEqual("Crytek Budapest", best_result.profile_dev)
        self.assertEqual("2008", str(best_result.release_world))
        self.assertAlmostEqual(7, self.getSimpleNumber(best_result.completionist), delta=3)

    def test_game_name_with_numbers(self):
        results = HowLongToBeat().search("The Witcher 3")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = self.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertAlmostEqual(50, self.getSimpleNumber(best_result.main_story), delta=5)

    def test_game_with_values(self):
        results = HowLongToBeat().search("Battlefield 2142")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Battlefield 2142", best_result.game_name)
        self.assertAlmostEqual(14, TestNormalRequest.getSimpleNumber(best_result.main_story), delta=5)
        self.assertAlmostEqual(17, TestNormalRequest.getSimpleNumber(best_result.main_extra), delta=5)
        self.assertAlmostEqual(30, TestNormalRequest.getSimpleNumber(best_result.completionist), delta=5)

    def test_game_links(self):
        results = HowLongToBeat().search("Battlefield 2142")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertNotEqual(None, best_result, "Search Result is None")
        self.assertEqual("Battlefield 2142", best_result.game_name)
        self.assertEqual("https://howlongtobeat.com/game/936", best_result.game_web_link)
        self.assertTrue("howlongtobeat.com/games/" in best_result.game_image_url)
        self.assertTrue("Battlefield_2142.png" in best_result.game_image_url or "Battlefield_2142.jpg" in best_result.game_image_url)

    def test_game_default_dlc_search(self):
        results = HowLongToBeat().search("Hearts of Stone")
        self.assertEqual(1, len(results))

    def test_game_hide_dlc_search(self):
        results = HowLongToBeat().search("Hearts of Stone", search_modifiers=SearchModifiers.HIDE_DLC)
        self.assertEqual(0, len(results))

    def test_game_include_dlc_search(self):
        results = HowLongToBeat().search("Hearts of Stone")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt - Hearts of Stone", best_result.game_name)

    def test_game_isolate_dlc_search(self):
        results = HowLongToBeat().search("Hearts of Stone", SearchModifiers.ISOLATE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt - Hearts of Stone", best_result.game_name)

    def test_game_really_isolate_dlc_search(self):
        results = HowLongToBeat(0).search("Skyrim", SearchModifiers.ISOLATE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertEqual(3, len(results))

    def test_game_case_sensitive(self):
        results_standard = HowLongToBeat(0).search("RED HOT VENGEANCE")
        results_not_case_sens = HowLongToBeat(0).search("RED HOT VENGEANCE",
                                                        similarity_case_sensitive=False)
        self.assertNotEqual(None, results_standard, "Search Results (standard) are None")
        self.assertNotEqual(None, results_not_case_sens, "Search Results (_not_case_sens) are None")
        self.assertNotEqual(0, len(results_standard))
        self.assertNotEqual(0, len(results_not_case_sens))
        best_element_standard = max(results_standard, key=lambda element: element.similarity)
        best_element_not_case = max(results_not_case_sens, key=lambda element: element.similarity)
        self.assertTrue(best_element_standard.similarity <= best_element_not_case.similarity,
                        "Wrong similarity results")

    def test_game_alias_present(self):
        results = HowLongToBeat(0).search("God Of War")
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertNotEqual(0, len(results))
        best_element = max(results, key=lambda element: element.similarity)
        self.assertEqual("God of War".lower(), best_element.game_name.lower())
        self.assertNotEqual(None, best_element.game_alias, "The suffix is still None, it should not be")
        self.assertEqual(best_element.game_alias, "God of War (PS4)")

    def test_game_alias_not_present(self):
        results = HowLongToBeat(0).search("XCOM 2")
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertNotEqual(0, len(results))
        best_element = max(results, key=lambda element: element.similarity)
        self.assertEqual(0, len(best_element.game_alias), "The suffix is not None, it should be")

    def test_no_real_game(self):
        results = HowLongToBeat().search("asfjklagls")
        self.assertEqual(0, len(results))

    def test_no_real_game_with_similarity(self):
        results = HowLongToBeat(0).search("asfjklagls")
        self.assertEqual(0, len(results))

    def test_empty_game_name(self):
        results = HowLongToBeat().search("")
        self.assertEqual(None, results)

    def test_null_game_name(self):
        results = HowLongToBeat().search(None)
        self.assertEqual(None, results)
