import asyncio
from modules.rick_morty_api import RickMortyAPI
from modules.retriever import Retriever

async def init_database():
    print("Iniciando carga de datos...")
    
    # Crear instancias
    api = RickMortyAPI()
    retriever = Retriever()
    
    # Obtener datos de la API
    print("Obteniendo datos de la API...")
    data = await api.fetch_all_data()
    print(f"Datos obtenidos: {len(data['characters'])} personajes, {len(data['episodes'])} episodios")

    # Procesar datos para embedding
    print("Procesando datos...")
    documents = api.process_data_for_embedding(data)
    print(f"Documentos preparados: {len(documents)}")

    
    # Cargar en ChromaDB
    print("Cargando datos en ChromaDB...")
    retriever.add_documents(documents)
    
    print(f"Verificando carga...")
    count = retriever.count_documents()
    print(f"Total documentos en la base: {count}")

    if count == 0:
        print("¡ADVERTENCIA! No se cargaron documentos")
    else:
        print("¡Carga completada exitosamente!")
    print("¡Carga completada!")

if __name__ == "__main__":
    asyncio.run(init_database())