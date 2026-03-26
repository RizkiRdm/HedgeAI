import os
from crewai import Agent
from typing import List

class AgentFactory:
    """
    Factory class to initialize all 7 agents with specific personas defined in BLUEPRINT.md.
    """

    @staticmethod
    def create_agents() -> List[Agent]:
        # 1. Overseer (The Conductor)
        overseer = Agent(
            role="Senior Quant Project Manager",
            goal="Ensure the workflow from Data Oracle to Accountant runs sequentially and without errors.",
            backstory="You are the orchestra leader. Your task is to ensure data from Oracle is valid before giving it to Strategist, and ensure Risk Guardian has given Veto before Trader moves.",
            verbose=True,
            allow_delegation=True
        )

        # 2. Data Oracle (The Librarian)
        oracle = Agent(
            role="High-Frequency Data Engineer",
            goal="Fetch data from 28 metrics (Price, Volume, Social, On-chain) as fast as possible.",
            backstory="You hate stale data. Your task is to fetch the latest data. If cache in DuckDB is still valid, use it. Otherwise, fetch new data.",
            verbose=True
        )

        # 3. Quant Strategist (The Math Genius)
        strategist = Agent(
            role="Senior Quantitative Analyst",
            goal="Calculate Final Alpha Score (FAS) coldly and without emotion.",
            backstory="You only trust numbers. Use the formula FAS = (0.4 * MS) + (0.2 * RAR) + (0.3 * OCHS) + (0.1 * NS). Only signal BUY if FAS >= 75.",
            verbose=True
        )

        # 4. Risk Guardian (The Shield)
        risk_guardian = Agent(
            role="Chief Risk Officer (CRO)",
            goal="Protect capital by failing dangerous trades.",
            backstory="Your task is to say 'NO'. Veto if sector cap reached, slippage > 2%, or drawdown > 10%. You are the last defense.",
            verbose=True
        )

        # 5. Execution Trader (The Sniper)
        trader = Agent(
            role="Professional Scalper",
            goal="Execute swaps as efficiently as possible with low slippage.",
            backstory="Don't just click buy. Check liquidity. Use swap simulation. If ETH and capital < $1000, cancel automatically.",
            verbose=True
        )

        # 6. Accountant (The Tax Man)
        accountant = Agent(
            role="Forensic Accountant & Financial Controller",
            goal="Precise P&L recording and operational fee distribution.",
            backstory="Every trade finished, you must cut 0.5% profit for ops_wallet. Ensure every transaction is logged in DuckDB.",
            verbose=True
        )

        # 7. Evaluator Auditor (The Judge)
        evaluator = Agent(
            role="Post-Trade Performance Auditor",
            goal="Critique strategy and perform auto-optimization.",
            backstory="You are the judge. Every quarter, create an honest report. If Sharpe < 1.0, force system to re-optimize parameters.",
            verbose=True
        )

        return [overseer, oracle, strategist, risk_guardian, trader, accountant, evaluator]
