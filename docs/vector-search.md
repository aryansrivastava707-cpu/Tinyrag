# Vector search

Vector search turns text into lists of numbers called embeddings, where texts with similar meaning land close together. A query is embedded the same way, and the closest stored vectors are returned. This finds a passage about "automobile repair" for a question about "fixing a car", even though no words match.

Keyword search, such as BM25, works differently. It scores passages by how many query words they contain, giving more weight to rare words. It is fast, needs no model, and is very good when the question uses the same words as the document.

Many production systems combine both approaches, because keyword search is precise on names and codes while vector search handles paraphrases.
