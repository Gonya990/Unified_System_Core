import os
from typing import List, Optional

from dotenv import load_dotenv
from google.cloud import discoveryengine_v1beta as discoveryengine

load_dotenv()


class VertexSearchClient:
    """
    Client for interacting with Google Cloud Vertex AI Search (Discovery Engine).
    Provides grounded search capabilities for the Unified System.
    """

    def __init__(self, project_id: Optional[str] = None, location: str = "global", data_store_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "gen-lang-client-0982257437")
        self.location = location
        self.data_store_id = data_store_id or os.getenv("GCP_SEARCH_DATA_STORE_ID")

        if not self.data_store_id:
            print("⚠️ GCP_SEARCH_DATA_STORE_ID is not set. Client will require manual ID passing.")

    def search(self, query: str, data_store_id: Optional[str] = None) -> List[dict]:
        """
        Performs a search query against the specified data store.
        """
        ds_id = data_store_id or self.data_store_id
        if not ds_id:
            raise ValueError("Data Store ID must be provided.")

        client = discoveryengine.SearchServiceClient()

        # Serving config path
        serving_config = client.serving_config_path(
            project=self.project_id,
            location=self.location,
            data_store=ds_id,
            serving_config="default_config",
        )

        request = discoveryengine.SearchRequest(
            serving_config=serving_config,
            query=query,
            page_size=5,
        )

        response = client.search(request)

        results = []
        for result in response.results:
            doc = result.document
            results.append(
                {
                    "id": doc.id,
                    "title": doc.derived_struct_data.get("title", "No Title"),
                    "snippet": doc.derived_struct_data.get("snippets", [{}])[0].get("snippet", ""),
                    "link": doc.derived_struct_data.get("link", ""),
                }
            )

        return results


if __name__ == "__main__":
    # POC Test
    test_query = "Who is Arthur?"
    print(f"🔍 Testing Vertex AI Search for: {test_query}")
    try:
        client = VertexSearchClient()
        # For POC, we assume the user provides a data store ID in env or here
        # search_results = client.search(test_query)
        # print(search_results)
        print("✅ Client structure initialized. (Actual search requires Data Store ID)")
    except Exception as e:
        print(f"❌ Search failed: {e}")
