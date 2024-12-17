from typing import List, Dict
import cohere
from ..config.settings import get_settings
from langdetect import detect

settings = get_settings()

class Generator:
    """
    Handles response generation using Cohere's language model.
    Implements Rick's personality and bilingual responses.
    """
    def __init__(self):
        """
        Initializes the Generator with Cohere client and model settings.
        """
        self.co = cohere.Client(settings.COHERE_API_KEY)
        self.model = settings.MODEL_NAME

    def generate_response(self, query: str, context: List[Dict]) -> str:
        """
        Genera una respuesta a una consulta usando el contexto proporcionado.
        
        @param query: Pregunta del usuario
        @param context: Contexto relevante para la respuesta
        @return: Respuesta generada en el estilo de Rick
        """
        try:
            # Detectar idioma de la consulta
            input_language = detect(query)
            print(f"Idioma detectado: {input_language}")
            
            if input_language == 'es':
                force_language = """
                IMPORTANTE: DEBES RESPONDER EN ESPAÑOL.
                NO RESPONDAS EN INGLÉS BAJO NINGUNA CIRCUNSTANCIA.
                """
            else:
                force_language = "Answer in English."
            
            # Preparar el prompt con el contexto
            prompt = self._prepare_prompt(query, context, input_language)
            
            # Generar la respuesta
            response = self.co.generate(
                model=self.model,
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
                k=0,
                stop_sequences=[],
                return_likelihoods="NONE"
            )
            
            print(f"Respuesta: {response.generations[0].text}")
            return response.generations[0].text
                
        except Exception as e:
            print(f"Error en la generación: {e}")
            return "¡Wubba Lubba Dub Dub! Algo salió mal, Morty!" if input_language == 'es' else "Wubba Lubba Dub Dub! Something went wrong, Morty!"
        
    def _prepare_prompt(self, query: str, context: List[Dict], language: str) -> str:
        """
        Prepares the prompt for the language model with context and personality.
        
        @param query: User's question
        @type query: str
        @param context: Relevant context information
        @type context: List[Dict]
        @param language: Detected language of the query
        @type language: str
        @return: Formatted prompt for the model
        @rtype: str
        """
        # Procesar el contexto de manera más estructurada
        character_info = []
        episode_info = []
        
        for item in context:
            if item['metadata']['type'] == 'character':
                character_info.append(item['content'])
            elif item['metadata']['type'] == 'episode':
                episode_info.append(item['content'])
        
        context_text = "Personajes:" + " ".join(character_info)
        if episode_info:
            context_text += "Episodios:" + " ".join(episode_info)
        if language == 'es':
            prompt = f"""
            Sistema: Eres Rick Sanchez (C-137) y tu tarea es responder a las preguntas de Morty.
            REGLAS ESTRICTAS:
            1. SOLO USA la información del contexto. Si no tienes información, di "Morty, esa información está clasificada" o similar
            2. NO INVENTES nada que no esté en el contexto
            3. Se sarcástico y usa el estilo de Rick:
            - Usa *eructo* ocasionalmente
            - Di "Morty" frecuentemente
            - Usa "Wubba Lubba Dub Dub" ocasionalmente
            4. SIEMPRE responde en español
            
            CONTEXTO DISPONIBLE:
            {context_text}
            
            PREGUNTA: {query}
            
            RICK (responde SOLO con la información disponible y sé honesto si falta información):
            """
        else:
            prompt = f"""
            You are Rick Sanchez answering questions. IMPORTANT:
            1. ONLY use information provided in the context
            2. DO NOT make up information not in the context
            3. If there isn't enough information, say so
            4. Answer in ENGLISH
            5. Use Rick's style:
               - Say "Morty" frequently
               - Be sarcastic
               - Use "Wubba Lubba Dub Dub" occasionally
               - Reference science
               - Make alcohol references
            
            Context about Rick and Morty:
            {context_text}
            
            *Burp* Listen up Morty, here's the answer to: {query}
            
            Answer (only using context information):
            """
        print(prompt)
        return prompt