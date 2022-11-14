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
        self.assertAlmostEqual(12, TestNormalRequest.getSimpleNumber(best_result.main_extra), delta=5)

    @async_test
    async def test_game_name_with_colon(self):
        results = await HowLongToBeat().async_search("Half-Life: Opposing Force")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Half-Life: Opposing Force", best_result.game_name)

    @async_test
    async def test_game_name_and_dev(self):
        results = await HowLongToBeat().async_search("Crysis Warhead")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Crysis Warhead", best_result.game_name)
        self.assertEqual("Crytek Budapest", best_result.profile_dev)
        self.assertEqual("2008", str(best_result.release_world))
        self.assertAlmostEqual(7, TestNormalRequest.getSimpleNumber(best_result.completionist), delta=3)

    @async_test
    async def test_game_name_with_numbers(self):
        results = await HowLongToBeat().async_search("The Witcher 3")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("The Witcher 3: Wild Hunt", best_result.game_name)
        self.assertAlmostEqual(50, TestNormalRequest.getSimpleNumber(best_result.main_story), delta=5)

    @async_test
    async def test_game_with_values(self):
        results = await HowLongToBeat().async_search("Battlefield 2142")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertEqual("Battlefield 2142", best_result.game_name)
        self.assertAlmostEqual(14, TestNormalRequest.getSimpleNumber(best_result.main_story), delta=5)
        self.assertAlmostEqual(17, TestNormalRequest.getSimpleNumber(best_result.main_extra), delta=5)
        self.assertAlmostEqual(30, TestNormalRequest.getSimpleNumber(best_result.completionist), delta=5)

    @async_test
    async def test_game_links(self):
        results = await HowLongToBeat().async_search("Battlefield 2142")
        self.assertNotEqual(None, results, "Search Results are None")
        best_result = TestNormalRequest.getMaxSimilarityElement(results)
        self.assertNotEqual(None, best_result, "Search Result is None")
        self.assertEqual("Battlefield 2142", best_result.game_name)
        self.assertEqual("https://howlongtobeat.com/game/936", best_result.game_web_link)
        self.assertTrue("howlongtobeat.com/games/256px-Battlefield_2142_box_art.jpg" in best_result.game_image_url)

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
        results = await HowLongToBeat().async_search("Hearts of Stone")
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
        results = await HowLongToBeat(0).async_search("Skyrim", SearchModifiers.ISOLATE_DLC)
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertEqual(3, len(results))

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
    async def test_game_alias_present(self):
        results = await HowLongToBeat(0).async_search("God Of War")
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertNotEqual(0, len(results))
        best_element = max(results, key=lambda element: element.similarity)
        self.assertEqual("God of War".lower(), best_element.game_name.lower())
        self.assertNotEqual(None, best_element.game_alias, "The suffix is still None, it should not be")
        self.assertEqual(best_element.game_alias, "God of War (PS4)")

    @async_test
    async def test_game_alias_not_present(self):
        results = await HowLongToBeat(0).async_search("XCOM 2")
        self.assertNotEqual(None, results, "Search Results are None")
        self.assertNotEqual(0, len(results))
        best_element = max(results, key=lambda element: element.similarity)
        self.assertEqual(0, len(best_element.game_alias), "The suffix is not None, it should be")

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
