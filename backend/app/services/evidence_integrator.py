import json
import os
from typing import Dict, List, Any

PARAMS = ["empathy", "conscientiousness", "collaborative_spirit", "emotional_agility", "curiosity", "creative_initiative", "motivation"]

def score_sjt(sjt_config: Dict[str, Any], responses: Dict[str, str]) -> Dict[str, Any]:
    # responses is mapping from scenario_id -> option_id
    raw = {p: 0 for p in PARAMS}
    min_vals = {p: 0 for p in PARAMS}
    max_vals = {p: 0 for p in PARAMS}
    
    # We must only consider scenarios that were answered to calculate the possible max/min for the *answered* ones?
    # Wait, the prompt says: "min[p] = sum over scenarios of min over options of keys[p]". It usually implies all scenarios, or only answered ones?
    # If SJT is incomplete, we should probably just score the answered ones, or it's incomplete.
    # Let's sum over answered scenarios.
    
    sjt_complete = True
    if len(responses) < len(sjt_config.get("scenarios", [])):
        sjt_complete = False
        
    for scenario in sjt_config.get("scenarios", []):
        sid = scenario["id"]
        chosen_opt_id = responses.get(sid)
        
        # Calculate min/max for this scenario
        opts = scenario["options"]
        for p in PARAMS:
            p_keys = [opt["keys"][p] for opt in opts]
            min_vals[p] += min(p_keys)
            max_vals[p] += max(p_keys)
            
            if chosen_opt_id:
                chosen_opt = next((o for o in opts if o["id"] == chosen_opt_id), None)
                if chosen_opt:
                    raw[p] += chosen_opt["keys"][p]
                    
    results = {}
    for p in PARAMS:
        span = max_vals[p] - min_vals[p]
        num = raw[p] - min_vals[p]
        
        if span > 0 and sjt_complete:
            sjt_relative = num / span
            if 3 * num >= 2 * span:
                sjt_band = "HIGH"
            elif 3 * num >= span:
                sjt_band = "MODERATE"
            else:
                sjt_band = "LOW"
        else:
            sjt_relative = None
            sjt_band = None
            
        results[p] = {
            "raw": raw[p],
            "min": min_vals[p],
            "max": max_vals[p],
            "span": span,
            "num": num,
            "sjt_relative": sjt_relative,
            "sjt_band": sjt_band
        }
        
    return {"parameters": results, "complete": sjt_complete}

def integrate_evidence(sjt_results: Dict[str, Any], game_relative: Dict[str, float], telemetry_flags: bool = False) -> List[Dict[str, Any]]:
    dossier = []
    
    sjt_complete = sjt_results.get("complete", False)
    sjt_params = sjt_results.get("parameters", {})
    
    for p in PARAMS:
        s_rel = sjt_params.get(p, {}).get("sjt_relative")
        g_rel = game_relative.get(p)
        
        delta = None
        if s_rel is not None and g_rel is not None:
            delta = abs(s_rel - g_rel)
            
        if delta is None:
            relationship = "NOT_ENOUGH_EVIDENCE"
        elif delta <= 0.15:
            relationship = "ALIGNED"
        elif delta <= 0.30:
            relationship = "PARTLY_ALIGNED"
        else:
            relationship = "DIFFERENT"
            
        if not sjt_complete or telemetry_flags:
            confidence = "LIMITED"
        elif g_rel is None:
            confidence = "LIMITED"
        else:
            confidence = "MODERATE"
            
        dossier.append({
            "Dimension": p,
            "SJT relative": s_rel,
            "Game relative": g_rel,
            "Delta": delta,
            "Relationship": relationship,
            "Confidence": confidence
        })
        
    return dossier
