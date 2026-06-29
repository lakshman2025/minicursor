import requests
from config import Config

class LLM:
    def __init__(self):
        self.endpoint = Config.LLM_ENDPOINT
        self.api_key = Config.LLM_API_KEY
        self.model = Config.LLM_MODEL

    def generate(self, prompt: str) -> str:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': self.model,
            'input': prompt,
        }
        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return self._extract_text(data)

    def _extract_text(self, data: dict) -> str:
        for item in data.get('output', []):
            if item.get('type') != 'message':
                continue
            for content in item.get('content', []):
                if content.get('type') == 'output_text':
                    return content['text']
        raise ValueError('No text output in LLM response')
