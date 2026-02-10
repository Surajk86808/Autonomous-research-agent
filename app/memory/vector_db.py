from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from sentence_transformers import SentenceTransformer


# ✅ Initialize embedding model FIRST (faster startup pattern)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    return embedding_model.encode(text).tolist()


# ✅ Persistent Local DB (not in-memory)
client = QdrantClient(path="./qdrant_data")

COLLECTION = "research_memory"


# ✅ Create collection ONLY if missing (VERY IMPORTANT)
if not client.collection_exists(COLLECTION):

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(
            size=384,     # MUST match all-MiniLM-L6-v2
            distance=Distance.COSINE
        )
    )


# ✅ Store memory
def store_memory(text: str):

    embedding = get_embedding(text)

    client.upsert(
        collection_name=COLLECTION,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": text}
            )
        ]
    )


# ✅ Retrieve memories
def get_memories(query: str, limit=3):

    query_vector = get_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,   # correct param for v1.16+
        limit=limit
    )

    return [point.payload["text"] for point in results.points]
