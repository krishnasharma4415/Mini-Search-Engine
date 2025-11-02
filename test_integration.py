import unittest
import json
import os
import time
from crawler import crawl_pages, build_link_graph
from indexer import build_inverted_index
from pagerank import calculate_pagerank
from ranker import search_tfidf
from search import search_with_ranking

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.test_data_dir = 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        self.sample_pages = [
            {
                'url': 'http://example.com/ml',
                'title': 'Machine Learning Basics',
                'content': 'Machine learning is a subset of artificial intelligence that focuses on algorithms.',
                'links': ['http://example.com/ai'],
                'crawl_timestamp': '2024-01-01T12:00:00Z'
            },
            {
                'url': 'http://example.com/ai', 
                'title': 'Artificial Intelligence Overview',
                'content': 'Artificial intelligence encompasses machine learning and deep learning techniques.',
                'links': ['http://example.com/dl'],
                'crawl_timestamp': '2024-01-01T12:01:00Z'
            },
            {
                'url': 'http://example.com/dl',
                'title': 'Deep Learning Guide',
                'content': 'Deep learning uses neural networks with multiple layers for complex pattern recognition.',
                'links': ['http://example.com/ml'],
                'crawl_timestamp': '2024-01-01T12:02:00Z'
            }
        ]
    
    def test_end_to_end_pipeline(self):
        with open(f'{self.test_data_dir}/crawled_pages.json', 'w') as f:
            json.dump(self.sample_pages, f)
        
        index_data = build_inverted_index(self.sample_pages)
        self.assertIn('index', index_data)
        self.assertIn('document_frequencies', index_data)
        
        with open(f'{self.test_data_dir}/inverted_index.json', 'w') as f:
            json.dump(index_data, f)
        
        link_graph = build_link_graph(self.sample_pages)
        self.assertIn('nodes', link_graph)
        self.assertIn('edges', link_graph)
        
        with open(f'{self.test_data_dir}/link_graph.json', 'w') as f:
            json.dump(link_graph, f)
        
        pagerank_scores = calculate_pagerank(link_graph)
        self.assertEqual(len(pagerank_scores), 3)
        
        with open(f'{self.test_data_dir}/pagerank_scores.json', 'w') as f:
            json.dump(pagerank_scores, f)
    
    def test_search_performance(self):
        self.test_end_to_end_pipeline()
        
        with open(f'{self.test_data_dir}/inverted_index.json', 'r') as f:
            index_data = json.load(f)
        
        start_time = time.time()
        results = search_tfidf('machine learning', index_data)
        search_time = time.time() - start_time
        
        self.assertLess(search_time, 2.0)
        self.assertGreater(len(results), 0)
    
    def test_error_handling(self):
        try:
            results = search_tfidf('', {})
            self.assertEqual(results, [])
        except Exception as e:
            self.fail(f"Error handling failed: {e}")
        
        try:
            empty_graph = {'nodes': [], 'edges': {}}
            scores = calculate_pagerank(empty_graph)
            self.assertEqual(scores, {})
        except Exception as e:
            self.fail(f"Empty graph handling failed: {e}")
    
    def tearDown(self):
        import shutil
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)

if __name__ == '__main__':
    unittest.main()