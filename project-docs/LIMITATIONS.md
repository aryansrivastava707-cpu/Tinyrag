# Limitations and safe use

This project implements retrieval only. It does not call an LLM or generate answers. Tokenization and stemming are intentionally simple; BM25 is lexical and may miss semantic matches. The JSON index should be rebuilt after source documents change.

Use synthetic or authorized data when exploring this project. Review output
before sharing it; reports may include repository paths, source snippets, or
request metadata from the input.
