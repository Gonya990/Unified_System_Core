import os
import sys
from google import genai
from google.genai.types import Tool, GoogleSearch, GenerateContentConfig

# Setup keys
GEMINI_API_KEY = "AIzaSyCZd986TK8vI-lk7ygpwMV0XgquWIHX7ZU"
PROJECT_ID = "gen-lang-client-0982257437"

def run_vertex_search_poc():
    print("🔍 Starting Vertex AI Search (Grounding) POC...")
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Define Grounding Tool
    # This uses Google Search for grounding. 
    # For Vertex AI Search (Data Stores), we would use different config if available.
    tools = [Tool(google_search=GoogleSearch())]
    
    query = "Is there a public API or developer access for Google Vids (the Workspace video creation app)? Search for Workspace developer documentation or recent announcements."
    
    print(f"❓ Query: {query}")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=query,
            config=GenerateContentConfig(
                tools=tools
            )
        )
        
        print("\n✅ Response:")
        print(response.text)
        
        if response.candidates[0].grounding_metadata:
            print("\n📚 Grounding Metadata found!")
            # print(response.candidates[0].grounding_metadata)
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")

if __name__ == "__main__":
    run_vertex_search_poc()
