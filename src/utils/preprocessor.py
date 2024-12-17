from typing import Dict, List
import re

class TextPreprocessor:
    """
    Utilities for preprocessing text data before embedding or analysis.
    Provides static methods for text cleaning and formatting.
    """
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Cleans and normalizes input text.
        
        @param text: Input text to clean
        @type text: str
        @return: Cleaned text
        @rtype: str
        """
        # Eliminar caracteres especiales y formateo básico
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower().strip()
        return text

    @staticmethod
    def prepare_episode_text(episode: Dict) -> str:
        """
        Formats episode information into structured text.
        
        @param episode: Episode data dictionary
        @type episode: Dict
        @return: Formatted episode text
        @rtype: str
        """
        # Combinar información relevante del episodio
        parts = [
            f"Episode Title: {episode['name']}",
            f"Season {episode['season']} Episode {episode['episode']}",
            f"Plot: {episode['plot']}",
        ]
        return "\n".join(parts)

    @staticmethod
    def prepare_character_text(character: Dict) -> str:
        """
        Formats character information into structured text.
        
        @param character: Character data dictionary
        @type character: Dict
        @return: Formatted character text
        @rtype: str
        """
        # Combinar información relevante del personaje
        parts = [
            f"Character Name: {character['name']}",
            f"Species: {character['species']}",
            f"Description: {character.get('description', '')}",
        ]
        return "\n".join(parts)