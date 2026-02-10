import logging

from google.api_core import exceptions
from google.cloud import secretmanager

logger = logging.getLogger(__name__)

class SecretManager:
    """Helper class to fetch secrets from Google Cloud Secret Manager."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        """
        Fetch a secret value from GCP Secret Manager.
        Returns the secret value or an empty string if not found.
        """
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        try:
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        except exceptions.NotFound:
            logger.warning(f"Secret {secret_id} not found in project {self.project_id}")
            return ""
        except Exception as e:
            logger.error(f"Error fetching secret {secret_id}: {e}")
            return ""

    def load_all_secrets(self, prefix: str = "") -> dict:
        """
        Convenience method to load common bot secrets.
        Returns a dict of secret_name: value.
        """
        secrets_to_fetch = [
            "telegram-bot-token",
            "gemini-api-key",
            "openai-api-key",
            "serpapi-key",
            "linear-api-key",
            "ha-token",
            "github-token",
            "allowed-users"
        ]

        results = {}
        for sid in secrets_to_fetch:
            val = self.get_secret(sid)
            if val:
                # Map back to environment variable names (convention)
                env_name = sid.upper().replace("-", "_")
                results[env_name] = val
        return results
