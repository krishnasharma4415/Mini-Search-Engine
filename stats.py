from utils import load_json_data

def generate_statistics():
    crawled_data = load_json_data('data/crawled_pages.json')
    index_data = load_json_data('data/inverted_index.json')
    link_graph = load_json_data('data/link_graph.json')
    
    if not all([crawled_data, index_data, link_graph]):
        print("Missing data files. Run crawler.py and indexer.py first.")
        return
    
    total_pages = len(crawled_data)
    unique_terms = len(index_data['index'])
    
    total_links = sum(len(links) for links in link_graph['edges'].values())
    avg_links_per_page = total_links / total_pages if total_pages > 0 else 0
    
    print("=== Search Engine Statistics ===")
    print(f"Total pages crawled: {total_pages}")
    print(f"Unique terms in index: {unique_terms}")
    print(f"Total outgoing links: {total_links}")
    print(f"Average links per page: {avg_links_per_page:.2f}")
    
    print(f"\nTop 10 most frequent terms:")
    term_frequencies = {}
    for term, postings in index_data['index'].items():
        total_tf = sum(doc_info['tf'] for doc_info in postings.values())
        term_frequencies[term] = total_tf
    
    top_terms = sorted(term_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (term, freq) in enumerate(top_terms, 1):
        print(f"{i}. {term}: {freq}")

if __name__ == "__main__":
    generate_statistics()