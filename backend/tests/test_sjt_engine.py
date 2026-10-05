import pytest
from app.services.evidence_integrator import score_sjt
import json
import os

def test_sjt_scoring():
    # Use config/sjt_items.json
    config_path = os.path.join(os.path.dirname(__file__), "../../config/sjt_items.json")
    with open(config_path, "r") as f:
        sjt_config = json.load(f)
        
    responses = {
        "S1": "S1D",
        "S2": "S2A",
        "S3": "S3C",
        "S4": "S4B",
        "S5": "S5A",
        "S6": "S6D",
        "S7": "S7C"
    }
    
    results = score_sjt(sjt_config, responses)
    assert results["complete"] is True
    
    params = results["parameters"]
    assert "empathy" in params
    
    # Check boundaries exact integer arithmetic for band assignment
    # e.g., if span is 3 and num is 1, 3*1 = 3, 2*span=6, 3*num >= span is True (3 >= 3) -> MODERATE
    span = params["empathy"]["span"]
    num = params["empathy"]["num"]
    band = params["empathy"]["sjt_band"]
    
    if 3 * num >= 2 * span:
        assert band == "HIGH"
    elif 3 * num >= span:
        assert band == "MODERATE"
    else:
        assert band == "LOW"
