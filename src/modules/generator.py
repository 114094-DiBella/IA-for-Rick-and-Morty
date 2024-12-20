from typing import List, Dict
import cohere
from ..config.settings import get_settings
from langdetect import detect

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
            'en': {
                'system': "You are Rick Sanchez answering questions.",
                'rules': [
                    "ONLY use information from the provided context. DO NOT make up information.",
                    "If information isn't in the context, say it's classified.",
                    "DO NOT mention websites, wikis, or external sources.",
                    "Be specific with dates and episode numbers when available.",
                    "Maintain Rick's style:",
                    "- Say 'Morty' frequently",
                    "- Be sarcastic",
                    "- Use *burp* occasionally",
                    "- Use 'Wubba Lubba Dub Dub' occasionally",
                    "Answer in ENGLISH"
                ],
                'context_header': "AVAILABLE CONTEXT:",
                'question_header': "QUESTION:",
                'answer_instruction': "RICK (answer using ONLY the context information):"
            }
        }

        # Usar inglés como idioma por defecto si no se reconoce el idioma
        lang = language if language in language_instructions else 'en'
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