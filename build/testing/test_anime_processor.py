import unittest, anime_processor

class TestAnimeProcessor(unittest.TestCase):
    def test_remove_non_numeric_parentheses(self):
        self.assertEqual(anime_processor.remove_non_numeric_parentheses("Ace Attorney (Gyakuten Saiban)"), "Ace Attorney")
        self.assertEqual(anime_processor.remove_non_numeric_parentheses("Naruto"), "Naruto")
