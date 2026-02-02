import json
import os
import time

from dotenv import load_dotenv
from google.cloud import pubsub_v1

load_dotenv()


def push_test_knowledge():
    project_id = os.getenv("GCP_PROJECT_ID", "gen-lang-client-0982257437")
    topic_id = "gonya90-topic"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Matching schema: id, content, metadata (map), timestamp
    message_data = {
        "id": f"test-{int(time.time())}",
        "content": "This is a test ground for Antigravity system logic. Arthur is an AI agent assistant.",
        "metadata": {"source": "manual_test", "category": "test_grounding"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    # Since we use JSON encoding for the topic
    data = json.dumps(message_data).encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"📡 Published message ID: {future.result()}")


if __name__ == "__main__":
    try:
        push_test_knowledge()
        print("✅ Test knowledge pushed to Pub/Sub topic 'gonya90-topic'.")
    except Exception as e:
        print(f"❌ Failed to push knowledge: {e}")
