# MongoDB Atlas Vector Search (optional)

TinyRAG's BM25 CLI works offline with only Python's standard library. This
adapter adds an optional Atlas Vector Search path when your application already
has query and passage embeddings.

## Setup

1. Create an Atlas cluster and a collection named `passages`.
2. Install the optional client: `pip install -r requirements-mongo.txt`.
3. Create a Vector Search index named `passage_vector` with a vector field named
   `embedding`. Set `numDimensions` to the dimension produced by your embedding
   model and use cosine similarity.
4. Set `MONGODB_URI` in your local environment. Do not commit credentials.

## Use from Python

```python
import os
from vector_search import AtlasVectorStore

store = AtlasVectorStore.from_uri(
    os.environ["MONGODB_URI"], "tinyrag", "passages", "passage_vector"
)
store.upsert("notes-1", "BM25 is a lexical ranker.", "notes.md", passage_vector)
hits = store.search(query_vector, limit=5)
```

The caller supplies `passage_vector` and `query_vector`; this adapter does not
create embeddings. The supplied vectors must match the index dimension. MongoDB
integration tests use a fake collection and do not require Atlas credentials.
