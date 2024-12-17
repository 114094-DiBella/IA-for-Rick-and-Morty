import json
import os
from typing import List, Dict

class DataLoader:
    """
    Handles loading of Rick & Morty data from JSON files.
    """
    def __init__(self, data_dir: str = "src/data/raw"):
        """
        Initializes the DataLoader with the specified data directory.
        
        @param data_dir: Path to the directory containing data files
        @type data_dir: str
        """
        self.data_dir = data_dir

    def load_episodes(self) -> List[Dict]:
        """
        Loads episode data from episodes.json file.
        
        @return: List of episode dictionaries
        @rtype: List[Dict]
        """
        try:
            with open(os.path.join(self.data_dir, "episodes.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["episodes"]
        except FileNotFoundError:
            print("Archivo episodes.json no encontrado")
            return []

    def load_characters(self) -> List[Dict]:
        """
        Loads character data from characters.json file.
        
        @return: List of character dictionaries
        @rtype: List[Dict]
        """
        try:
            with open(os.path.join(self.data_dir, "characters.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["characters"]
        except FileNotFoundError:
            print("Archivo characters.json no encontrado")
            return []

    def load_all(self) -> Dict[str, List[Dict]]:
        """
        Loads all available data (episodes and characters).
        
        @return: Dictionary containing both episode and character data
        @rtype: Dict[str, List[Dict]]
        """
        return {
            "episodes": self.load_episodes(),
            "characters": self.load_characters()
        }