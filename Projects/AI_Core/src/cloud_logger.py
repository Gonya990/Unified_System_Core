import logging
import os

from google.cloud import logging as cloud_logging


def setup_cloud_logging(service_name="ai-telegram-bot"):
    """
    Attaches Google Cloud Logging handler to the root logger.
    Requires GOOGLE_APPLICATION_CREDENTIALS env var to be set.
    """
    try:
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            # Try to locate it relative to this file if not set
            check_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gcp-service-account.json")
            if os.path.exists(check_path):
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = check_path
                print(f"🔧 [CloudLogger] Auto-detected credentials: {check_path}")

        # Instantiates a client
        client = cloud_logging.Client()

        # Retrieves a Cloud Logging handler based on the environment
        # you're running in and integrates the handler with the
        # Python logging module. By default this captures all logs
        # at INFO level and higher
        client.setup_logging()

        logging.info(f"☁️ Cloud Logging enabled for {service_name}")
        return True

    except Exception as e:
        print(f"⚠️ [CloudLogger] Could not enable Cloud Logging: {e}")
        return False
