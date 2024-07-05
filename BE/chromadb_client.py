import requests


class ChromaDBClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def store_message_embedding(self, message_id, user_id, embedding):
        url = f"{self.base_url}/store_message_embedding"
        data = {
            "message_id": message_id,
            "user_id": user_id,
            "embedding": embedding
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to store message embedding: {response.text}")

    def store_strategy_embedding(self, strategy_id, embedding):
        url = f"{self.base_url}/store_strategy_embedding"
        data = {
            "strategy_id": strategy_id,
            "embedding": embedding
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to store strategy embedding: {response.text}")
