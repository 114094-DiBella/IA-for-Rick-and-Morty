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
            "confidence": 0.95,
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