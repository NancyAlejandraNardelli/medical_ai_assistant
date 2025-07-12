import os
import requests
from typing import Dict, List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

load_dotenv()

class MedicalAPIClient:
    def __init__(self):
        self.base_url = os.getenv('MED_ASSISTANT_API')
        self.hf_token = os.getenv('HF_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.hf_token}' if self.hf_token else ''
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_cases(self) -> List[Dict]:
        try:
            response = requests.get(f'{self.base_url}/cases', headers=self.headers)
            response.raise_for_status()
            return response.json()
        except:
            # Mock data if API fails
            return [{'id': 'demo-1', 'title': 'Caso Demo 1'}]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def get_summary(self, case_id: str) -> Dict:
        try:
            response = requests.get(f'{self.base_url}/summary/{case_id}', headers=self.headers)
            response.raise_for_status()
            return response.json()
        except:
            return {
                'sections': {
                    'Diagnóstico': 'Datos de ejemplo - diagnóstico',
                    'Laboratorio': 'Datos de ejemplo - laboratorio',
                    'Tratamiento': 'Datos de ejemplo - tratamiento'
                }
            }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def chat(self, chat_id: str, query: str) -> Dict:
        try:
            response = requests.post(
                f'{self.base_url}/chat',
                headers=self.headers,
                json={'chat_id': chat_id, 'query': query}
            )
            response.raise_for_status()
            return response.json()
        except:
            return {'answer': 'Lo siento, no puedo procesar tu consulta en este momento.'}

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_file(self, chat_id: str, file) -> Dict:
        try:
            files = {'file': file}
            data = {'chat_id': chat_id}
            response = requests.post(
                f'{self.base_url}/upload',
                headers=self.headers,
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
        except:
            return {'ok': False, 'error': 'Error al subir el archivo'}

    def get_files(self, chat_id: str) -> List[Dict]:
        try:
            response = requests.get(f'{self.base_url}/files/{chat_id}', headers=self.headers)
            response.raise_for_status()
            return response.json()
        except:
            return []

api_client = MedicalAPIClient()