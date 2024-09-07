from unittest import TestCase
from howlongtobeatpy import HowLongToBeat
from .test_normal_request import TestNormalRequest


class TestNormalRequestById(TestCase):

    def test_simple_game_name(self):
        result = HowLongToBeat().search_from_id(42818)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Celeste", result.game_name)
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(result.main_story), delta=5)

    def test_game_name_with_colon(self):
        result = HowLongToBeat().search_from_id(4256)
        self.assertNotEqual(None, result, "Search Results are None")
        self.assertEqual("Half-Life: Opposing Force", result.game_name)

    def test_game_name_and_dev(self):
        result = HowLongToBeat().search_from_id(2071)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Crysis Warhead", result.game_name)
        if result.profile_dev is not None:
            self.assertEqual("Crytek Budapest", result.profile_dev)
        self.assertEqual("2008", str(result.release_world))
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(result.completionist), delta=3)

    def test_game_name_with_numbers(self):
        result = HowLongToBeat().search_from_id(10270)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("The Witcher 3: Wild Hunt", result.game_name)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(result.main_story), delta=5)

    def test_game_with_values(self):
        result = HowLongToBeat().search_from_id(936)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Battlefield 2142", result.game_name)
        self.assertAlmostEqual(14, TestNormalRequest.getSimpleNumber(result.main_story), delta=5)
        self.assertAlmostEqual(17, TestNormalRequest.getSimpleNumber(result.main_extra), delta=5)
        self.assertAlmostEqual(30, TestNormalRequest.getSimpleNumber(result.completionist), delta=5)

    def test_game_links(self):
        result = HowLongToBeat().search_from_id(936)
        self.assertNotEqual(None, result, "Search Result is None")
        self.assertEqual("Battlefield 2142", result.game_name)
        self.assertEqual("https://howlongtobeat.com/game/936", result.game_web_link)
        self.assertTrue("howlongtobeat.com/games/" in result.game_image_url)
        self.assertTrue("Battlefield_2142.png" in result.game_image_url or "Battlefield_2142.jpg" in result.game_image_url)

    def test_no_real_game(self):
        result = HowLongToBeat().search_from_id(123)
        self.assertEqual(None, result)

    def test_empty_game_name(self):
        result = HowLongToBeat().search_from_id(0)
        self.assertEqual(None, result)

    def test_null_game_name(self):
        result = HowLongToBeat().search_from_id(None)
        self.assertEqual(None, result)
