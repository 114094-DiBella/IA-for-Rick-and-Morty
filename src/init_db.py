import asyncio
from src.modules.rick_morty_api import RickMortyAPI
from src.modules.retriever import Retriever
from src.modules.data_loader import DataLoader

async def init_database():
    print("Iniciando carga de datos...")
    
    # Crear instancias
    api = RickMortyAPI()
    retriever = Retriever()
    data_loader = DataLoader()
    
    # Obtener datos de la API
    print("Obteniendo datos de la API...")
    data = await api.fetch_all_data()
    print(f"Datos obtenidos: {len(data['characters'])} personajes, {len(data['episodes'])} episodios")

    # Cargar transcripciones
    print("Cargando transcripciones...")
    transcriptions = data_loader.load_transcripts()
    print(f"Transcripciones cargadas: {len(transcriptions)}")

    # Procesar datos para embedding
    print("Procesando datos...")
    documents = api.process_data_for_embedding(data, transcriptions)
    print(f"Documentos preparados: {len(documents)}")

    # Cargar en ChromaDB
    print("Cargando datos en ChromaDB...")
    retriever.add_documents(documents)
    
    print("Verificando carga...")
    count = retriever.count_documents()
    print(f"Total documentos en la base: {count}")

    if count == 0:
        print("¡ADVERTENCIA! No se cargaron documentos")
    else:
        print("¡Carga completada exitosamente!")

if __name__ == "__main__":
    asyncio.run(init_database())