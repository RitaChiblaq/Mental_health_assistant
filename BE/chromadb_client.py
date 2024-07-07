import requests


class ChromaDBClient:
    def __init__(self, base_url):
        """
        Initialize the ChromaDBClient with the base URL for the ChromaDB API.

        :param base_url: The base URL for the ChromaDB API.
        """
        self.base_url = base_url

    def store_message_embedding(self, message_id, user_id, embedding):
        """
        Store the embedding of a message in the ChromaDB.

        :param message_id: The unique identifier for the message.
        :param user_id: The unique identifier for the user.
        :param embedding: The embedding data for the message.
        :raises Exception: If the request to store the embedding fails.
        """
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
        """
        Store the embedding of a coping strategy in the ChromaDB.

        :param strategy_id: The unique identifier for the coping strategy.
        :param embedding: The embedding data for the coping strategy.
        :raises Exception: If the request to store the embedding fails.
        """
        url = f"{self.base_url}/store_strategy_embedding"
        data = {
            "strategy_id": strategy_id,
            "embedding": embedding
        }
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise Exception(f"Failed to store strategy embedding: {response.text}")