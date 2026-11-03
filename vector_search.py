"""Optional MongoDB Atlas Vector Search adapter for TinyRAG.

The BM25 CLI remains usable without MongoDB. Pass precomputed vectors to this
adapter when you have an embeddings model and an Atlas vector index configured.
"""
import math


class AtlasVectorStore:
    def __init__(self, collection, index_name="passage_vector", vector_path="embedding"):
        if not index_name or not vector_path:
            raise ValueError("index_name and vector_path are required")
        self.collection = collection
        self.index_name = index_name
        self.vector_path = vector_path

    @classmethod
    def from_uri(cls, uri, database, collection, index_name="passage_vector", vector_path="embedding"):
        if not uri:
            raise ValueError("MongoDB URI is required")
        try:
            from pymongo import MongoClient
        except ImportError as exc:
            raise RuntimeError("Install the optional dependency: pip install -r requirements-mongo.txt") from exc
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        return cls(client[database][collection], index_name, vector_path)

    @staticmethod
    def _validate_vector(vector):
        if not isinstance(vector, (list, tuple)) or not vector:
            raise ValueError("embedding must be a non-empty numeric vector")
        normalized = []
        for value in vector:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError("embedding values must be finite numbers")
            normalized.append(float(value))
        return normalized

    def upsert(self, document_id, text, source, embedding):
        if not document_id or not isinstance(text, str) or not text.strip():
            raise ValueError("document_id and non-empty text are required")
        record = {"_id": str(document_id), "text": text, "source": str(source),
                  "embedding": self._validate_vector(embedding)}
        self.collection.replace_one({"_id": record["_id"]}, record, upsert=True)
        return record["_id"]

    def search(self, query_vector, limit=5, candidates=None):
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        vector = self._validate_vector(query_vector)
        num_candidates = candidates or max(100, limit * 20)
        if num_candidates < limit:
            raise ValueError("candidates must be greater than or equal to limit")
        pipeline = [
            {"$vectorSearch": {
                "index": self.index_name,
                "path": self.vector_path,
                "queryVector": vector,
                "numCandidates": num_candidates,
                "limit": limit,
            }},
            {"$project": {"_id": 0, "text": 1, "source": 1,
                          "score": {"$meta": "vectorSearchScore"}}},
        ]
        return list(self.collection.aggregate(pipeline))
