import asyncio
import logging
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents.factory import AgentFactory
from heartbeat.loop import HeartbeatDaemon
from core.database import get_db

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler("data/cryptohedge.log"),
        logging.StreamHandler()
    ]
)

async def run_orchestrator():
    """
    Initializes the CrewAI Orchestrator and executes the trading cycle.
    """
    try:
        # Initialize Agents
        agents = AgentFactory.create_agents()
        overseer = agents[0]
        
        # Define Tasks (Simplified for Sprint 1 & 2)
        # TODO: Define granular tasks for each agent based on BLUEPRINT.md
        
        # Initialize Crew
        trading_crew = Crew(
            agents=agents,
            tasks=[], # Tasks will be dynamically generated in later sprints
            process=Process.sequential,
            verbose=True
        )
        
        logging.info("CrewAI Orchestrator ready. Executing cycle...")
        # result = trading_crew.kickoff()
        # logging.info(f"Cycle Result: {result}")
        
    except Exception as e:
        logging.error(f"Orchestrator Failure: {e}")

async def main():
    """
    System Entry Point.
    """
    logging.info("Initializing CryptoHedgeAI Crew...")
    
    # Initialize Database
    db = get_db()
    
    # Check Emergency Stop
    config = db.conn.execute("SELECT value FROM system_config WHERE key = 'emergency_stop'").fetchone()
    if config and config[0].lower() == 'true':
        logging.warning("EMERGENCY STOP ACTIVE. System will not start.")
        return

    # Initialize Heartbeat Daemon
    daemon = HeartbeatDaemon(interval=60)
    
    try:
        await daemon.start(run_orchestrator)
    except KeyboardInterrupt:
        daemon.stop()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
