import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ranker import compute_tf, compute_idf, calculate_tfidf_scores
from pagerank import build_adjacency_matrix, handle_dangling_nodes, calculate_pagerank
from hits import extract_query_subgraph, calculate_hits
from indexer import preprocess_text

class TestTFIDF(unittest.TestCase):
    
    def setUp(self):
        self.sample_index = {
            'machine': {
                '0': {'tf': 3, 'url': 'url1', 'title': 'title1'},
                '1': {'tf': 1, 'url': 'url2', 'title': 'title2'}
            },
            'learning': {
                '0': {'tf': 2, 'url': 'url1', 'title': 'title1'}
            }
        }
        self.sample_index_data = {
            'index': self.sample_index,
            'document_frequencies': {'machine': 2, 'learning': 1},
            'total_documents': 2
        }
    
    def test_compute_tf(self):
        tf = compute_tf('machine', '0', self.sample_index)
        self.assertEqual(tf, 3)
        
        tf_missing = compute_tf('missing', '0', self.sample_index)
        self.assertEqual(tf_missing, 0)
    
    def test_compute_idf(self):
        idf = compute_idf('machine', {'machine': 2}, 2)
        expected_idf = np.log(2 / 2)
        self.assertAlmostEqual(idf, expected_idf, places=5)
    
    def test_calculate_tfidf_scores(self):
        scores = calculate_tfidf_scores(['machine'], self.sample_index_data)
        self.assertIn(0, scores)
        self.assertIn(1, scores)
        self.assertGreater(scores[0], scores[1])

class TestPageRank(unittest.TestCase):
    
    def setUp(self):
        self.sample_graph = {
            'nodes': ['A', 'B', 'C'],
            'edges': {
                'A': ['B'],
                'B': ['C'],
                'C': ['A']
            }
        }
    
    def test_build_adjacency_matrix(self):
        matrix, url_to_index = build_adjacency_matrix(self.sample_graph)
        self.assertEqual(matrix.shape, (3, 3))
        self.assertEqual(len(url_to_index), 3)
    
    def test_handle_dangling_nodes(self):
        matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
        normalized = handle_dangling_nodes(matrix)
        
        for col in range(3):
            self.assertAlmostEqual(np.sum(normalized[:, col]), 1.0, places=5)
    
    def test_calculate_pagerank(self):
        scores = calculate_pagerank(self.sample_graph, max_iterations=10)
        self.assertEqual(len(scores), 3)
        
        total_score = sum(scores.values())
        self.assertAlmostEqual(total_score, 1.0, places=3)

class TestHITS(unittest.TestCase):
    
    def setUp(self):
        self.sample_graph = {
            'nodes': ['A', 'B', 'C'],
            'edges': {
                'A': ['B', 'C'],
                'B': ['C'],
                'C': []
            }
        }
        self.sample_index = {
            'index': {
                'test': {
                    '0': {'tf': 1, 'url': 'A', 'title': 'Page A'},
                    '1': {'tf': 1, 'url': 'B', 'title': 'Page B'}
                }
            }
        }
    
    def test_extract_query_subgraph(self):
        subgraph = extract_query_subgraph(['test'], self.sample_graph, self.sample_index)
        self.assertIn('A', subgraph['nodes'])
        self.assertIn('B', subgraph['nodes'])
    
    def test_calculate_hits(self):
        hub_scores, auth_scores = calculate_hits(['test'], self.sample_graph, self.sample_index)
        self.assertIsInstance(hub_scores, dict)
        self.assertIsInstance(auth_scores, dict)

class TestPreprocessing(unittest.TestCase):
    
    def test_preprocess_text(self):
        text = "Machine Learning is Amazing!"
        tokens = preprocess_text(text)
        
        self.assertIn('machin', tokens)
        self.assertIn('learn', tokens)
        self.assertIn('amaz', tokens)
        self.assertNotIn('is', tokens)

if __name__ == '__main__':
    unittest.main()