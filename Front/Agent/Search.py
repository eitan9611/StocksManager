import requests
from qdrant_client import QdrantClient
from qdrant_client.models import SearchParams
import TxtToVec
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Connect to the existing Qdrant database
# When running in Docker, we need to use the service name instead of localhost
qdrant = QdrantClient("qdrant", port=6333)  # Changed from localhost to qdrant


# Function to search for relevant knowledge in Qdrant
def search_knowledge(query):
    response = TxtToVec.get_embedding(query)
    if not response:
        return "Error getting embeddings for your query."

    query_vector = response["embedding"]  # This should now be a list of floats

    search_results = qdrant.search(
        collection_name="finance_vectors",
        query_vector=query_vector,
        limit=3,  # Get top 3 most relevant results
        search_params=SearchParams(hnsw_ef=128, exact=False),  # Improve search efficiency
    )

    retrieved_texts = [hit.payload["text"] for hit in search_results if hit.payload]

    if not retrieved_texts:
        return "I couldn't find any relevant information."

    print(f"🔍 Found related texts: {retrieved_texts}")
    return "\n".join(retrieved_texts)


# Function to ask Ollama with retrieved knowledge
def ask_agent(question):
    context = search_knowledge(question)  # Retrieve relevant knowledge
    print(f"🔍 Context for question: {context}")

    if not ensure_model_exists("mistral"):
        raise Exception("Failed to pull required model")

    payload = {
        "model": "mistral",
        "prompt": f"Using this financial knowledge:\n{context}\n\nAnswer the following question IN NO MORE THEN 3 LINES:\n{question}",
        "stream": False
    }

    # When running in Docker, use the service name instead of localhost
    response = requests.post("http://ollama:11434/api/generate", json=payload)
    return response.json().get("response", "Error: No response found")


def ensure_model_exists(model_name="mistral"):
    # Check if model exists
    response = requests.post("http://ollama:11434/api/generate",
                             json={"model": model_name, "prompt": "", "stream": False})

    if response.status_code != 200:
        # Model doesn't exist, pull it
        print(f"Pulling model {model_name}...")
        pull_response = requests.post("http://ollama:11434/api/pull",
                                      json={"name": model_name})
        return pull_response.ok
    return True


# Add an API endpoint to handle /ask
@app.route('/ask', methods=['POST'])
def handle_ask():
    print("Received request at /ask")
    data = request.json
    question = data.get('question')
    print(f"Received question: {question}")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = ask_agent(question)
    return jsonify({"response": response})


# Run the Flask app if this file is executed directly
if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, host="0.0.0.0", port=5000)



