#!/bin/bash
set -e

# Función para verificar ChromaDB
check_chroma() {
    curl --silent --fail http://chromadb:8000/api/v1/heartbeat > /dev/null
}

# Esperar a que ChromaDB esté disponible
echo "Esperando que ChromaDB esté listo..."
until check_chroma; do
    echo "ChromaDB no está disponible - esperando 2 segundos..."
    sleep 2
done
echo "¡ChromaDB está listo!"

# Verificar si la base de datos ya está inicializada
echo "Verificando estado de la base de datos..."
python << END
import asyncio
from src.modules.retriever import Retriever

async def check_db():
    try:
        retriever = Retriever()
        count = retriever.count_documents()
        print(f"Documentos encontrados: {count}")
        return count
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")
        return 0

count = asyncio.run(check_db())
with open('/tmp/db_count', 'w') as f:
    f.write(str(count))
END

DB_COUNT=$(cat /tmp/db_count)

# Inicializar la base de datos si está vacía
if [ "$DB_COUNT" -eq "0" ]; then
    echo "Inicializando base de datos..."
    python -c "
import asyncio
from src.modules.rick_morty_api import RickMortyAPI
from src.modules.retriever import Retriever

async def init_database():
    print('Iniciando carga de datos...')
    api = RickMortyAPI()
    retriever = Retriever()
    
    print('Obteniendo datos de la API...')
    data = await api.fetch_all_data()
    
    print('Procesando datos...')
    documents = api.process_data_for_embedding(data)
    
    print('Cargando en ChromaDB...')
    retriever.add_documents(documents)
    
    count = retriever.count_documents()
    print(f'Total documentos cargados: {count}')

asyncio.run(init_database())
"
    echo "¡Base de datos inicializada correctamente!"
else
    echo "La base de datos ya está inicializada con $DB_COUNT documentos."
fi

# Iniciar la aplicación
echo "Iniciando aplicación FastAPI..."
exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --proxy-headers