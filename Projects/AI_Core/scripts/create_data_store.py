import os

from dotenv import load_dotenv
from google.api_core import exceptions
from google.cloud import discoveryengine_v1beta as discoveryengine

load_dotenv()


def create_data_store():
    project_id = "gen-lang-client-0982257437"
    location = "global"
    data_store_id = "gonya90-knowledge-store"

    # Set quota project
    os.environ["GOOGLE_CLOUD_QUOTA_PROJECT"] = project_id

    print(f"🚀 Initializing Data Store creation: {data_store_id}")

    client = discoveryengine.DataStoreServiceClient()

    # Parent for collection
    parent = f"projects/{project_id}/locations/{location}/collections/default_collection"

    # Define Data Store
    # For Pub/Sub ingestion, we use 'unstructured' or similar depending on needs,
    # but primarily we want to link the ingestion source.
    # Note: LRO (Long Running Operation) might be involved.

    ds = discoveryengine.DataStore(
        display_name="Gonya90 Knowledge Store",
        industry_vertical=discoveryengine.IndustryVertical.GENERIC,
        solution_types=[discoveryengine.SolutionType.SOLUTION_TYPE_SEARCH],
        content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
    )

    try:
        operation = client.create_data_store(parent=parent, data_store=ds, data_store_id=data_store_id)
        print(f"⌛ Creation operation started: {operation.operation.name}")
        result = operation.result()
        print(f"✅ Data Store created: {result.name}")

    except exceptions.AlreadyExists:
        print(f"ℹ️ Data Store {data_store_id} already exists.")
    except Exception as e:
        print(f"❌ Failed to create Data Store: {e}")
        return None

    # Step 2: Configure Pub/Sub Ingestion (this often requires IngestionConfig/Source)
    # However, create_data_store might not link it directly in one call.
    # We might need to use 'import_documents' with Pub/Sub source later if not in initial config.
    return data_store_id


if __name__ == "__main__":
    create_data_store()
