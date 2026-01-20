import os
import requests

class GeminiBridge:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"

    def ask(self, prompt):
        if not self.api_key:
            return "Error: Gemini API key not configured."

        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        try:
            response = requests.post(self.url, json=payload, timeout=15)
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Gemini connection failed: {str(e)}"
