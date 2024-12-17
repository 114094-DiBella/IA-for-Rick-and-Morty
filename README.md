# Rick and Morty RAG Assistant 🌌

## Descripción
Este proyecto implementa un sistema de Question-Answering basado en arquitectura RAG (Retrieval-Augmented Generation) especializado en la serie Rick and Morty. El asistente puede responder preguntas sobre episodios, personajes, dimensiones, teorías y referencias científicas de la serie.

## 🎯 Problemática
La serie Rick and Morty tiene un universo complejo con múltiples dimensiones, líneas temporales y referencias científicas que pueden ser difíciles de seguir. Los fans necesitan una herramienta que pueda:
- Proporcionar información precisa sobre episodios y personajes
- Explicar referencias científicas y culturales
- Conectar eventos entre diferentes episodios
- Aclarar líneas temporales y dimensiones alternativas

## 🚀 Características Principales
- Búsqueda inteligente de información sobre episodios
- Explorador de personajes y sus variantes dimensionales
- Catálogo de inventos y tecnologías de Rick
- Sistema de mapeo de dimensiones y líneas temporales
- Explicación de referencias científicas
- API RESTful para integración con otros sistemas

## 📋 Requisitos Previos
- Python 3.9+
- MongoDB
- Redis
- Git

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/yourusername/rick-morty-rag.git
cd rick-morty-rag
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: source venv/Scripts/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

## 📦 Requirements.txt
```
fastapi
uvicorn
cohere
chromadb
httpx
pydantic
python-dotenv
langdetect
```

## 🗂️ Estructura del Proyecto
```
rick_morty_rag/
├── src/
│   ├── api/
│   │   ├── main.py          # Endpoints FastAPI
│   │   └── models.py        # Modelos Pydantic
│   ├── config/
│   │   └── settings.py      # Configuraciones
│   └── modules/
│       ├── generator.py     # Generación de respuestas
│       ├── retriever.py     # Manejo de ChromaDB
│       ├── rag_engine.py    # Motor principal RAG
│       └── rick_morty_api.py# Cliente API Rick & Morty
└── chroma_db/               # Base de datos persistente
```

## 🚀 Uso

1. Iniciar el servidor:
```bash
uvicorn src.api.main:app --reload
```

2. Acceder a la documentación de la API:
```
http://localhost:8000/docs
```

3. Ejemplo de uso de la API:
```python
import requests

response = requests.post(
    "http://localhost:8000/qa",
    json={"question": "¿En qué episodio aparece Evil Morty por primera vez?"}
)
print(response.json())
```

## Pasos para ejecutar el proyecto

1. Configurar el entorno:
   ```bash
   # Clonar repositorio
   git clone https://github.com/[usuario]/rick-morty-rag.git
   cd rick-morty-rag

   # Crear entorno virtual
   python -m venv venv
   source venv/bin/activate  # Windows: source venv/Scripts/activate

   # Instalar dependencias
   pip install -r requirements.txt

   # Configurar variables de entorno
   cp .env.example .env
   # Editar .env con las configuraciones necesarias
   ```

2. Inicializar la base de datos:
   ```bash
   # Este paso es OBLIGATORIO antes de iniciar el servidor
   # Consume la API de Rick & Morty e inicializa ChromaDB
   python src/init_db.py
   ```

3. Iniciar el servidor:
   ```bash
   # Una vez inicializada la BD, podemos iniciar el servidor
   uvicorn src.api.main:app --reload
   ```

4. Verificar la instalación:
   ```bash
   # Comprobar el estado de la base de datos
   curl http://localhost:8000/status
   ```

### Notas importantes sobre la inicialización
- La inicialización de la base de datos es un paso **obligatorio**
- El script `init_db.py`:
  - Consume la API oficial de Rick & Morty
  - Procesa los datos para embedding
  - Crea y popula la base de datos vectorial
  - Verifica la carga correcta de los documentos
- El proceso puede tomar varios minutos dependiendo de la cantidad de datos
- La base de datos es persistente y solo necesita inicializarse una vez

    
## 🧪 Tests
Ejecutar tests:
```bash
pytest
```

## 📝 Ejemplos de Consultas
- "¿Cuál es la historia de Evil Morty?"
- "Explica cómo funciona el Portal Gun"
- "¿Qué dimensiones aparecen en la temporada 1?"
- "¿Cuáles son los inventos más importantes de Rick?"

## 🔄 Flujo de Trabajo de RAG
1. **Recuperación**: Búsqueda de información relevante en la base de datos vectorial
2. **Augmentación**: Enriquecimiento del contexto con información adicional
3. **Generación**: Creación de respuestas coherentes y precisas

## 🛠️ Tecnologías Utilizadas
- FastAPI: Framework web
- LangChain: Orquestación de LLMs
- ChromaDB: Base de datos vectorial


## 🤝 Contribución
1. Fork el proyecto
2. Crear una rama (`git checkout -b feature/amazing_feature`)
3. Commit los cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing_feature`)
5. Abrir un Pull Request

## 👥 Autores
- Agustin Di Bella (@114094-DiBella)


## 📞 Contacto
- Email: aguss.dibella777@gmail.com
- GitHub: @114094-DiBella