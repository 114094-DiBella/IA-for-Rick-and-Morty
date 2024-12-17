import unittest
from src.modules.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.loader = DataLoader()

    def test_load_episodes(self):
        episodes = self.loader.load_episodes()
        self.assertIsInstance(episodes, list)
        if episodes:  # si hay episodios cargados
            self.assertTrue(all(isinstance(ep, dict) for ep in episodes))

    def test_load_characters(self):
        characters = self.loader.load_characters()
        self.assertIsInstance(characters, list)
        if characters:  # si hay personajes cargados
            self.assertTrue(all(isinstance(char, dict) for char in characters))

if __name__ == '__main__':
    unittest.main()