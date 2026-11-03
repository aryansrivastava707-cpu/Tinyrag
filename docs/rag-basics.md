# Retrieval-augmented generation

A language model only knows what was in its training data. Retrieval-augmented generation, usually shortened to RAG, adds a lookup step before the model answers. The system first finds passages related to the question, then hands those passages to the model as context.

Documents are split into chunks before they are indexed. Chunks that are too large bury the useful sentence in noise, and chunks that are too small lose the surrounding meaning. A few hundred words with sensible paragraph boundaries is a common starting point.

Retrieval quality limits answer quality. If the right passage is not retrieved, the model cannot use it, no matter how strong the model is. Teams therefore measure retrieval separately, for example by checking whether the correct source appears in the top three results.
