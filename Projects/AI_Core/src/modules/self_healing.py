import asyncio
import logging
import os
from typing import Optional

try:
    from kubernetes import client, config

    K8S_AVAILABLE = True
except ImportError:
    K8S_AVAILABLE = False

try:
    from github import Auth, Github

    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

logger = logging.getLogger("SelfHealing")


class SelfHealer:
    """
    Automated watchdog for K8s services.
    - Monitors Pod statuses
    - Detects restart loops (CrashLoopBackOff)
    - Auto-creates GitHub issues for investigation
    """

    def __init__(self, github_token: Optional[str] = None, namespace: str = "default"):
        self.namespace = namespace
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.is_active = False

        if K8S_AVAILABLE:
            try:
                # Try in-cluster first, then local kubeconfig
                try:
                    config.load_incluster_config()
                    logger.info("Loaded in-cluster K8s/GKE config")
                except config.ConfigException:
                    config.load_kube_config()
                    logger.info("Loaded local Kubeconfig")

                self.v1 = client.CoreV1Api()
                self.apps_v1 = client.AppsV1Api()
                self.is_active = True
            except Exception as e:
                logger.warning(f"Failed to load K8s config ({e}). Self-healing disabled.")
                self.is_active = False
        else:
            logger.warning("kubernetes library not installed. Self-healing disabled.")

    async def run_loop(self, check_interval: int = 300):
        """Main monitoring loop."""
        if not self.is_active:
            return

        logger.info(f"🛡 Self-Healing Watchdog started (Interval: {check_interval}s)")

        while True:
            try:
                await self.check_pods()
            except Exception as e:
                logger.error(f"Error in self-healing loop: {e}")

            await asyncio.sleep(check_interval)

    async def check_pods(self):
        """Check all pods in namespace for issues."""
        # This is blocking, run in executor
        await asyncio.to_thread(self._check_pods_sync)

    def _check_pods_sync(self):
        if not self.is_active:
            return

        pods = self.v1.list_namespaced_pod(self.namespace)
        for pod in pods.items:
            name = pod.metadata.name
            # status = pod.status.phase

            # Check container statuses
            if pod.status.container_statuses:
                for container in pod.status.container_statuses:
                    restart_count = container.restart_count
                    state = container.state

                    # Detection Logic
                    is_crashing = (state.waiting and state.waiting.reason == "CrashLoopBackOff") or (
                        state.terminated and state.terminated.exit_code != 0
                    )

                    if is_crashing or restart_count > 5:
                        logger.warning(
                            f"⚠️ Pod {name} container {container.name} is unstable! "
                            f"Restarts: {restart_count}, State: {state}"
                        )
                        self._handle_unstable_pod(pod, container)

    def _handle_unstable_pod(self, pod, container):
        """Take action on unstable pod."""
        # 1. Check if we already have an issue open
        if GITHUB_AVAILABLE and self.github_token:
            self._create_github_issue(pod, container)

        # 2. Add future auto-remediation (e.g., restart deployment if stuck)
        # For now, we just alert via logs (alerts handle the rest)

    def _create_github_issue(self, pod, container):
        try:
            gh = Github(auth=Auth.Token(self.github_token))
            # Fallback for bot repo
            try:
                repo = gh.get_repo("Unified-system-Core/Unified_System_Core")
            except Exception:
                repo = gh.get_repo("Unified-system-Core/AI_Core")

            title = f"[AUTO-HEAL] Pod {pod.metadata.name} crashing ({container.restart_count} restarts)"
            body = (
                f"**Pod:** `{pod.metadata.name}`\n"
                f"**Namespace:** `{self.namespace}`\n"
                f"**Container:** `{container.name}`\n"
                f"**Restart Count:** {container.restart_count}\n"
                f"**State:** `{container.state}`\n\n"
                "Please investigate immediately via `kubectl logs`."
            )

            # Check for existing open issues with same title
            issues = repo.get_issues(state="open", labels=["bug", "auto-heal"])
            for issue in issues:
                if f"Pod {pod.metadata.name}" in issue.title:
                    logger.info(f"Issue #{issue.number} already exists for {pod.metadata.name}")
                    return

            # Create new
            issue = repo.create_issue(title=title, body=body, labels=["bug", "auto-heal", "sev-2"])
            logger.info(f"Created GitHub Issue #{issue.number} for crashing pod {pod.metadata.name}")

        except Exception as e:
            logger.error(f"Failed to create GitHub issue: {e}")
