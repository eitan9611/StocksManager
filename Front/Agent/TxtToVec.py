import requests
import numpy as np

# Function to get embeddings from Mistral and return JSON
def get_embedding(text):
    response = requests.post(
        "http://ollama:11434/api/embeddings",  # Changed from localhost to ollama
        json={"model": "mistral", "prompt": text}
    )
    try:
        response_json = response.json()
        # Extract the embedding array from the response
        embedding = response_json["embedding"]
        return {"text": text, "embedding": embedding}  # Return JSON with embedding array
    except KeyError as e:
        print(f"Error: Unexpected response format: {e}")
        print(f"Response: {response.json()}")
        return None