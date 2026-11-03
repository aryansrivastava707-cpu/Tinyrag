# Retrieval method

Markdown and text files are split at paragraph boundaries. A small tokenizer
normalizes terms and removes a short stop-word list. The index stores term
frequencies, document frequencies, and passage lengths. Queries are ranked with
BM25; the implementation returns evidence passages and matching terms without
calling a language model or generating an answer.
