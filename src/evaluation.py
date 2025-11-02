import time
from utils import load_json_data
from search import search_with_ranking

def evaluate_sample_queries():
    print("Loading search engine data...")
    
    crawled_data = load_json_data('crawled_pages.json')
    index_data = load_json_data('inverted_index.json')
    pagerank_scores = load_json_data('pagerank_scores.json')
    link_graph = load_json_data('link_graph.json')
    
    if not all([crawled_data, index_data, pagerank_scores, link_graph]):
        print("Missing data files. Please run the complete pipeline first.")
        return
    
    sample_queries = [
        "deep learning",
        "natural language processing", 
        "computer vision",
        "reinforcement learning",
        "neural networks",
        "machine learning algorithms",
        "artificial intelligence",
        "data science"
    ]
    
    ranking_methods = {
        '1': 'TF-IDF',
        '2': 'TF-IDF + PageRank',
        '3': 'TF-IDF + HITS'
    }
    
    print("=== Query Evaluation Results ===\n")
    
    for query in sample_queries:
        print(f"Query: '{query}'")
        print("-" * 50)
        
        for method_id, method_name in ranking_methods.items():
            start_time = time.time()
            results = search_with_ranking(query, method_id, crawled_data, 
                                        index_data, pagerank_scores, link_graph)
            search_time = time.time() - start_time
            
            print(f"{method_name}:")
            print(f"  Results found: {len(results)}")
            print(f"  Search time: {search_time:.3f}s")
            
            if results:
                top_result = results[0]
                if top_result[0] < len(crawled_data):
                    page = crawled_data[top_result[0]]
                    print(f"  Top result: {page['title']}")
                    print(f"  Score: {top_result[1]:.6f}")
            print()
        
        print("=" * 60)
        print()

def compare_ranking_methods():
    crawled_data = load_json_data('crawled_pages.json')
    index_data = load_json_data('inverted_index.json')
    pagerank_scores = load_json_data('pagerank_scores.json')
    link_graph = load_json_data('link_graph.json')
    
    test_query = "machine learning"
    
    print(f"Detailed comparison for query: '{test_query}'")
    print("=" * 80)
    
    methods = ['1', '2', '3']
    method_names = ['TF-IDF', 'TF-IDF + PageRank', 'TF-IDF + HITS']
    
    all_results = {}
    
    for method_id, method_name in zip(methods, method_names):
        results = search_with_ranking(test_query, method_id, crawled_data,
                                    index_data, pagerank_scores, link_graph)
        all_results[method_name] = results[:5]
        
        print(f"\n{method_name} - Top 5 Results:")
        for i, (doc_id, score) in enumerate(results[:5], 1):
            if doc_id < len(crawled_data):
                page = crawled_data[doc_id]
                print(f"{i}. {page['title'][:60]}...")
                print(f"   Score: {score:.6f}")
                print(f"   URL: {page['url']}")
        print("-" * 80)
    
    print("\nRanking Method Analysis:")
    print("- TF-IDF: Pure content-based ranking, fast computation")
    print("- TF-IDF + PageRank: Incorporates global page authority")
    print("- TF-IDF + HITS: Uses query-specific authority calculation")

if __name__ == "__main__":
    print("Starting query evaluation...")
    evaluate_sample_queries()
    print("\nDetailed method comparison:")
    compare_ranking_methods()