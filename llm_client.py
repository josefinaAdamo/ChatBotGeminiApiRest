import time
from typing import Dict, List, Optional
import google.generativeai as genai
from config import Settings

class GeminiClient:
    def __init__(self, api_key: str, model_name: str):
        if not api_key:
            raise ValueError("API key no configurado")
        genai.configure(api_key=api_key)  # Corrección aquí
        self.model = genai.GenerativeModel(model_name)
        
    def generate(
        self, 
        system_prompt: str,
        history: List[Dict[str, str]],
        user_message: str,
        max_retries: int,
        timeout_seconds: int
    ) -> str:
        attempt = 0
        last_error: Optional[Exception] = None
        
        convo = self.model.start_chat(
            history=[{"role": "user", "parts": system_prompt}] +
                    [{"role": m["role"], "parts": m["parts"]} for m in history])
        
        while attempt < max_retries:
            try:
                response = convo.send_message(user_message)
                text = getattr(response, 'text', "")
                if not text:
                    raise ValueError("Respuesta vacía del modelo")
                return text
            except Exception as e:
                last_error = e
                sleep_seconds = 2 ** attempt
                time.sleep(sleep_seconds)
                attempt += 1
                
        raise RuntimeError(f"Falló después del numero maximo de reintentos") from last_error
    
                        
                    
