# TinyRAG

> A dependency-free retrieval demo that ranks passages from your notes with BM25.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library-green.svg)](requirements.txt)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Tests](#-tests)
- [Limitations](#-limitations)
- [License](#-license)

## 🎯 Overview

A dependency-free retrieval demo that ranks passages from your notes with BM25. This project focuses on Python, information retrieval, and RAG fundamentals.

## ✨ Features

- Index Markdown and text files as passages
- Rank passages with a transparent BM25 implementation
- Show source names, matching terms, and relevant text
- Rebuild a local index when your notes change

## 🧱 Architecture

The CLI chunks local notes, records term statistics, and ranks matching passages with BM25. It returns retrieved evidence only; there is no language-model call or answer generation.

See the [architecture notes](project-docs/ARCHITECTURE.md), [algorithm details](docs/ALGORITHM.md),
[development guide](project-docs/DEVELOPMENT.md), and [input/output notes](docs/INPUTS_AND_OUTPUTS.md).

## 🚀 Quick Start

Requires Python 3.10 or newer. No third-party packages are required. From this
project folder, run the tests: 

```bash
python -m unittest -v
```

## 🧪 Usage

```bash
python tinyrag.py index docs/
python tinyrag.py ask "how does BM25 rank passages?" -k 3
```

## ✅ Tests

Run `python -m unittest -v` from this folder. Tests use the bundled sample notes and check retrieval, chunking, and unrelated queries.

## ⚠️ Limitations

Tokenization and stemming are intentionally simple. BM25 is lexical and may miss semantic matches. The generated `index.json` is local and should be rebuilt when source documents change.

More detail: [limitations and safe use](project-docs/LIMITATIONS.md).

## 📄 License

MIT. See [LICENSE](LICENSE).
