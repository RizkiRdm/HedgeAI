from crewai import Task
from typing import List
from tools.trading_tools import TradingTools

class TaskFactory:
    @staticmethod
    def create_tasks(agents: list) -> List[Task]:
        overseer, oracle, strategist, risk, trader, accountant, evaluator = agents

        # Task 1: Data Gathering
        fetch_data_task = Task(
            description="Scan the market for low-cap altcoins with high liquidity (>50k) and volume surge. Fetch 28 core metrics.",
            expected_output="A structured JSON list of potential altcoin candidates with their raw metrics.",
            agent=oracle,
            tools=[TradingTools.hunt_altcoins]
        )

        # Task 2: Quant Analysis
        analyze_alpha_task = Task(
            description="Calculate the Final Alpha Score (FAS) for each candidate using the formula: (0.4*MS) + (0.2*RAR) + (0.3*OCHS) + (0.1*NS).",
            expected_output="A list of tickers with FAS scores. Only include those with FAS >= 75.",
            agent=strategist,
            context=[fetch_data_task]
        )

        # Task 3: Risk Assessment
        risk_veto_task = Task(
            description="Review the high-FAS candidates. Apply Max 2% risk sizing, check sector caps, and simulate slippage.",
            expected_output="A final approved list of trades with specific position sizes (Half-Kelly).",
            agent=risk,
            context=[analyze_alpha_task]
        )

        # Task 4: Execution
        execution_task = Task(
            description="Execute spot buy orders for the approved candidates via CCXT. Ensure slippage < 2%.",
            expected_output="Execution report with order IDs and final slippage values.",
            agent=trader,
            tools=[TradingTools.execute_trade],
            context=[risk_veto_task]
        )

        # Task 5: Accounting & Tax
        accounting_task = Task(
            description="Log the trades into DuckDB. Calculate and transfer 0.5% profit tax to ops_wallet if applicable.",
            expected_output="Updated balance sheet and confirmation of tax transfer.",
            agent=accountant,
            context=[execution_task]
        )

        return [fetch_data_task, analyze_alpha_task, risk_veto_task, execution_task, accounting_task]
