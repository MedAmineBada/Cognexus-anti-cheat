import time

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from config import env

# Qdrant connection settings
QDRANT_HOST = env.QDRANT_HOST
QDRANT_PORT = env.QDRANT_PORT

# Vector settings
VECTOR_SIZE = env.VECTOR_SIZE
SIMILARITY_DISTANCE = Distance.COSINE

# Search settings
SIMILARITY_THRESHOLD = env.SIMILARITY_THRESHOLD

# Global client instance
vdb = None


def connect_qdrant():
    """Connect to Qdrant server with retry logic"""
    global vdb

    print("Connecting to Qdrant...")

    max_attempts = 30  # 1 minute / 2 seconds = 30 attempts
    attempt = 0

    while attempt < max_attempts:
        try:
            vdb = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            vdb.get_collections()
            print("Connected to Qdrant successfully")
            return vdb

        except Exception as e:
            attempt += 1
            print(f"Connection attempt {attempt}/{max_attempts} failed: {e}")

            if attempt >= max_attempts:
                print(f"Failed to connect to Qdrant after {max_attempts} attempts")
                raise ConnectionError(
                    f"Could not connect to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}"
                )

            print("Retrying in 2 seconds...")
            time.sleep(2)


def disconnect_qdrant():
    """Disconnect from Qdrant server"""
    global vdb
    if vdb:
        print("Disconnecting from Qdrant...")
        vdb.close()
        vdb = None
        print("Qdrant disconnected")


def get_qdrant_client():
    """Get the Qdrant client instance"""
    if vdb is None:
        raise RuntimeError(
            "Qdrant client not initialized. Call connect_qdrant() first."
        )
    return vdb


def ensure_collection(exam_id: str, question_id: str) -> str:
    client = get_qdrant_client()
    collection_name = f"{exam_id}_Q{question_id}"

    existing = [c.name for c in client.get_collections().collections]

    if collection_name not in existing:
        print(f"Creating collection {collection_name}...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=SIMILARITY_DISTANCE),
        )
        print(f"Collection {collection_name} created")

    return collection_name
