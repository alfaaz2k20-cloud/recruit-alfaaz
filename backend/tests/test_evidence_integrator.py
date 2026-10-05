import pytest
from app.services.evidence_integrator import integrate_evidence

def test_evidence_integrator():
    sjt_results = {
        "complete": True,
        "parameters": {
            "empathy": {"sjt_relative": 0.8},
            "conscientiousness": {"sjt_relative": 0.5},
            "collaborative_spirit": {"sjt_relative": 0.2},
            "emotional_agility": {"sjt_relative": 0.9},
            "curiosity": {"sjt_relative": 0.4},
            "creative_initiative": {"sjt_relative": 0.5},
            "motivation": {"sjt_relative": 0.7}
        }
    }
    
    game_relative = {
        "empathy": 0.7, # delta 0.1 -> ALIGNED
        "conscientiousness": 0.3, # delta 0.2 -> PARTLY_ALIGNED
        "collaborative_spirit": 0.6, # delta 0.4 -> DIFFERENT
        "emotional_agility": None, # None -> NOT_ENOUGH_EVIDENCE
        "curiosity": 0.4,
        "creative_initiative": 0.5,
        "motivation": 0.7
    }
    
    dossier = integrate_evidence(sjt_results, game_relative, telemetry_flags=False)
    
    for row in dossier:
        assert "Dimension" in row
        assert "SJT relative" in row
        assert "Game relative" in row
        assert "Delta" in row
        assert "Relationship" in row
        assert "Confidence" in row
        
        # Check no composite or fused keywords
        assert "fused" not in str(row).lower()
        assert "composite" not in str(row).lower()
        assert "rank" not in str(row).lower()
        assert "recommended" not in str(row).lower()
        assert "overall" not in str(row).lower()
        
    emp = next(r for r in dossier if r["Dimension"] == "empathy")
    assert emp["Relationship"] == "ALIGNED"
    assert emp["Confidence"] == "MODERATE"
    
    cons = next(r for r in dossier if r["Dimension"] == "conscientiousness")
    assert cons["Relationship"] == "PARTLY_ALIGNED"
    
    col = next(r for r in dossier if r["Dimension"] == "collaborative_spirit")
    assert col["Relationship"] == "DIFFERENT"
    
    emo = next(r for r in dossier if r["Dimension"] == "emotional_agility")
    assert emo["Relationship"] == "NOT_ENOUGH_EVIDENCE"
    assert emo["Confidence"] == "LIMITED"
    
    # Check separate fields
    assert "SJT relative" in emp
    assert "Game relative" in emp

def test_telemetry_flags():
    sjt_results = {
        "complete": True,
        "parameters": {
            "empathy": {"sjt_relative": 0.8},
        }
    }
    game_relative = {"empathy": 0.7}
    
    dossier = integrate_evidence(sjt_results, game_relative, telemetry_flags=True)
    emp = next(r for r in dossier if r["Dimension"] == "empathy")
    assert emp["Confidence"] == "LIMITED"
