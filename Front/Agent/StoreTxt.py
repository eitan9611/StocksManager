import requests
import uuid
import re
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import TxtToVec

# ✅ Connect to the existing Qdrant database
qdrant = QdrantClient("localhost", port=6333)

# ✅ Function to split long text into smaller chunks
def split_text(text, chunk_size=200):
    """Splits text into smaller chunks of max chunk_size characters."""
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split by sentences
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# ✅ Function to store text in Qdrant
def store_text(text, chunk_size=200):
    chunks = split_text(text, chunk_size)  # Split long text into chunks
    print("IM THE ARTICLE TEXT:")
    print(chunks)

    for chunk in chunks:
        if chunk:
            vector_data = TxtToVec.get_embedding(chunk)  # Convert chunk to vector
            vector = vector_data["embedding"]

            if isinstance(vector, list) and all(isinstance(i, float) for i in vector):
                point_id = str(uuid.uuid4())  # Generate unique ID for each chunk
                qdrant.upsert(
                    collection_name="finance_vectors",
                    points=[PointStruct(id=point_id, vector=vector, payload={"text": chunk})]
                )
                print(f"✅ Stored: {chunk[:30]}... with ID {point_id}")
            else:
                print("❌ Error: The vector format is incorrect.")

# 🔥 Example: Store a long finance-related text
#long_text = """Stock market volatility measures how much stock prices fluctuate over time.
#High volatility means large price swings, while low volatility indicates stable prices.
#Investors monitor volatility to assess risk and potential returns. Market events, economic
#news, and investor sentiment all influence volatility levels. Strategies like diversification
#and options trading help manage volatility risks."""

#store_text(long_text)
