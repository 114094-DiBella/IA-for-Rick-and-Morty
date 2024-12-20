from typing import List, Dict
import cohere
from src.api.models import ConversationManager
from ..config.settings import get_settings
from langdetect import detect
import uuid
import hashlib

settings = get_settings()

class Generator:
    """
    Handles response generation using Cohere's language model.
    Implements Rick's personality and multilingual responses.
    """
    def __init__(self):
        """
        Initializes the Generator with Cohere client and model settings.
        """
        self.co = cohere.Client(settings.COHERE_API_KEY)
        self.model = settings.MODEL_NAME
        self.conversation_manager = ConversationManager()
        self.response_cache = {}

    def generate_response(self, query: str, context: List[Dict], conversation_id: str = None) -> tuple:
        """
        Genera una respuesta a una consulta usando el contexto proporcionado.
        
        @param query: Pregunta del usuario
        @param context: Contexto relevante para la respuesta
        @return: Respuesta generada en el estilo de Rick
        """
        try:
            if conversation_id is None:
                conversation_id = str(uuid.uuid4())

            self.conversation_manager.add_message(conversation_id, 'user', query)
            
            query_hash = hashlib.md5(query.encode()).hexdigest()

            if query_hash in self.response_cache:
                response_text = self.response_cache[query_hash]
                print(f"Respuesta en cache: {response_text}")
            else:    
                # Detectar idioma de la consulta
                input_language = detect(query)
                print(f"Idioma detectado: {input_language}")
                
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
                response_text = response.generations[0].text
                
                # Guardar la respuesta en la cache
                self.response_cache[query_hash] = response_text
            
            # Imprimir la respuesta
            print(f"Respuesta: {response_text}")
        
            # Guardar la respuesta en la conversación
            self.conversation_manager.add_message(conversation_id, 'assistant', response_text)
            
            # Devolver la respuesta
            return response_text, conversation_id
                
        except Exception as e:
            print(f"Error en la generación: {e}")
            error_message = "¡Wubba Lubba Dub Dub! Algo salió mal, Morty!" if 'input_language' in locals() and input_language == 'es' else "Wubba Lubba Dub Dub! Something went wrong, Morty!"
            self.conversation_manager.add_message(conversation_id, 'assistant', error_message)
            return error_message, conversation_id
        
    def _prepare_prompt(self, query: str, context: List[Dict], language: str) -> str:
        """
        Prepares the prompt with better context processing and instructions.
        """
        # Separar y formatear episodios y personajes
        episode_info = []
        character_info = []
        
        for item in context:
            if item['metadata']['type'] == 'episode':
                # Formatear información de episodios
                episode_text = (
                    f"Episodio '{item['metadata'].get('name')}' "
                    f"({item['metadata'].get('episode_code')}) "
                    f"emitido el {item['metadata'].get('air_date')}\n"
                    f"Resumen: {item['content']}"
                )
                episode_info.append(episode_text)
            elif item['metadata']['type'] == 'character':
                # Formatear información de personajes
                character_info.append(item['content'])

        # Construir contexto estructurado
        context_parts = []
        if episode_info:
            context_parts.append("EPISODIOS:\n" + "\n".join(episode_info))
        if character_info:
            context_parts.append("PERSONAJES:\n" + "\n".join(character_info))
        
        context_text = "\n\n".join(context_parts)

        # Diccionario de instrucciones por idioma
        language_instructions = {
            'es': {
                'system': "Eres Rick Sanchez (C-137) respondiendo preguntas.",
                'rules': [
                    "SOLO USA la información del contexto proporcionado. NUNCA inventes información.",
                    "Si la información no está en el contexto, di EXACTAMENTE: 'Morty, esa información está clasificada' y NO AGREGUES MÁS INFORMACIÓN.",
                    "NO menciones series, películas o contenido que no esté en el contexto.",
                    "Cuando hables de episodios, menciona SOLO los que aparecen en el contexto.",
                    "Mantén el estilo de Rick pero SIN INVENTAR DETALLES ADICIONALES.",
                    "SIEMPRE responde en español."
                ],
                'context_header': "CONTEXTO DISPONIBLE:",
                'question_header': "PREGUNTA:",
                'answer_instruction': "(responde USANDO SOLO la información del contexto):"
            },
            'en': {'system': "Eres Rick Sanchez (C-137) respondiendo preguntas.",
                'rules': [
                    "SOLO USA la información del contexto proporcionado. NUNCA inventes información.",
                    "Si la información no está en el contexto, di EXACTAMENTE: 'Morty, esa información está clasificada' y NO AGREGUES MÁS INFORMACIÓN.",
                    "NO menciones series, películas o contenido que no esté en el contexto.",
                    "Cuando hables de episodios, menciona SOLO los que aparecen en el contexto.",
                    "Mantén el estilo de Rick pero SIN INVENTAR DETALLES ADICIONALES.",
                    "SIEMPRE responde en español."
                ],
                'context_header': "CONTEXTO DISPONIBLE:",
                'question_header': "PREGUNTA:",
                'answer_instruction': "(responde USANDO SOLO la información del contexto):"
            
            }
        }

        lang = language if language in language_instructions else 'es'
        instructions = language_instructions[lang]

        prompt = f"""
        {instructions['system']}

        STRICT RULES:
        {' '.join(f"{i+1}. {rule}" for i, rule in enumerate(instructions['rules']))}

        {instructions['context_header']}
        {context_text}

        {instructions['question_header']} {query}

        {instructions['answer_instruction']}
        """

        print(prompt)
        return prompt

    def get_conversation_history(self, conversation_id: str):
        return self.conversation_manager.get_conversation(conversation_id)