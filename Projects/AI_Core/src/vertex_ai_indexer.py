import logging
import os

from google.cloud import discoveryengine_v1 as discoveryengine
from google.cloud import storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VertexAIIndexer")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "unified-system-413119") # Example, modify as needed
LOCATION = os.environ.get("VERTEX_LOCATION", "global")
DATASTORE_ID = os.environ.get("VERTEX_DATASTORE_ID", "knowledge-base-datastore")
BUCKET_NAME = os.environ.get("VERTEX_BUCKET_NAME", "unified-knowledge-base-bucket")
KNOWLEDGE_BASE_DIR = os.environ.get("KNOWLEDGE_BASE_DIR", "../../Agent_Context/Knowledge_Base")

class VertexAIIndexer:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.location = LOCATION
        self.datastore_id = DATASTORE_ID
        self.bucket_name = BUCKET_NAME
        self.kb_dir = os.path.abspath(KNOWLEDGE_BASE_DIR)
        self.storage_client = storage.Client(project=self.project_id)
        self.document_service_client = discoveryengine.DocumentServiceClient()

    def upload_to_gcs(self):
        """Uploads Knowledge Base files to GCS bucket for indexing."""
        logger.info(f"Uploading files from {self.kb_dir} to gs://{self.bucket_name}...")
        bucket = self.storage_client.bucket(self.bucket_name)

        # Make sure bucket exists
        if not bucket.exists():
            logger.info(f"Bucket {self.bucket_name} does not exist. Creating...")
            bucket = self.storage_client.create_bucket(self.bucket_name, location="US")

        count = 0
        for root, _, files in os.walk(self.kb_dir):
            for file in files:
                if file.endswith((".md", ".txt", ".pdf")):
                    local_path = os.path.join(root, file)
                    blob_name = os.path.relpath(local_path, self.kb_dir)
                    blob = bucket.blob(blob_name)
                    blob.upload_from_filename(local_path)
                    count += 1

        logger.info(f"Successfully uploaded {count} files to gs://{self.bucket_name}.")
        return f"gs://{self.bucket_name}/*"

    def trigger_indexing(self, gcs_uri: str):
        """Triggers a data ingestion/indexing job in Vertex AI Search."""
        logger.info(f"Triggering Vertex AI Indexing for {gcs_uri}...")

        parent = self.document_service_client.branch_path(
            project=self.project_id,
            location=self.location,
            data_store=self.datastore_id,
            branch="default_branch",
        )

        request = discoveryengine.ImportDocumentsRequest(
            parent=parent,
            gcs_source=discoveryengine.GcsSource(
                input_uris=[gcs_uri], data_schema="custom"
            ),
            reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
        )

        try:
            operation = self.document_service_client.import_documents(request=request)
            logger.info("Import operation started. Waiting for completion...")
            response = operation.result()
            logger.info(f"Import completed. Success count: {response.success_count}, Error count: {response.error_count}")
        except Exception as e:
            logger.error(f"Failed to trigger indexing: {e}")

if __name__ == "__main__":
    logger.info("Initializing Vertex AI Indexer...")
    indexer = VertexAIIndexer()
    gcs_uri = indexer.upload_to_gcs()
    # To run the ingestion, Vertex Search Datastore must be created manually first in Cloud Console.
    logger.info("Make sure Datastore is created in Google Cloud Console before triggering ingestion.")
    # indexer.trigger_indexing(gcs_uri)
