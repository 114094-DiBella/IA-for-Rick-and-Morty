from typing import Dict, List
from .retriever import Retriever
from .generator import Generator

class RAGEngine:
    """
    Main engine for Retrieval-Augmented Generation (RAG).
    Coordinates between retriever and generator components.
    """
    def __init__(self):
        """
        Initializes the RAG engine with retriever and generator components.
        """
        print("Inicializando RAG Engine...")
        self.retriever = Retriever()
        self.generator = Generator()
        print(f"RAG Engine inicializado. Documentos en la colección: {self.retriever.count_documents()}")

    async def process_query(self, question: str) -> Dict:
        """
        Processes a question using RAG architecture.
        
        @param question: User's question
        @type question: str
        @return: Dictionary containing answer, confidence, sources and context
        @rtype: Dict
        """
        # Buscar información relevante
        results = self.retriever.search(question)
        
        # Preparar contexto
        context = self._prepare_context(results)
        
        # Generar respuesta
        response = self.generator.generate_response(question, context)
        
        # Preparar fuentes
        sources = self._prepare_sources(results)
        
        return {
            "answer": response,
            "confidence": self._calculate_confidence(results),
            "sources": sources,
            "context_used": str(context)[:200] + "..." if context else None
        }
    def _prepare_context(self, results) -> List[Dict]:
        """
        Prepares context information from retrieval results.
        
        @param results: Raw results from retriever
        @return: List of context items with type, content and metadata
        @rtype: List[Dict]
        """
        context = []
        if results.get('documents'):
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                context.append({
                    "type": metadata['type'],
                    "content": doc,
                    "metadata": metadata
                })
        return context
    
    def _prepare_sources(self, results) -> List[Dict]:
        """
        Prepares source attribution information from results.
        
        @param results: Raw results from retriever
        @return: List of source information
        @rtype: List[Dict]
        """
        sources = []
        if results.get('metadatas'):
            for meta in results['metadatas'][0]:
                source = {
                    "type": meta['type'],
                    "id": meta.get('id', 'unknown'),
                    "title": meta.get('name', 'Unknown')
                }
                
                if meta['type'] == 'episode':
                    source["title"] = f"Episode: {meta.get('name', '?')}"
                elif meta['type'] == 'character':
                    source["title"] = f"Character: {meta.get('name', '?')}"
                
                sources.append(source)
        return sources
    
    def _calculate_confidence(self, results) -> float:
        """
        Calculates a confidence score based on the search results.
        
        @param results: Raw results from retriever
        @type results: Dict
        @return: Confidence score between 0 and 1
        @rtype: float
        """
        if not results.get('documents') or not results['documents'][0]:
            return 0.0
            
        # Factores para calcular la confianza:
        # 1. Número de documentos encontrados
        doc_count = len(results['documents'][0])
        doc_score = min(doc_count / 5, 1.0)  # Normalizar a máximo de 1
        
        # 2. Diversidad de fuentes (episodios vs personajes)
        source_types = set(meta['type'] for meta in results['metadatas'][0])
        diversity_score = len(source_types) / 2  # Normalizado por los 2 tipos posibles
        
        # 3. Calidad del contenido (longitud del texto como proxy simple)
        avg_length = sum(len(doc) for doc in results['documents'][0]) / doc_count
        length_score = min(avg_length / 500, 1.0)  # Normalizar, asumiendo 500 chars como ideal
        
        # Calcular score final (promedio ponderado)
        final_score = (doc_score * 0.4 + diversity_score * 0.3 + length_score * 0.3)
        
        return round(final_score, 2)    