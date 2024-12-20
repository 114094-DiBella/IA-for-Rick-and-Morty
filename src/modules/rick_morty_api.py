import httpx
from typing import List, Dict

class RickMortyAPI:
    """
    Cliente para interactuar con la API de Rick and Morty.
    Maneja la obtención y procesamiento de datos.
    """
    
    BASE_URL = "https://rickandmortyapi.com/api"

    async def fetch_all_data(self) -> Dict:
        """
        Obtiene todos los datos necesarios de la API.
        
        @return: Diccionario con personajes y episodios
        @rtype: Dict
        """
        async with httpx.AsyncClient() as client:
            # Obtener datos de personajes
            characters = await self._fetch_all_pages(client, "/character")
            # Obtener datos de episodios
            episodes = await self._fetch_all_pages(client, "/episode")
            
            return {
                "characters": characters,
                "episodes": episodes
            }

    async def _fetch_all_pages(self, client: httpx.AsyncClient, endpoint: str) -> List[Dict]:
        """
        Obtiene todos los datos paginados de un endpoint.
        
        @param client: Cliente HTTP asíncrono
        @param endpoint: Endpoint de la API
        @return: Lista de resultados
        """
        results = []
        url = f"{self.BASE_URL}{endpoint}"
        
        while url:
            response = await client.get(url)
            data = response.json()
            results.extend(data['results'])
            url = data['info']['next']
            
        return results

    def process_data_for_embedding(self, data: Dict, transcriptions: Dict[str, str]) -> List[Dict]: 
        """
        Procesa los datos de la API para ser insertados en ChromaDB.
        
        @param data: Diccionario con datos de personajes y episodios
        @return: Lista de documentos procesados para embedding
        """
        documents = []
        
        # Procesar personajes
        for char in data['characters']:
            # Construir lista de relaciones y apariciones
            relationships = []
            if char.get('episode'):
                relationships.append(f"Appears in {len(char['episode'])} episodes")
            
            # Construir descripción detallada del personaje
            description = (
                f"Character Information:\n"
                f"Name: {char['name']}\n"
                f"Species: {char['species']}\n"
                f"Status: {char['status']}\n"
                f"Origin: {char['origin']['name']}\n"
                f"Location: {char['location']['name']}\n"
                f"{' '.join(relationships)}\n"
                f"Type: {char.get('type', 'Not specified')}\n"
                f"Gender: {char.get('gender', 'Not specified')}\n"
                f"Detailed description: {char['name']} is a {char['species']} who originates from "
                f"{char['origin']['name']}. They are currently {char['status'].lower()} "
                f"and were last seen in {char['location']['name']}."
            )
            
            # Crear documento para el personaje
            doc = {
                'id': f"char_{char['id']}",
                'text': description,
                'metadata': {
                    'type': 'character',
                    'name': char['name'],
                    'species': char['species'],
                    'status': char['status'],
                    'origin': char['origin']['name'],
                    'location': char['location']['name']
                }
            }
            documents.append(doc)
        
        # Procesar episodios
        for ep in data['episodes']:
            # Construir lista de personajes importantes
            characters = []
            if ep.get('characters'):
                # Tomar solo los IDs de los primeros 5 personajes
                char_ids = [char.split('/')[-1] for char in ep['characters'][:5]]
                characters.append(f"Featured characters IDs: {', '.join(char_ids)}")
            
            # Extraer temporada y número de episodio
            episode_code = ep['episode']  # Formato: "S01E01"
            season = episode_code[:3]  # "S01"
            episode_num = episode_code[3:]  # "E01"
            
            # Obtener transcripción del episodio
            transcription = transcriptions.get(ep['name'], "Transcription not available")
            description += f"\nTranscription:\n{transcription[:500]}..."

            # Construir descripción detallada del episodio
            description = (
                f"Episode Information:\n"
                f"Title: {ep['name']}\n"
                f"Episode Code: {ep['episode']}\n"
                f"Season: {season}\n"
                f"Episode Number: {episode_num}\n"
                f"Air Date: {ep['air_date']}\n"
                f"Number of characters: {len(ep.get('characters', []))}\n"
                f"{' '.join(characters)}\n"
                f"Summary: This is episode {ep['episode']} of Rick and Morty titled '{ep['name']}', "
                f"which aired on {ep['air_date']}."
            )
            
            # Crear documento para el episodio
            doc = {
                'id': f"ep_{ep['id']}",
                'text': description,
                'metadata': {
                    'type': 'episode',
                    'name': ep['name'],
                    'episode_code': ep['episode'],
                    'air_date': ep['air_date'],
                    'season': season,
                    'episode_num': episode_num,
                    'has_transcript': ep['name'] in transcriptions

                }
            }
            documents.append(doc)
        
        return documents