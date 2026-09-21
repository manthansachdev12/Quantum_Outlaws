# SIH26141 Step 4 — FastAPI Backend

## What this step adds
- FastAPI REST backend
- Swagger UI at `/docs`
- Persistent quantum baseline from Step 3
- Quantum verification endpoint
- Channel-manipulation detection
- Forgery, impersonation and replay endpoints
- SQLite result logging
- CORS for a future React frontend
- No AI/ML

## Setup (Windows PowerShell)

```powershell
cd SIH26141_Step4
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 1. Calibrate once
```powershell
python -m quantum_engine.calibration
```
If the module does not have a CLI entry in your environment, use the API after starting the server:
`POST /calibrate`

## 2. Start server
```powershell
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

## Main endpoints
- GET `/health`
- GET `/baseline`
- POST `/calibrate`
- POST `/verify`
- POST `/attack/channel`
- POST `/attack/forgery`
- POST `/attack/impersonation`
- POST `/attack/replay`
- GET `/results`
- GET `/results/{result_id}`

This is a controlled simulation/prototype, not a production QDS implementation or formal security proof.
