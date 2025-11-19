from typing import List, Dict

def build_system_prompt(role_instructions:str) -> str:
    base = (
        "sos un chatbot de consola que responde en español de forma cara y util."
        "si el usuario pide codigo, inclui explicaciones breves"
        "evita informacion inventada, y pedi aclaraciones sin faltan datos"
    )
    return base + f"Contexto de {role_instructions}"

def collapse_history(history: list[Dict[str,str]]) -> list[dict[str, str]]:
    return history
