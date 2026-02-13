import asyncio
import json
import logging
import os
import sys

# Ensure proper path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.cloud import pubsub_v1  # noqa: E402

logger = logging.getLogger("AlertListener")


class AlertListener:
    def __init__(self, project_id, subscription_id):
        self.project_id = project_id
        # Use full path if provided, else construct it
        if "/" in subscription_id:
            self.subscription_path = subscription_id
        else:
            self.subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"
        self.subscriber = None
        self.streaming_pull_future = None

    def start(self, callback_coro, loop):
        """
        Starts listening for messages.
        :param callback_coro: async function(data: dict)
        :param loop: asyncio loop to schedule callback on
        """
        try:
            self.subscriber = pubsub_v1.SubscriberClient()
            logger.info(f"🎧 Listening for alerts on {self.subscription_path}...")

            def sync_callback(message):
                try:
                    data_str = message.data.decode("utf-8")
                    try:
                        json_data = json.loads(data_str)
                    except json.JSONDecodeError:
                        json_data = {"raw_text": data_str}

                    message.ack()
                    asyncio.run_coroutine_threadsafe(callback_coro(json_data), loop)

                except Exception as e:
                    logger.error(f"Error processing alert: {e}")
                    message.nack()

            self.streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=sync_callback)
        except Exception as e:
            logger.error(f"Failed to start AlertListener: {e}")

    def stop(self):
        if self.streaming_pull_future:
            self.streaming_pull_future.cancel()
        if self.subscriber:
            self.subscriber.close()
