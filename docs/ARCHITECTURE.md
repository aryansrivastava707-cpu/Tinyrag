# Architecture

`tinyrag.py` implements local BM25 retrieval over Markdown and text. `vector_search.py` provides an optional PyMongo adapter for MongoDB Atlas Vector Search. Callers supply embeddings; the adapter validates them, upserts passages, and builds an Atlas `$vectorSearch` aggregation.

## Local path

```bash
python tinyrag.py index docs/
python tinyrag.py ask "how does BM25 rank passages?" -k 3
```

## Optional vector path

See [MongoDB Vector Search setup](MONGODB_VECTOR_SEARCH.md). Atlas credentials and a matching vector index are required for a live search.
