import time
from utils import load_json_data
from ranker import search_tfidf, process_query
from hits import calculate_hits

def main_search_loop():
    print("Loading search engine data...")
    
    crawled_data = load_json_data('data/crawled_pages.json')
    index_data = load_json_data('data/inverted_index.json')
    pagerank_scores = load_json_data('data/pagerank_scores.json')
    link_graph = load_json_data('data/link_graph.json')
    
    if not all([crawled_data, index_data, pagerank_scores, link_graph]):
        print("Missing data files. Please run:")
        print("1. python crawler.py")
        print("2. python indexer.py") 
        print("3. python pagerank.py")
        return
    
    print("Search engine ready!")
    print("\nRanking options:")
    print("1. TF-IDF only")
    print("2. TF-IDF + PageRank")
    print("3. TF-IDF + HITS Authority")
    
    while True:
        print("\n" + "="*50)
        query = input("Enter search query (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
        
        ranking_mode = input("Select ranking mode (1-3): ").strip()
        if ranking_mode not in ['1', '2', '3']:
            print("Invalid ranking mode. Using TF-IDF only.")
            ranking_mode = '1'
        
        start_time = time.time()
        results = search_with_ranking(query, ranking_mode, crawled_data, index_data, 
                                    pagerank_scores, link_graph)
        search_time = time.time() - start_time
        
        display_results(results, query, ranking_mode, search_time)

def process_query(query_text):
    from indexer import preprocess_text
    return preprocess_text(query_text)

def search_with_ranking(query, ranking_mode, crawled_data, index_data, pagerank_scores, link_graph):
    query_terms = process_query(query)
    if not query_terms:
        return []
    
    tfidf_results = search_tfidf(query, index_data)
    
    if ranking_mode == '1':
        return tfidf_results[:10]
    
    elif ranking_mode == '2':
        return combine_tfidf_pagerank(tfidf_results, pagerank_scores, crawled_data)
    
    elif ranking_mode == '3':
        return combine_tfidf_hits(query_terms, tfidf_results, link_graph, index_data, crawled_data)
    
    return tfidf_results[:10]def
 combine_tfidf_pagerank(tfidf_results, pagerank_scores, crawled_data):
    combined_scores = []
    
    for doc_id, tfidf_score in tfidf_results:
        if doc_id < len(crawled_data):
            url = crawled_data[doc_id]['url']
            pagerank_score = pagerank_scores.get(url, 0)
            
            combined_score = 0.6 * tfidf_score + 0.4 * pagerank_score
            combined_scores.append((doc_id, combined_score))
    
    return sorted(combined_scores, key=lambda x: x[1], reverse=True)[:10]

def combine_tfidf_hits(query_terms, tfidf_results, link_graph, index_data, crawled_data):
    hub_scores, auth_scores = calculate_hits(query_terms, link_graph, index_data)
    
    combined_scores = []
    
    for doc_id, tfidf_score in tfidf_results:
        if doc_id < len(crawled_data):
            url = crawled_data[doc_id]['url']
            authority_score = auth_scores.get(url, 0)
            
            combined_score = 0.6 * tfidf_score + 0.4 * authority_score
            combined_scores.append((doc_id, combined_score))
    
    return sorted(combined_scores, key=lambda x: x[1], reverse=True)[:10]

def format_results(results, crawled_data):
    formatted = []
    
    for doc_id, score in results:
        if doc_id < len(crawled_data):
            page = crawled_data[doc_id]
            snippet = page['content'][:200] + "..." if len(page['content']) > 200 else page['content']
            
            formatted.append({
                'title': page['title'],
                'url': page['url'],
                'snippet': snippet,
                'score': score
            })
    
    return formatted

def display_results(results, query, ranking_mode, search_time):
    ranking_names = {
        '1': 'TF-IDF',
        '2': 'TF-IDF + PageRank', 
        '3': 'TF-IDF + HITS Authority'
    }
    
    print(f"\nResults for '{query}' using {ranking_names[ranking_mode]}")
    print(f"Search completed in {search_time:.3f} seconds")
    print("-" * 80)
    
    if not results:
        print("No results found.")
        return
    
    crawled_data = load_json_data('data/crawled_pages.json')
    formatted_results = format_results(results, crawled_data)
    
    for i, result in enumerate(formatted_results, 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Score: {result['score']:.6f}")
        print(f"   Snippet: {result['snippet']}")
        print()

if __name__ == "__main__":
    main_search_loop()d
ef show_statistics():
    from stats import generate_statistics
    generate_statistics()