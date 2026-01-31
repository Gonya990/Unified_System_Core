import os
import sys

# Add SDK
sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../External_Tools/Stack/agent_mail_sdk/src"))
sys.path.append(sdk_path)

from agent_mail import AgentMailClient


def main():
    os.environ["AGENT_MAIL_SERVER"] = "http://100.126.23.67:8765"
    os.environ["AGENT_MAIL_TOKEN"] = "antigravity_secret"

    # Try different potential project keys
    potential_keys = [
        "/Users/igorgoncharenko/Documents/Unified_System_Core",
        "/home/igorgoncharenko/Documents/Unified_System_Core",
        "/home/gonya/Unified_System",
        "Unified_System_Core",
        "Gonya990/Documents"
    ]

    client = AgentMailClient()

    for key in potential_keys:
        print(f"Checking project: {key}")
        try:
            # We don't have a 'list_projects' so we try to 'ensure' it
            res = client._call_tool("ensure_project", {"human_key": key})
            print(f"✅ Success for {key}: {res}")

            # Now try to Fetch Agents to see if it's the right one
            agents = client._call_tool("list_agents", {"project_key": key})
            print(f"👥 Agents: {agents}")

            # If we find agents, this is likely it!
            if agents.get("structuredContent", {}).get("agents"):
                print(f"🎯 FOUND ACTIVE PROJECT: {key}")
                break

        except Exception as e:
            print(f"❌ Failed for {key}: {e}")

if __name__ == "__main__":
    main()
