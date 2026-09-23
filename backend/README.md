# Backend pendiente para siguiente fase — ahora implementado en app/

Para iniciar el servidor:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Documentación Swagger: http://localhost:8000/docs
