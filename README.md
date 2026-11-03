# TinyRAG

> Local BM25 retrieval with an optional MongoDB Atlas Vector Search adapter.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas%20Vector%20Search-47a248.svg?logo=mongodb)](https://www.mongodb.com/atlas)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Optional MongoDB Setup](#-optional-mongodb-setup)
- [Tests](#-tests)
- [Limitations](#-limitations)
- [License](#-license)

## 🎯 Overview

TinyRAG ranks passages from local notes. The default BM25 path is dependency-free; an optional adapter sends existing embeddings to MongoDB Atlas Vector Search.

## ✨ Features

- Chunk Markdown and text files and build a local BM25 index
- Show source passages and matched query terms
- Upsert precomputed vectors and query an Atlas Vector Search index
- Keep the local lexical workflow independent from MongoDB credentials

## 🧱 Architecture

`tinyrag.py` implements lexical retrieval. `vector_search.py` is an optional PyMongo adapter that accepts vectors from an embedding model and issues an Atlas `$vectorSearch` aggregation. It does not create embeddings.

See [BM25 method](docs/ALGORITHM.md), [Atlas setup and use](docs/MONGODB_VECTOR_SEARCH.md), and [input/output notes](docs/INPUTS_AND_OUTPUTS.md).

## 🚀 Quick Start

Requires Python 3.10+. From this folder:

```bash
python -m unittest -v
python tinyrag.py index docs/
python tinyrag.py ask "how does BM25 rank passages?" -k 3
```

The generated `index.json` is local and ignored by Git.

## 🧭 Optional MongoDB Setup

For Atlas Vector Search, install `pip install -r requirements-mongo.txt`, configure an Atlas vector index, and provide precomputed query/passage vectors. See [MongoDB Vector Search](docs/MONGODB_VECTOR_SEARCH.md). The BM25 commands above do not require MongoDB.

## ✅ Tests

`python -m unittest -v` runs the BM25 tests and fake-collection tests for vector pipeline construction. No MongoDB account is needed for tests.

## ⚠️ Limitations

BM25 uses simple tokenization and may miss semantic matches. Atlas search requires an existing vector index whose dimensions and similarity settings match your embedding model; embeddings and Atlas credentials are supplied by the caller.

## 📄 License

MIT. See [LICENSE](LICENSE).
