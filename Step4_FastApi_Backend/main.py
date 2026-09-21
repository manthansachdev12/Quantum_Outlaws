
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3, os, uuid
from datetime import datetime, timezone

from quantum_engine.engine import bell_state, run_teleportation
from quantum_engine.attacks import forgery_attack, impersonation_attack, ReplayGuard
from quantum_engine.calibration import calibrate, load_baseline
from quantum_engine.detection import detect_channel

app = FastAPI(
    title="SIH26141 Quantum Security API",
    description="Prototype backend for quantum-inspired digital-signature threat detection. No AI/ML.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH=os.path.join(os.path.dirname(__file__), "data", "results.db")
replay_guard=ReplayGuard()

def db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con=sqlite3.connect(DB_PATH)
    con.row_factory=sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS results(
        id TEXT PRIMARY KEY, timestamp TEXT, scenario TEXT, decision TEXT, risk_score INTEGER, result_json TEXT
    )""")
    con.commit()
    return con

def save_result(scenario, result, decision=None, risk_score=0):
    rid=str(uuid.uuid4())
    decision=decision or ("THREAT DETECTED" if result.get("detected") else "NORMAL")
    con=db()
    import json
    con.execute("INSERT INTO results VALUES(?,?,?,?,?,?)",
                (rid, datetime.now(timezone.utc).isoformat(), scenario, decision, int(risk_score), json.dumps(result)))
    con.commit(); con.close()
    return rid

class VerifyRequest(BaseModel):
    shots: int = Field(4096, ge=256, le=100000)
    noise_probability: float = Field(0.01, ge=0.0, le=1.0)

class ChannelRequest(BaseModel):
    shots: int = Field(4096, ge=256, le=100000)
    noise_probability: float = Field(0.08, ge=0.0, le=1.0)
    likelihood_threshold: float = Field(10.0, gt=0.0)

class CalibrateRequest(BaseModel):
    repetitions: int = Field(50, ge=5, le=500)
    shots: int = Field(4096, ge=256, le=100000)
    noise_probability: float = Field(0.01, ge=0.0, le=1.0)

class ForgeryRequest(BaseModel):
    original_signature: str
    modified_signature: str

class ImpersonationRequest(BaseModel):
    expected_signer: str
    presented_signer: str

class ReplayRequest(BaseModel):
    signature_id: str

@app.get("/health")
def health():
    return {"status":"ok", "service":"SIH26141", "ai_ml_used":False}

@app.get("/baseline")
def baseline():
    data=load_baseline()
    if data is None:
        raise HTTPException(404, "Baseline not calibrated. Run POST /calibrate.")
    return data

@app.post("/calibrate")
def calibrate_api(req: CalibrateRequest):
    return {"status":"calibrated", "baseline":calibrate(req.repetitions, req.shots, req.noise_probability)}

@app.post("/verify")
def verify(req: VerifyRequest):
    counts=bell_state(req.shots, req.noise_probability)
    total=req.shots
    unexpected=counts.get("01",0)+counts.get("10",0)
    deviation=unexpected/total*100
    baseline=load_baseline()
    threshold=baseline["threshold_percent"] if baseline else None
    detected=(threshold is not None and deviation>threshold)
    result={
        "scenario":"normal_verification",
        "counts":counts,
        "shots":total,
        "observed_deviation_percent":deviation,
        "threshold_percent":threshold,
        "decision":"THREAT DETECTED" if detected else "NORMAL",
        "risk_score":100 if detected else 0
    }
    rid=save_result("normal_verification", result, result["decision"], result["risk_score"])
    result["result_id"]=rid
    return result

@app.post("/attack/channel")
def channel(req: ChannelRequest):
    try:
        result=detect_channel(req.shots, req.noise_probability, req.likelihood_threshold)
    except RuntimeError as e:
        raise HTTPException(400, str(e))
    rid=save_result("channel_manipulation", result, result["decision"], result["risk_score"])
    result["result_id"]=rid
    return result

@app.post("/attack/forgery")
def forgery(req: ForgeryRequest):
    result=forgery_attack(req.original_signature, req.modified_signature)
    result["risk_score"]=100 if result["detected"] else 0
    result["result_id"]=save_result("forgery", result, None, result["risk_score"])
    return result

@app.post("/attack/impersonation")
def impersonation(req: ImpersonationRequest):
    result=impersonation_attack(req.expected_signer, req.presented_signer)
    result["risk_score"]=100 if result["detected"] else 0
    result["result_id"]=save_result("impersonation", result, None, result["risk_score"])
    return result

@app.post("/attack/replay")
def replay(req: ReplayRequest):
    result=replay_guard.check(req.signature_id)
    result["risk_score"]=100 if result["detected"] else 0
    result["result_id"]=save_result("replay", result, None, result["risk_score"])
    return result

@app.get("/results")
def results(limit: int=20):
    limit=max(1,min(limit,100))
    con=db()
    rows=con.execute("SELECT id,timestamp,scenario,decision,risk_score FROM results ORDER BY timestamp DESC LIMIT ?",(limit,)).fetchall()
    con.close()
    return [dict(r) for r in rows]

@app.get("/results/{result_id}")
def result_by_id(result_id: str):
    import json
    con=db()
    row=con.execute("SELECT * FROM results WHERE id=?",(result_id,)).fetchone()
    con.close()
    if row is None:
        raise HTTPException(404,"Result not found")
    item=dict(row)
    item["result"]=json.loads(item.pop("result_json"))
    return item

@app.get("/")
def root():
    return {"message":"SIH26141 Quantum Security API","docs":"/docs"}
