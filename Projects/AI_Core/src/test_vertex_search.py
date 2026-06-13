import logging
import os

from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1 as discoveryengine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VertexSearchTester")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "unified-system-413119")
LOCATION = os.environ.get("VERTEX_LOCATION", "global")
DATASTORE_ID = os.environ.get("VERTEX_DATASTORE_ID", "knowledge-base-datastore")

def search_knowledge_base(query: str):
    logger.info(f"Searching Knowledge Base for: '{query}'")

    client_options = (
        ClientOptions(api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com")
        if LOCATION != "global"
        else None
    )

    client = discoveryengine.SearchServiceClient(client_options=client_options)

    serving_config = client.serving_config_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATASTORE_ID,
        serving_config="default_config",
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=query,
        page_size=5,
    )

    try:
        response = client.search(request)
        for i, result in enumerate(response.results):
            logger.info(f"Result {i+1}:")
            logger.info(f"Title: {result.document.name}")
            # Snippet could be in document.struct_data depending on schema
            logger.info(f"Data: {result.document.struct_data}")
        return response
    except Exception as e:
        logger.error(f"Search API error: {e}")
        return None

if __name__ == "__main__":
    test_query = "What is Unified System Core?"
    search_knowledge_base(test_query)
