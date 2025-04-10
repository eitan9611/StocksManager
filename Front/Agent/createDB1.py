from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect to Qdrant (assuming it's running on localhost)
client = QdrantClient("localhost", port=6333)

# Define a new collection (database) to store vectors
client.recreate_collection(
    collection_name="finance_vectors",
    vectors_config=VectorParams(
        size=4096,  # This depends on the embedding model
        distance=Distance.COSINE  # Use cosine similarity for better retrieval
    ),
)

print("✅ Collection created successfully!")
