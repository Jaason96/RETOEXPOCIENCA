from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_database
from app.routes import event_config, games, health, question_sets, questions, websocket


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    yield


app = FastAPI(
    title="Reto Científico API",
    description="Backend del juego educativo — Colegio La Nueva Esperanza",
    version="0.4.2",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(event_config.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(question_sets.router, prefix="/api")
app.include_router(games.router, prefix="/api")
app.include_router(websocket.router)
