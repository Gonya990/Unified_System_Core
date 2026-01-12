
import requests


class AIOSClient:
    def __init__(self, host="100.110.209.49", port=8000):
        self.base_url = f"http://{host}:{port}"

    def get_status(self):
        try:
            response = requests.get(f"{self.base_url}/status")
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def query(self, agent_name, query_type, query_data):
        """
        query_type: "llm", "tool", "storage", "memory"
        query_data: dictionary containing parameters for the specific query type
        """
        payload = {
            "agent_name": agent_name,
            "query_type": query_type,
            "query_data": query_data
        }
        try:
            response = requests.post(f"{self.base_url}/query", json=payload)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def select_llms(self, llms_list):
        """
        llms_list: list of dicts with {"name": ..., "provider": ...}
        """
        try:
            response = requests.post(f"{self.base_url}/user/select/llms", json=llms_list)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    client = AIOSClient()
    print("AIOS Status:", client.get_status())

    # Example selection
    # print(client.select_llms([{"name": "gemini-2.0-flash-exp", "provider": "gemini"}]))

    # Example query
    # print(client.query("test_agent", "llm", {
    #     "messages": [{"role": "user", "content": "Hello AIOS!"}],
    #     "llms": [{"name": "gemini-2.0-flash-exp", "provider": "gemini"}]
    # }))
