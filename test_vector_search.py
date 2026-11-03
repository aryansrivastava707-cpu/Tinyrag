import unittest
from vector_search import AtlasVectorStore

class FakeCollection:
    def __init__(self): self.records={}; self.pipeline=None
    def replace_one(self, query, record, upsert=False): self.records[query['_id']]=record
    def aggregate(self, pipeline): self.pipeline=pipeline; return [{'text':'note','source':'notes.md','score':0.91}]

class AtlasVectorStoreTest(unittest.TestCase):
    def setUp(self): self.collection=FakeCollection(); self.store=AtlasVectorStore(self.collection)
    def test_upsert_normalizes_vector_and_replaces_by_id(self):
        self.assertEqual(self.store.upsert('a','hello','x.md',[1,2]),'a')
        self.assertEqual(self.collection.records['a']['embedding'],[1.0,2.0])
    def test_search_uses_configured_atlas_vector_pipeline(self):
        hits=self.store.search([0.25,0.75],limit=2)
        stage=self.collection.pipeline[0]['$vectorSearch']
        self.assertEqual((stage['index'],stage['path'],stage['limit']),('passage_vector','embedding',2))
        self.assertEqual(hits[0]['source'],'notes.md')
    def test_rejects_bad_vectors_and_limits(self):
        for vector in ([],[float('nan')],[True]):
            with self.assertRaises(ValueError): self.store.search(vector)
        with self.assertRaises(ValueError): self.store.search([1],limit=101)
    def test_requires_mongo_uri(self):
        with self.assertRaises(ValueError): AtlasVectorStore.from_uri('', 'db','docs')

if __name__=='__main__': unittest.main()
