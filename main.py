import os
import uuid
from threading import Lock
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from chat_service import ChattService
from roles import ROLES_SYSTEM_PROMPT, RolesPreset


class SessionManager:
    """Simple in-memory session registry for chat services."""

    def __init__(self):
        self._sessions: Dict[str, ChattService] = {}
        self._lock = Lock()

    def _create(self, role: RolesPreset) -> Tuple[str, ChattService]:
        session_id = uuid.uuid4().hex
        service = ChattService(roles=role)
        self._sessions[session_id] = service
        return session_id, service

    def get_or_create(
        self, session_id: Optional[str], role: Optional[RolesPreset]
    ) -> Tuple[str, ChattService]:
        with self._lock:
            if session_id:
                service = self._sessions.get(session_id)
                if not service:
                    raise KeyError(session_id)
            else:
                session_id, service = self._create(role or RolesPreset.ASISTENTE)

            if role:
                service.set_role(role)
            return session_id, service

    def reset(self, session_id: str):
        service = self.get(session_id)
        service.reset()

    def get(self, session_id: str) -> ChattService:
        with self._lock:
            service = self._sessions.get(session_id)
        if not service:
            raise KeyError(session_id)
        return service


session_manager = SessionManager()

app = FastAPI(
    title="ChatBot Gemini API",
    version="1.0.0",
    description="API REST para interactuar con el bot impulsado por Gemini.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Mensaje del usuario.")
    session_id: Optional[str] = Field(
        None, description="Identificador de sesión para mantener contexto."
    )
    role: Optional[RolesPreset] = Field(
        None,
        description="Rol del bot. También se puede usar para cambiar el rol de una sesión existente.",
    )
    reset: bool = Field(
        default=False,
        description="Si es verdadero, la sesión se reinicia antes de procesar el mensaje.",
    )


class ChatResponse(BaseModel):
    session_id: str
    role: RolesPreset
    reply: str


class RoleInfo(BaseModel):
    id: RolesPreset
    description: str


def _role_description(role: RolesPreset) -> str:
    description = ROLES_SYSTEM_PROMPT.get(role, "")
    if isinstance(description, (tuple, list)):
        return " ".join(description)
    return str(description)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.get("/roles", response_model=List[RoleInfo])
def list_roles():
    return [
        RoleInfo(id=role, description=_role_description(role))
        for role in RolesPreset
    ]


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest):
    message = payload.message.strip()
    if not message:
        raise HTTPException(status_code=422, detail="El mensaje no puede estar vacío.")

    try:
        session_id, chat_service = session_manager.get_or_create(
            payload.session_id, payload.role
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")

    if payload.reset:
        chat_service.reset()

    try:
        reply = chat_service.ask(message)
    except Exception as exc:  # pragma: no cover - passthrough to client
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(session_id=session_id, role=chat_service.roles, reply=reply)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
