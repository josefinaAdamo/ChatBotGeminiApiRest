# ChatBot Gemini API

Servicio REST en Python que expone al asistente impulsado por la API de Gemini. Permite crear sesiones, cambiar el rol del bot y mantener contexto de conversación a través de HTTP.

## Requisitos

- Python 3.10 o superior
- Dependencias de `requirements.txt`
- Una clave válida de Gemini (`GEMINI_API_KEY`)

## Variables de entorno

| Variable | Descripción | Valor por defecto |
| --- | --- | --- |
| `GEMINI_API_KEY` | Clave privada de Gemini | _obligatoria_ |
| `MODEL` | Modelo a utilizar | `gemini-1.5-flash` (definir en `.env`) |
| `MAX_RETRIES` | Reintentos contra la API | `3` |
| `TIMEOUT_SECONDS` | Tiempo máximo de espera | `30` |
| `MAX_HISTORY` | Mensajes que se guardan en memoria por sesión | `12` |
| `PORT` | Puerto usado al ejecutar `python main.py` | `8000` |
| `RELOAD` | Activa recarga automática al ejecutar `python main.py` | `false` |

Puedes definirlos en un archivo `.env` en la raíz del proyecto.

## Instalación

```bash
git clone https://github.com/tuusuario/ChatBotGemini.git
cd ChatBotGemini
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Arranca el servidor FastAPI (recarga automática opcional):

```bash
uvicorn main:app --reload
# o
python main.py  # usa PORT y RELOAD definidos en el entorno
```

El servicio estará disponible bajo `http://localhost:8000`.

## Endpoints principales

- `GET /health`: Verifica que el servicio esté vivo.
- `GET /roles`: Devuelve los roles disponibles del asistente.
- `POST /chat`: Envía un mensaje al bot.

### Ejemplo `POST /chat`

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "message": "Hola, ¿podés explicarme recursión?",
        "role": "profesor"
      }'
```

Respuesta:

```json
{
  "session_id": "c9b41f8f7b154879a68ca0df5525cbba",
  "role": "profesor",
  "reply": "..."
}
```

Guarda el `session_id` y reutilízalo en la siguiente llamada para mantener el contexto. Puedes añadir `reset: true` para limpiar el historial de esa sesión o cambiar el rol enviando otro valor en `role`.

## Contribución

Las contribuciones son bienvenidas. Abre un issue o envía un pull request.
