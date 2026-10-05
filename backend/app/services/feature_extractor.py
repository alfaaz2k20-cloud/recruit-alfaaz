from typing import List, Dict, Any, Optional

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def extract_f1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    rounds = {}
    for ev in events:
        if ev["action"] == "lock_in":
            rnd = ev["trial"]
            rounds[rnd] = ev["data"]["x_final"]
        elif ev["action"] == "round_start":
            rnd = ev["trial"]
            if rnd not in rounds:
                rounds[rnd] = None
    
    # We need peak and comfort. These should be in round_start or config. 
    # The prompt says "The signal peak and the producer's comfort zone differ."
    # Let's assume they are in round_start data.
    acc_shares = []
    for ev in events:
        if ev["action"] == "round_start":
            rnd = ev["trial"]
            peak = ev["data"]["peak"]
            comfort = ev["data"]["comfort"]
            x_final = rounds.get(rnd)
            if x_final is not None:
                # clamp((peak - x_final)/(peak - comfort), 0, 1)
                # Ensure no division by zero
                denom = peak - comfort
                if denom == 0:
                    acc = 0.0
                else:
                    acc = clamp((peak - x_final) / denom, 0.0, 1.0)
                acc_shares.append(acc)
    
    if not acc_shares:
        return {"value": None, "invalid_reason": "MISSING_DATA"}
    return {"value": sum(acc_shares) / len(acc_shares), "invalid_reason": None}

def extract_f2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # ambiguous_response per round:
    # asked_and_adjusted = 1.0, adjusted_without_ask = 0.5, asked_no_adjust = 0.5, ignored = 0.0
    # adjusted means accommodation_share >= 0.7
    rounds = {}
    for ev in events:
        rnd = ev["trial"]
        if rnd not in rounds:
            rounds[rnd] = {"asked": False, "x_final": None, "peak": 0, "comfort": 0}
        if ev["action"] == "ask_press":
            rounds[rnd]["asked"] = True
        elif ev["action"] == "lock_in":
            rounds[rnd]["x_final"] = ev["data"]["x_final"]
        elif ev["action"] == "round_start":
            rounds[rnd]["peak"] = ev["data"]["peak"]
            rounds[rnd]["comfort"] = ev["data"]["comfort"]
            
    scores = []
    for rnd, data in rounds.items():
        if data["x_final"] is not None:
            denom = data["peak"] - data["comfort"]
            acc = clamp((data["peak"] - data["x_final"]) / denom, 0.0, 1.0) if denom != 0 else 0.0
            adjusted = acc >= 0.7
            asked = data["asked"]
            if asked and adjusted:
                scores.append(1.0)
            elif adjusted and not asked:
                scores.append(0.5)
            elif asked and not adjusted:
                scores.append(0.5)
            else:
                scores.append(0.0)
                
    if not scores:
        return {"value": None, "invalid_reason": "MISSING_DATA"}
    return {"value": sum(scores) / len(scores), "invalid_reason": None}

def extract_a1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    correct = 0
    total = 3
    for ev in events:
        if ev["action"] == "item_dropped":
            if ev["data"]["correct"]:
                correct += 1
    return {"value": correct / total, "invalid_reason": None}

def extract_a2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # items: EXC_01 (genuine), EXC_02 (control), EXC_03 (genuine), EXC_04 (genuine)
    # The game uses EXC_01, EXC_03, EXC_04 as the three items.
    # genuine_evaluated < 3 -> INVALID ("INSUFFICIENT_OBSERVATIONS")
    flags = {}
    evaluated = set()
    for ev in events:
        if ev["action"] == "flag_toggle":
            item_id = ev["data"]["item_id"]
            flags[item_id] = not flags.get(item_id, False)
        elif ev["action"] == "item_dropped":
            evaluated.add(ev["data"]["item_id"])
            
    genuine_evaluated = sum(1 for i in evaluated if i in ["EXC_01", "EXC_03", "EXC_04"])
    if genuine_evaluated < 3:
        return {"value": None, "invalid_reason": "INSUFFICIENT_OBSERVATIONS"}
        
    tp = sum(1 for i, flagged in flags.items() if flagged and i in ["EXC_01", "EXC_03", "EXC_04"])
    fp = sum(1 for i, flagged in flags.items() if flagged and i not in ["EXC_01", "EXC_03", "EXC_04"])
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    return {"value": precision, "invalid_reason": None}

def extract_c1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    sections = {}
    for ev in events:
        sec = ev["trial"]
        if sec not in sections:
            sections[sec] = {"sent": 0, "deficit": 0}
        if ev["action"] == "section_start":
            sections[sec]["deficit"] = ev["data"]["deficit"]
        elif ev["action"] == "share_send":
            sections[sec]["sent"] += ev["data"]["amount"]
            
    shares = []
    for sec, data in sections.items():
        if data["deficit"] > 0:
            shares.append(clamp(data["sent"] / data["deficit"], 0.0, 1.0))
            
    if not shares:
        return {"value": None, "invalid_reason": "MISSING_DATA"}
    return {"value": sum(shares) / len(shares), "invalid_reason": None}

def extract_c2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    sections = {}
    for ev in events:
        sec = ev["trial"]
        if sec not in sections:
            sections[sec] = {"choice": None}
        if ev["action"] == "coord_choice":
            sections[sec]["choice"] = ev["data"]["choice"]
            
    scores = []
    for sec, data in sections.items():
        if data["choice"] in ["Wait", "Signal"]:
            scores.append(1.0)
        elif data["choice"] == "Keep painting":
            scores.append(0.0)
            
    if not scores:
        return {"value": None, "invalid_reason": "MISSING_DATA"}
    return {"value": sum(scores) / len(scores), "invalid_reason": None}

def extract_e1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # trials from reversal to first run of 3 consecutive correct
    reversal_idx = -1
    consecutive_correct = 0
    trials_after_reversal = 0
    found = False
    
    for ev in events:
        if ev["action"] == "reversal_marker":
            reversal_idx = 0
        elif ev["action"] == "feedback" and reversal_idx >= 0:
            trials_after_reversal += 1
            if ev["data"]["correct"]:
                consecutive_correct += 1
                if consecutive_correct == 3:
                    found = True
                    break
            else:
                consecutive_correct = 0
                
    if reversal_idx == -1:
        return {"value": None, "invalid_reason": "NO_REVERSAL"}
        
    val = trials_after_reversal if found else 15
    val = min(val, 15)
    return {"value": val, "invalid_reason": None}

def extract_e2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    bursts = sum(1 for ev in events if ev["action"] == "burst")
    idle_gaps = sum(1 for ev in events if ev["action"] == "idle_gap")
    return {"value": {"bursts": bursts, "idle_gaps": idle_gaps}, "invalid_reason": None}

def extract_q1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    doors = set()
    for ev in events:
        if ev["action"] == "panel_open":
            doors.add(ev["data"]["door_id"])
    return {"value": len(doors) / 5.0, "invalid_reason": None}

def extract_q2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    opportunities = 0
    used = 0
    for ev in events:
        if ev["action"] == "panel_open" and ev["data"].get("has_closer", False):
            opportunities += 1
        elif ev["action"] == "look_closer":
            used += 1
    if opportunities == 0:
        return {"value": None, "invalid_reason": "NO_OPPORTUNITIES"}
    return {"value": used / opportunities, "invalid_reason": None}

def extract_cr1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    families = set()
    for ev in events:
        if ev["action"] == "release":
            families.add(ev["data"].get("strategy_family", "unknown"))
    return {"value": len(families), "invalid_reason": None}

def extract_cr3(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    post_fail_total = 0
    post_fail_diff = 0
    for ev in events:
        if ev["action"] == "release" and ev["data"].get("is_post_fail", False):
            post_fail_total += 1
            if ev["data"].get("config_distance", 0.0) >= 0.25:
                post_fail_diff += 1
                
    if post_fail_total == 0:
        return {"value": None, "invalid_reason": "NO_FAILS"}
    return {"value": post_fail_diff / post_fail_total, "invalid_reason": None}

def extract_m1(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    stamps = sum(1 for ev in events if ev["action"] == "stamp")
    extra_units = max(0, stamps - 10)
    if extra_units == 0:
        return {"value": None, "invalid_reason": "NEUTRAL_STOP"}
    return {"value": extra_units, "invalid_reason": None}

def extract_m2(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    # We must check if M1's extra_units == 0
    stamps = sum(1 for ev in events if ev["action"] == "stamp")
    extra_units = max(0, stamps - 10)
    if extra_units == 0:
        return {"value": None, "invalid_reason": "NEUTRAL_STOP"}
        
    chose = 0
    for ev in events:
        if ev["action"] == "harder_option_chosen":
            chose = 1
    return {"value": float(chose), "invalid_reason": None}

EXTRACTORS = {
    "F1": extract_f1,
    "F2": extract_f2,
    "A1": extract_a1,
    "A2": extract_a2,
    "C1": extract_c1,
    "C2": extract_c2,
    "E1": extract_e1,
    "E2": extract_e2,
    "Q1": extract_q1,
    "Q2": extract_q2,
    "CR1": extract_cr1,
    "CR3": extract_cr3,
    "M1": extract_m1,
    "M2": extract_m2
}
