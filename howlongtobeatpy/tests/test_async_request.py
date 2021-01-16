from unittest import TestCase
from aiounittest import async_test
from howlongtobeatpy import HowLongToBeat
from howlongtobeatpy.HTMLRequests import SearchModifiers

from .test_normal_request import TestNormalRequest


class TestAsyncRequest(TestCase):

    @async_test
    async def test_simple_game_name(self):
        results = await HowLongToBeat().async_search("Celeste")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Celeste", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(best_result.gameplay_main_extra), delta=5)

    @async_test
    async def test_game_name_with_colon(self):
        results = await HowLongToBeat().async_search("Half-Life: Opposing Force")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Half-Life: Opposing Force", best_result.game_name)

    @async_test
    async def test_game_name(self):
        results = await HowLongToBeat().async_search("A way out")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("A Way Out", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(best_result.gameplay_completionist), delta=3)

    @async_test
    async def test_game_name_with_numbers(self):
        results = await HowLongToBeat().async_search("The Witcher 3")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertEqual("Main Story", best_result.gameplay_main_label)
        self.assertEqual("Main + Extra", best_result.gameplay_main_extra_label)
        self.assertEqual("Completionist", best_result.gameplay_completionist_label)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(best_result.gameplay_main), delta=5)

    @async_test
    async def test_game_with_no_all_values(self):
        results = await HowLongToBeat().async_search("Battlefield 2142")
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

    @async_test
    async def test_game_default_dlc_search(self):
        results = await HowLongToBeat().async_search("Hearts of Stone")
        self.assertEqual(1, len(results))

    @async_test
    async def test_game_hide_dlc_search(self):
        results = await HowLongToBeat().async_search("Hearts of Stone", search_modifiers=SearchModifiers.HIDE_DLC)
        self.assertEqual(0, len(results))

    @async_test
    async def test_game_include_dlc_search(self):
        results = await HowLongToBeat().async_search("Hearts of Stone", SearchModifiers.INCLUDE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt - Hearts of Stone", best_result.game_name)

    @async_test
    async def test_game_isolate_dlc_search(self):
        results = await HowLongToBeat().async_search("Hearts of Stone", SearchModifiers.ISOLATE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt - Hearts of Stone", best_result.game_name)

    @async_test
    async def test_game_really_isolate_dlc_search(self):
        results = await HowLongToBeat().async_search("The Witcher 3", SearchModifiers.ISOLATE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertEqual(2, len(results))

    @async_test
    async def test_game_case_sensitive(self):
        results_standard = await HowLongToBeat(0).async_search("RED HOT VENGEANCE")
        results_not_case_sens = await HowLongToBeat(0).async_search("RED HOT VENGEANCE",
                                                                    similarity_case_sensitive=False)
        self.assertNotEqual(None, results_standard, "Search Results (standard) are None")
        self.assertNotEqual(None, results_not_case_sens, "Search Results (_not_case_sens) are None")
        self.assertNotEqual(0, len(results_standard))
        self.assertNotEqual(0, len(results_not_case_sens))
        best_element_standard = max(results_standard, key=lambda element: element.similarity)
        best_element_not_case = max(results_not_case_sens, key=lambda element: element.similarity)
        self.assertTrue(best_element_standard.similarity <= best_element_not_case.similarity,
                        "Wrong similarity results")

    @async_test
    async def test_no_real_game(self):
        results = await HowLongToBeat().async_search("asfjklagls")
        self.assertEqual(0, len(results))

    @async_test
    async def test_empty_game_name(self):
        results = await HowLongToBeat().async_search("")
        self.assertEqual(None, results)

    @async_test
    async def test_null_game_name(self):
        results = await HowLongToBeat().async_search(None)
        self.assertEqual(None, results)
