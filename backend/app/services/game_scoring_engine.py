from typing import List, Dict, Any
from .feature_extractor import EXTRACTORS

def extract_features(session_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    game_events = {}
    for ev in session_events:
        g = ev.get("game")
        if g:
            game_events.setdefault(g, []).append(ev)
            
    features = {}
    for game, events in game_events.items():
        if game in EXTRACTORS:
            features[game] = EXTRACTORS[game](events)
    return features

def compute_game_scores(features: Dict[str, Any]) -> Dict[str, float]:
    params = ["empathy", "conscientiousness", "collaborative_spirit", "emotional_agility", "curiosity", "creative_initiative", "motivation"]
    game_relative = {p: None for p in params}
    
    param_games = {
        "empathy": ["F1", "F2"],
        "conscientiousness": ["A1", "A2"],
        "collaborative_spirit": ["C1", "C2"],
        "emotional_agility": ["E1", "E2"],
        "curiosity": ["Q1", "Q2"],
        "creative_initiative": ["CR1", "CR3"],
        "motivation": ["M1", "M2"]
    }
    
    def score_F1(val): return val
    def score_F2(val): return val
    def score_A1(val): return val
    def score_A2(val): return val
    def score_C1(val): return val
    def score_C2(val): return val
    def score_E1(val): return max(0.0, min(1.0, 1.0 - (val - 3) / 12.0))
    def score_E2(val): return max(0.0, min(1.0, 1.0 - (val["bursts"] + val["idle_gaps"]) / 4.0))
    def score_Q1(val): return val
    def score_Q2(val): return val
    def score_CR1(val): return max(0.0, min(1.0, (val - 1) / 2.0))
    def score_CR3(val): return val
    def score_M1(val): return max(0.0, min(1.0, val / 30.0))
    def score_M2(val): return val
    
    SCORERS = {
        "F1": score_F1, "F2": score_F2,
        "A1": score_A1, "A2": score_A2,
        "C1": score_C1, "C2": score_C2,
        "E1": score_E1, "E2": score_E2,
        "Q1": score_Q1, "Q2": score_Q2,
        "CR1": score_CR1, "CR3": score_CR3,
        "M1": score_M1, "M2": score_M2
    }
    
    for p, g_list in param_games.items():
        vals = []
        for g in g_list:
            if g in features and features[g].get("invalid_reason") is None and features[g].get("value") is not None:
                val = SCORERS[g](features[g]["value"])
                vals.append(val)
        if vals:
            game_relative[p] = sum(vals) / len(vals)
            
    return game_relative
