import unittest

import tinyrag


class TinyRagTest(unittest.TestCase):
    def setUp(self):
        self.idx = tinyrag.build_index("docs")

    def test_finds_right_document(self):
        hit = tinyrag.search(self.idx, "why are documents split into chunks?", 1)[0]
        self.assertEqual(hit["chunk"]["source"], "rag-basics.md")

    def test_keyword_vs_vector_question(self):
        hit = tinyrag.search(self.idx, "how does BM25 keyword search score passages", 1)[0]
        self.assertEqual(hit["chunk"]["source"], "vector-search.md")

    def test_unrelated_question_returns_nothing(self):
        self.assertEqual(tinyrag.search(self.idx, "volcano eruption lava", 3), [])

    def test_chunking_respects_limit(self):
        text = "\n\n".join(["word " * 40] * 5)
        self.assertEqual(len(tinyrag.chunk_text(text, 70)), 5)


if __name__ == "__main__":
    unittest.main()
