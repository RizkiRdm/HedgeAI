# src/core/kelly_sizer.py

def calculate_kelly(win_rate: float, avg_rr: float) -> float:
    """
    Kelly Criterion: f = W - (1-W)/R
    W = win_rate (0.0-1.0), R = avg risk/reward ratio
    Returns half-Kelly: result * 0.5
    Hard cap: 0.02 (2% max of equity) — HARDCODED.
    """
    if avg_rr <= 0 or win_rate <= 0:
        return 0.0
    
    # Kelly formula
    kelly = win_rate - ((1 - win_rate) / avg_rr)
    
    # Half-Kelly for safety
    half_kelly = kelly * 0.5
    
    # Hard cap 2%
    return max(0.0, min(0.02, float(half_kelly)))
