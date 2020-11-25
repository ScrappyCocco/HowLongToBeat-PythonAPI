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
