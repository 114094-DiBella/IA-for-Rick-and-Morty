import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import os
import re
import traceback

class Retriever:
    """
    Manages vector database operations using ChromaDB for document storage and retrieval.
    Handles persistence, document addition, and semantic search functionality.
    """
    def __init__(self):
        """
        Initializes the Retriever with a persistent ChromaDB client.
        Sets up the embedding function and creates/retrieves the collection.
        
        @raises Exception: If there's an error creating or accessing the collection
        """
        # Configurar directorio para persistencia
        persist_dir = "chroma_db"
        os.makedirs(persist_dir, exist_ok=True)
        
        # Usar cliente persistente
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        try:
            print("Intentando obtener colección existente...")
            self.collection = self.client.get_or_create_collection(
                name="rick_morty",
                embedding_function=self.embedding_function
            )
            doc_count = self.collection.count()
            print(f"Colección obtenida/creada exitosamente. Documentos: {doc_count}")
        except Exception as e:
            print(f"Error al obtener/crear colección: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            print(f"Traceback completo: {traceback.format_exc()}")
            raise

    def add_documents(self, documents: List[Dict]):
        """
        Adds documents to the vector database in batches.
        
        @param documents: List of documents to add, each containing 'id', 'text', and 'metadata'
        @type documents: List[Dict]
        @raises Exception: If there's an error adding documents to the collection
        """
        if not documents:
            return
        
        print(f"Añadiendo {len(documents)} documentos...")
        
        # Procesar en lotes para evitar problemas de memoria
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            print(f"Procesando lote {i//batch_size + 1} de {len(documents)//batch_size + 1}")
            
            # Verificar conexión con ChromaDB
            print("Verificando conexión con ChromaDB...")
            try:
                self.collection.count()
                print("Conexión con ChromaDB activa")
            except Exception as e:
                print(f"Error de conexión con ChromaDB: {str(e)}")
                print(f"Tipo de error: {type(e)}")
                print(f"Traceback completo: {traceback.format_exc()}")
                raise

            ids = [doc['id'] for doc in batch]
            texts = [doc['text'] for doc in batch]
            metadatas = [doc['metadata'] for doc in batch]
            
            # Verificar tamaño de los documentos
            for doc in batch:
                if len(doc['text']) > 10000:
                    print(f"Documento muy grande: {doc['id']}, longitud: {len(doc['text'])}")
            
            print(f"IDs: {ids}")
            print(f"Textos: {[text[:100] + '...' for text in texts]}")  # Mostrar solo los primeros 100 caracteres
            print(f"Metadatas: {metadatas}")
            
            try:
                print(f"Iniciando adición del lote {i//batch_size + 1}")
                print(f"IDs: {ids}")
                print(f"Textos: {[text[:100] + '...' for text in texts]}")
                print(f"Metadatas: {metadatas}")
                self.collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas
                )
                print(f"Lote {i//batch_size + 1} añadido exitosamente")
            except Exception as e:
                print(f"Error añadiendo lote: {str(e)}")
                print(f"Tipo de error: {type(e)}")
                print(f"Traceback completo: {traceback.format_exc()}")
                raise

    def count_documents(self):
        """
        Returns the total number of documents in the collection.
        
        @return: Number of documents
        @rtype: int
        """
        return self.collection.count()

    def get_all_documents(self):
        """
        Retrieves all documents from the collection for verification purposes.
        
        @return: All documents in the collection or None if error occurs
        @rtype: Dict or None
        """
        try:
            return self.collection.get()
        except Exception as e:
            print(f"Error obteniendo documentos: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            print(f"Traceback completo: {traceback.format_exc()}")
            return None
            
    def search(self, query: str, n_results: int = 5):
        """
        Performs semantic search in the vector database.
        """
        try:
            # Detectar si la consulta es sobre una temporada específica

            season_match = re.search(r'temporada (\d+)', query.lower())
            season = f"S{int(season_match.group(1)):02d}" if season_match else None

            # Búsqueda de episodios
            if season:
                episode_results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where={
                        "$and": [
                            {"type": "episode"},
                            {"season": season}
                        ]
                    }
                )
            else:
                episode_results = self.collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    where={"type": "episode"}
                )
            
            # Búsqueda de personajes relevantes
            character_results = self.collection.query(
                query_texts=[query],
                n_results=3,
                where={"type": "character"}
            )
            
            transcription_results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where={"type": "episode"}
            )
            
            # Combinar resultados
            combined_docs = []
            combined_meta = []
            
            if episode_results['documents'][0]:
                combined_docs.extend(episode_results['documents'][0])
                combined_meta.extend(episode_results['metadatas'][0])
                combined_docs.extend(transcription_results['documents'][0])
                combined_meta.extend(transcription_results['metadatas'][0])
    
            if character_results['documents'][0]:
                combined_docs.extend(character_results['documents'][0])
                combined_meta.extend(character_results['metadatas'][0])
                
            if not combined_docs:
                print("No se encontraron resultados relevantes")
                return {"documents": [[]], "metadatas": [[]]}
                
            print(f"Total resultados encontrados: {len(combined_docs)}")
            return {
                "documents": [combined_docs],
                "metadatas": [combined_meta]
            }
                
        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            print(f"Tipo de error: {type(e)}")
            print(f"Traceback completo: {traceback.format_exc()}")
            return {"documents": [[]], "metadatas": [[]]}