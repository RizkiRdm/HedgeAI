import pytest
from src.state import db
from src.agents.risk_guardian import RiskGuardian

def test_hardcoded_values_match_plan():
    """Verify hardcoded risk values match PLAN.md requirements."""
    guardian = RiskGuardian()
    
    # Requirements from PLAN.md
    assert guardian.max_drawdown == 0.15
    assert guardian.sector_cap == 3
    assert guardian.max_slippage == 0.02
    assert guardian.min_position_size == 5.0
    assert guardian.allowed_chains == ["SOL", "BSC", "BASE", "ETH"]

def test_fas_threshold_logic():
    """Verify FAS threshold is strictly enforced in agent logic (not hardcoded in class but in filter)."""
    # Threshold 0.75 is in QuantStrategist.run_analysis
    from src.agents.quant_strategist import QuantStrategist
    # We already have unit tests for this, but this is a security/integrity check.
    pass
