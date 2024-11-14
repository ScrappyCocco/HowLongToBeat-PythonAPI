from unittest import TestCase
from aiounittest import async_test
from howlongtobeatpy import HowLongToBeat
from .test_normal_request import TestNormalRequest


class TestAsyncRequestById(TestCase):

    @async_test
    async def test_simple_game_name(self):
        result = await HowLongToBeat().async_search_from_id(42818)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Celeste", result.game_name)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(result.main_story), delta=5)

    @async_test
    async def test_game_name_with_colon(self):
        result = await HowLongToBeat().async_search_from_id(4256)
        self.assertNotEqual(None, result, "Search Results are None")
        self.assertEqual("Half-Life: Opposing Force", result.game_name)

    @async_test
    async def test_game_name_and_dev(self):
        result = await HowLongToBeat().async_search_from_id(2071)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Crysis Warhead", result.game_name)
        if result.profile_dev is not None:
            self.assertEqual("Crytek Budapest", result.profile_dev)
        self.assertEqual("2008", str(result.release_world))
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(result.completionist), delta=3)

    @async_test
    async def test_game_name_with_numbers(self):
        result = await HowLongToBeat().async_search_from_id(10270)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("The Witcher 3: Wild Hunt", result.game_name)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(result.main_story), delta=25)

    @async_test
    async def test_game_with_values(self):
        result = await HowLongToBeat().async_search_from_id(2070)
        self.assertNotEqual(None, result, "Search Results are None")
        self.assertEqual("Crysis 3", result.game_name)
        self.assertAlmostEqual(6, TestNormalRequest.getSimpleNumber(result.main_story), delta=20)
        self.assertAlmostEqual(8, TestNormalRequest.getSimpleNumber(result.main_extra), delta=20)
        self.assertAlmostEqual(13, TestNormalRequest.getSimpleNumber(result.completionist), delta=20)

    @async_test
    async def test_game_links(self):
        result = await HowLongToBeat().async_search_from_id(936)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Battlefield 2142", result.game_name)
        self.assertEqual("https://howlongtobeat.com/game/936", result.game_web_link)
        self.assertTrue("howlongtobeat.com/games/" in result.game_image_url)
        self.assertTrue("Battlefield_2142.png" in result.game_image_url or "Battlefield_2142.jpg" in result.game_image_url)

    @async_test
    async def test_no_real_game(self):
        result = await HowLongToBeat().async_search_from_id(123)
        self.assertEqual(None, result)

    @async_test
    async def test_empty_game_name(self):
        result = await HowLongToBeat().async_search_from_id(0)
        self.assertEqual(None, result)

    @async_test
    async def test_null_game_name(self):
        result = await HowLongToBeat().async_search_from_id(None)
        self.assertEqual(None, result)
