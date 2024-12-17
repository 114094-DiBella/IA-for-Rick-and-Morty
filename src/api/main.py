from fastapi import FastAPI, HTTPException
from .models import Query, Response
from ..modules.rag_engine import RAGEngine

"""
FastAPI application for Rick & Morty RAG (Retrieval-Augmented Generation) system.
This module provides endpoints for question answering using RAG architecture.
"""

app = FastAPI(title="Rick & Morty RAG API")
# Inicializar RAG Engine
rag_engine = None

@app.on_event("startup")
async def startup_event():
    """
    Initializes the RAG engine when the application starts.
    This is an event handler that runs at application startup.
    """
    global rag_engine
    rag_engine = RAGEngine()

@app.get("/")
async def root():
    """
    Root endpoint to verify API status.
    
    @return: Dictionary with status message
    @rtype: dict
    """
    return {"message": "Rick & Morty RAG API is running"}

@app.post("/qa", response_model=Response)
async def question_answering(query: Query):
    """
    Processes a question about Rick & Morty and returns an answer.
    
    @param query: The question to be answered
    @type query: Query
    @return: Response containing the answer and metadata
    @rtype: Response
    @raises HTTPException: If there's an error processing the query
    """
    try:
        result = await rag_engine.process_query(query.question)
        return Response(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/status")
async def get_status():
    """
    Retrieves the current status of the vector database.
    
    @return: Dictionary containing total document count and sample documents
    @rtype: dict
    """
    """Endpoint para verificar el estado de la base de datos"""
    docs = rag_engine.retriever.get_all_documents()
    return {
        "total_documents": rag_engine.retriever.count_documents(),
        "sample_docs": docs['documents'][:5] if docs else None
    }    