import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import os

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
            
            ids = [doc['id'] for doc in batch]
            texts = [doc['text'] for doc in batch]
            metadatas = [doc['metadata'] for doc in batch]
            
            try:
                self.collection.add(
                    ids=ids,
                    documents=texts,
                    metadatas=metadatas
                )
                print(f"Lote {i//batch_size + 1} añadido exitosamente")
            except Exception as e:
                print(f"Error añadiendo lote: {str(e)}")
                raise

    def search(self, query: str, n_results: int = 5):
        """
        Performs semantic search in the vector database.
        
        @param query: Search query text
        @type query: str
        @param n_results: Number of results to return
        @type n_results: int
        @return: Dictionary containing search results and metadata
        @rtype: Dict
        """
        try:
            print(f"\nBuscando: {query}")
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include_embeddings=False  # Evitar duplicados
            )
            if not results['documents'][0]:
                print("No se encontraron resultados relevantes")
                return {"documents": [[]], "metadatas": [[]]}
        
            print(f"Resultados encontrados: {len(results['documents'][0])}")
            return results
        except Exception as e:
            print(f"Error en búsqueda: {str(e)}")
            return {"documents": [[]], "metadatas": [[]]}

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
            return None