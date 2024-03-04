from dsp import LM
import requests

class HuggingFaceInferenceClient(LM):
    def __init__(self, model, api_key):
        self.model = model
        self.api_key = api_key
        self.provider = "default"
        self.history = []
        self.base_url = f"https://api-inference.huggingface.co/models/{model}"

    def basic_request(self, prompt: str, **kwargs):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "inputs": prompt,
            **kwargs
        }

        response = requests.post(self.base_url, headers=headers, json=data)
        response = response.json()

        self.history.append({
            "prompt": prompt,
            "response": response,
            "kwargs": kwargs,
        })
        
        return response

    def __call__(self, prompt, only_completed=True, return_sorted=False, **kwargs):
        response = self.basic_request(prompt, **kwargs)
        completions = [result['generated_text'] for result in response]

        return completions