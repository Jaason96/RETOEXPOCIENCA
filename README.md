# Reto Científico — Colegio La Nueva Esperanza

Juego educativo sincronizado en tiempo real para feria de ciencias.

## Requisitos

- Node.js 18+
- Python 3.13 (`py -3.13` en Windows)

## Backend

```bash
cd backend
py -3.13 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- API REST: http://localhost:8000
- WebSocket: `ws://localhost:8000/ws/games/{game_id}`
- Swagger: http://localhost:8000/docs
- SQLite: `backend/data/reto_cientifico.db`

## Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: http://localhost:5173
- Configuración: `frontend/.env` → `VITE_API_URL=http://localhost:8000`

## Flujo de una partida real

1. Abrir http://localhost:5173
2. **INICIAR DESAFÍO** → configurar jugadores → **COMENZAR PARTIDA**
3. Se abre el **panel del moderador**: `/game/{id}/moderator`
4. Pulsar **ABRIR PANTALLA TV** → mover esa ventana al televisor
5. En el moderador: **ACTIVAR PULSADORES**
6. Pulsadores simulados con teclado (desde el panel del moderador):
   - Jugador 1 → `A`
   - Jugador 2 → `F`
   - Jugador 3 → `J`
   - Jugador 4 → `L`
7. Evaluar respuestas, avanzar preguntas y finalizar partida

## Fase actual

Juego funcional local con WebSockets, pulsadores por teclado y puntuación real. Sin tablets, Arduino ni autenticación.
