from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
#- Agregar configuración para API Rick and Morty
#- Ajustar configuraciones para Docker
class Settings(BaseSettings):
    """
    Configuration settings for the application.
    Handles environment variables and configuration values.
    
    @param COHERE_API_KEY: API key for Cohere
    @param ENVIRONMENT: Current environment (default: "development")
    @param MODEL_NAME: Name of the Cohere model to use
    """
    COHERE_API_KEY: str
    ENVIRONMENT: str = "development"
    MODEL_NAME: str = "command-r7b-12-2024"

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='allow'
    )
@lru_cache()
def get_settings():
    """
    Retrieves application settings with caching.
    
    @return: Settings instance
    @rtype: Settings
    """
    return Settings()