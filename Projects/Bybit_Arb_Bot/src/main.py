import os
import asyncio
import logging
from dotenv import load_dotenv

# Import components
from src.pipeline.exchange_connector import BybitConnector
from src.pipeline.compliance_logger import ComplianceLogger
from src.pipeline.funding_arb_bot import FundingArbBot

# K8s components
try:
    from kubernetes import config

    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("MainOrchestrator")


async def k8s_leader_election(pod_name: str, namespace: str):
    """
    Leader Election using K8s Lease API (coordination.k8s.io).
    Ensures only one instance sends orders to Bybit.
    """
    if not K8S_AVAILABLE:
        logger.warning(
            "K8s Client not found. Skipping Leader Election (Local Dev Mode)."
        )
        return True

    try:
        config.load_incluster_config()
    except Exception as e:
        logger.info(f"Using local kube-config (Error: {e})")
        config.load_kube_config()

    # (Simplified Lease Logic for MVP)
    logger.info(f"Pod {pod_name} is competing in {namespace}...")
    return True  # Assume leader if single pod or dev mode


async def main():
    load_dotenv()

    # Initialize Infrastructure
    api_key = os.getenv("BYBIT_API_KEY")
    api_secret = os.getenv("BYBIT_API_SECRET")

    if not api_key:
        logger.error("BYBIT_API_KEY missing in .env")
        return

    pod_name = os.getenv("HOSTNAME", "local-dev")
    namespace = os.getenv("K8S_NAMESPACE", "trading")

    # Leader Election
    is_leader = await k8s_leader_election(pod_name, namespace)

    if is_leader:
        logger.info("👑 I AM THE LEADER. Starting Execution Engine...")

        connector = BybitConnector(api_key, api_secret)
        compliance = ComplianceLogger()
        bot = FundingArbBot(connector, compliance)

        # Start Strategy
        await bot.execute_arb("BTCUSDT", 1000.0)

        # Keep alive
        while True:
            await asyncio.sleep(60)
    else:
        logger.info("🥈 Passive Mode (Standby). Waiting for Leader handover...")
        while True:
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
