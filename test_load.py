from src.modules.data_loader import DataLoader

def test_data():
    loader = DataLoader()
    
    # Cargar datos
    print("Cargando datos...")
    episodes = loader.load_episodes()
    characters = loader.load_characters()
    
    # Verificar episodios
    print("\nEpisodios cargados:")
    print(f"Número de episodios: {len(episodes)}")
    if episodes:
        print(f"Ejemplo de episodio: {episodes[0]['name']}")
    
    # Verificar personajes
    print("\nPersonajes cargados:")
    print(f"Número de personajes: {len(characters)}")
    if characters:
        print(f"Ejemplo de personaje: {characters[0]['name']}")

if __name__ == "__main__":
    test_data()