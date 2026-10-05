from fastapi import APIRouter, Request, HTTPException
from typing import List, Dict, Any
from app.services.game_scoring_engine import extract_features, compute_game_scores
from app.services.evidence_integrator import score_sjt, integrate_evidence
import json
import os

router = APIRouter(prefix="/recruit", tags=["recruit"])

session_telemetry = {}

@router.post("/telemetry/events")
async def receive_telemetry(request: Request):
    data = await request.json()
    events = data.get("events", [])
    for ev in events:
        sid = ev.get("session_id")
        if sid:
            session_telemetry.setdefault(sid, []).append(ev)
    return {"status": "ok"}

@router.post("/evaluate/{session_id}")
async def evaluate_session(session_id: str, request: Request):
    data = await request.json()
    sjt_responses = data.get("sjt_responses", {})
    
    # Load SJT config
    config_path = os.path.join(os.path.dirname(__file__), "../../../config/sjt_items.json")
    try:
        with open(config_path, "r") as f:
            sjt_config = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="SJT config not found")
        
    sjt_res = score_sjt(sjt_config, sjt_responses)
    
    events = session_telemetry.get(session_id, [])
    features = extract_features(events)
    game_scores = compute_game_scores(features)
    
    # Simple telemetry flag checking (e.g. timeouts)
    critical_flags = any(ev.get("action") == "game_timeout" for ev in events)
    
    dossier = integrate_evidence(sjt_res, game_scores, critical_flags)
    return {"dossier": dossier}
