
import os
import sys

# Add the current directory to sys.path to allow importing agent_mail_client
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_mail_client import AgentMailClient

def main():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    client = AgentMailClient()
    project_key = client.config.project_key
    
    print(f"Listing tools on server {client.config.server}")
    # Remove Authorization header since auth is disabled on server and might be causing issues
    client.session.headers.pop("Authorization", None)
    
    payload = {
        'jsonrpc': '2.0',
        'method': 'tools/list',
        'id': 1
    }
    
    try:
        response = client.session.post(f'{client.config.server}/mcp', json=payload)
        response.raise_for_status()
        result = response.json()
        
        tools = result.get('result', {}).get('tools', [])
        tool_names = [t['name'] for t in tools]
        
        print(f"Total tools: {len(tool_names)}")
        if 'ensure_project' in tool_names:
            print("Tool 'ensure_project' FOUND.")
            # If found, try calling it again purely without header (already popped)
            # Maybe the 403 was transient or due to header previously?
            # Or maybe we can't call it via the same user session if it failed once?
            
            # Re-attempt call
            print("Attempting to call 'ensure_project' again...")
            call_payload = {
                'jsonrpc': '2.0',
                'method': 'tools/call',
                'params': {
                    'name': 'ensure_project',
                    'arguments': {'human_key': project_key}
                },
                'id': 2
            }
            call_resp = client.session.post(f'{client.config.server}/mcp', json=call_payload)
            print(f"Call Status: {call_resp.status_code}")
            print(f"Call Body: {call_resp.text}")
        else:
            print("Tool 'ensure_project' NOT FOUND in list.")
            print("Available tools:", tool_names)

    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    main()
