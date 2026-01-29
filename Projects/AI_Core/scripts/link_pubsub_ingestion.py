import os
from google.cloud import discoveryengine_v1beta as discoveryengine
from dotenv import load_dotenv

load_dotenv()


def link_pubsub_ingestion():
    project_id = "gen-lang-client-0982257437"
    location = "global"
    data_store_id = "gonya90-knowledge-store"
    topic_id = f"projects/{project_id}/topics/gonya90-topic"

    os.environ["GOOGLE_CLOUD_QUOTA_PROJECT"] = project_id

    print(f"🔗 Linking Pub/Sub topic {topic_id} to Data Store {data_store_id}")

    client = discoveryengine.DocumentServiceClient()

    # Parent for branch
    parent = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}/branches/0"

    # Pub/Sub source
    # Note: For real-time ingestion via Pub/Sub, the Data Store usually needs to be configured
    # to listen to the topic. If there's no direct 'set_ingestion_source' in this version,
    # we use the ImportDocuments with a PubSubSource.

    pubsub_source = discoveryengine.ImportDocumentsRequest.PubsubSource(
        topic=topic_id,
        schema_id="gonya90",  # This matches the schema created earlier
    )

    request = discoveryengine.ImportDocumentsRequest(
        parent=parent,
        pubsub_source=pubsub_source,
        reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
    )

    try:
        operation = client.import_documents(request=request)
        print(f"⌛ Ingestion link started (Operation): {operation.operation.name}")
        # We don't necessarily wait for completion as ingestion is a continuous stream
        # but the setup operation should finish.
        result = operation.result()
        print(f"✅ Ingestion link established.")
    except Exception as e:
        print(f"❌ Failed to link Pub/Sub: {e}")


if __name__ == "__main__":
    link_pubsub_ingestion()
