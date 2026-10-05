import pytest
from app.services.feature_extractor import EXTRACTORS

def test_extractors():
    # F1
    ev_f1 = [
        {"action": "round_start", "trial": "1", "data": {"peak": 80, "comfort": 30}},
        {"action": "lock_in", "trial": "1", "data": {"x_final": 55}},
        {"action": "round_start", "trial": "2", "data": {"peak": 90, "comfort": 50}},
        {"action": "lock_in", "trial": "2", "data": {"x_final": 70}},
    ]
    res_f1 = EXTRACTORS["F1"](ev_f1)
    assert res_f1["invalid_reason"] is None
    assert 0 <= res_f1["value"] <= 1
    # expected 1: (80-55)/(80-30) = 25/50 = 0.5
    # expected 2: (90-70)/(90-50) = 20/40 = 0.5
    # mean = 0.5
    assert res_f1["value"] == 0.5

    # F2
    ev_f2 = [
        {"action": "round_start", "trial": "1", "data": {"peak": 100, "comfort": 0}},
        {"action": "ask_press", "trial": "1"},
        {"action": "lock_in", "trial": "1", "data": {"x_final": 20}}, # acc = (100-20)/100 = 0.8 >= 0.7 -> adjusted
        {"action": "round_start", "trial": "2", "data": {"peak": 100, "comfort": 0}},
        {"action": "lock_in", "trial": "2", "data": {"x_final": 80}}, # acc = (100-80)/100 = 0.2 < 0.7 -> not adjusted
    ]
    res_f2 = EXTRACTORS["F2"](ev_f2)
    # 1: asked+adjusted = 1.0, 2: not asked+not adjusted = 0.0, mean = 0.5
    assert res_f2["value"] == 0.5

    # A1
    ev_a1 = [
        {"action": "item_dropped", "data": {"correct": True}},
        {"action": "item_dropped", "data": {"correct": False}},
        {"action": "item_dropped", "data": {"correct": True}},
    ]
    assert EXTRACTORS["A1"](ev_a1)["value"] == 2/3

    # A2
    ev_a2_insufficient = [
        {"action": "item_dropped", "data": {"item_id": "EXC_01"}},
        {"action": "item_dropped", "data": {"item_id": "EXC_02"}},
    ]
    assert EXTRACTORS["A2"](ev_a2_insufficient)["invalid_reason"] == "INSUFFICIENT_OBSERVATIONS"

    ev_a2_valid = [
        {"action": "item_dropped", "data": {"item_id": "EXC_01"}},
        {"action": "item_dropped", "data": {"item_id": "EXC_03"}},
        {"action": "item_dropped", "data": {"item_id": "EXC_04"}},
        {"action": "flag_toggle", "data": {"item_id": "EXC_01"}},
        {"action": "flag_toggle", "data": {"item_id": "EXC_02"}}, # FP
    ]
    res_a2 = EXTRACTORS["A2"](ev_a2_valid)
    assert res_a2["invalid_reason"] is None
    # tp = 1 (EXC_01), fp = 1 (EXC_02). precision = 1/2 = 0.5
    assert res_a2["value"] == 0.5

    # C1
    ev_c1 = [
        {"action": "section_start", "trial": "1", "data": {"deficit": 10}},
        {"action": "share_send", "trial": "1", "data": {"amount": 5}},
    ]
    assert EXTRACTORS["C1"](ev_c1)["value"] == 0.5

    # C2
    ev_c2 = [
        {"action": "coord_choice", "trial": "1", "data": {"choice": "Wait"}},
        {"action": "coord_choice", "trial": "2", "data": {"choice": "Keep painting"}},
    ]
    assert EXTRACTORS["C2"](ev_c2)["value"] == 0.5

    # E1
    ev_e1 = [
        {"action": "reversal_marker"},
        {"action": "feedback", "data": {"correct": False}},
        {"action": "feedback", "data": {"correct": True}},
        {"action": "feedback", "data": {"correct": True}},
        {"action": "feedback", "data": {"correct": True}},
    ]
    assert EXTRACTORS["E1"](ev_e1)["value"] == 4

    # E2
    ev_e2 = [
        {"action": "burst"},
        {"action": "idle_gap"},
    ]
    res_e2 = EXTRACTORS["E2"](ev_e2)["value"]
    assert res_e2["bursts"] == 1 and res_e2["idle_gaps"] == 1

    # Q1
    ev_q1 = [{"action": "panel_open", "data": {"door_id": f"D{i}"}} for i in range(5)]
    assert EXTRACTORS["Q1"](ev_q1)["value"] == 1.0

    # Q2
    ev_q2 = [
        {"action": "panel_open", "data": {"door_id": "D1", "has_closer": True}},
        {"action": "look_closer"}
    ]
    assert EXTRACTORS["Q2"](ev_q2)["value"] == 1.0

    # CR1
    ev_cr1 = [
        {"action": "release", "data": {"strategy_family": "A"}},
        {"action": "release", "data": {"strategy_family": "B"}},
    ]
    assert EXTRACTORS["CR1"](ev_cr1)["value"] == 2

    # CR3
    ev_cr3 = [
        {"action": "release", "data": {"is_post_fail": True, "config_distance": 0.3}},
        {"action": "release", "data": {"is_post_fail": True, "config_distance": 0.1}},
    ]
    assert EXTRACTORS["CR3"](ev_cr3)["value"] == 0.5

    # M1
    ev_m1 = [{"action": "stamp"} for _ in range(15)]
    assert EXTRACTORS["M1"](ev_m1)["value"] == 5

    # M2
    ev_m2 = [{"action": "stamp"} for _ in range(15)] + [{"action": "harder_option_chosen"}]
    assert EXTRACTORS["M2"](ev_m2)["value"] == 1.0

def test_values_in_range():
    # Test valid fixtures have values mapped in [0, 1] in scoring engine
    from app.services.game_scoring_engine import compute_game_scores
    features = {
        "E1": {"value": 6, "invalid_reason": None},
        "CR1": {"value": 2, "invalid_reason": None},
        "M1": {"value": 15, "invalid_reason": None}
    }
    scores = compute_game_scores(features)
    assert 0 <= scores["emotional_agility"] <= 1
    assert 0 <= scores["creative_initiative"] <= 1
    assert 0 <= scores["motivation"] <= 1
