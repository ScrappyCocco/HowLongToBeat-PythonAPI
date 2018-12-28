from unittest import TestCase
from aiounittest import async_test
from howlongtobeatpy import HowLongToBeat
from .test_normal_request import TestNormalRequest


class TestAsyncRequest(TestCase):

    @async_test
    async def test_async_add(self):
        results = await HowLongToBeat().async_search("Celeste")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Celeste", best_result.game_name)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(best_result.gameplay_main_extra), delta=5)

    @async_test
    async def test_simple_game_name(self):
        results = await HowLongToBeat().async_search("Celeste")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Celeste", best_result.game_name)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(best_result.gameplay_main_extra), delta=5)

    @async_test
    async def test_game_name(self):
        results = await HowLongToBeat().async_search("A way out")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("A Way Out", best_result.game_name)
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(best_result.gameplay_completionist), delta=3)

    @async_test
    async def test_game_name_with_numbers(self):
        results = await HowLongToBeat().async_search("The Witcher 3")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(best_result.gameplay_main), delta=5)

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
