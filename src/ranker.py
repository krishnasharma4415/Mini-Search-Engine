import math
from collections import defaultdict
from utils import load_json_data
from indexer import preprocess_text

def compute_tf(term, doc_id, index):
    if term in index and doc_id in index[term]:
        return index[term][doc_id]['tf']
    return 0

def compute_idf(term, document_frequencies, total_docs):
    if term in document_frequencies:
        df = document_frequencies[term]
        return math.log(total_docs / df)
    return 0

def calculate_tfidf_scores(query_terms, index_data):
    index = index_data['index']
    document_frequencies = index_data['document_frequencies']
    total_docs = index_data['total_documents']
    
    doc_scores = defaultdict(float)
    
    for term in query_terms:
        if term in index:
            idf = compute_idf(term, document_frequencies, total_docs)
            
            for doc_id, doc_info in index[term].items():
                tf = doc_info['tf']
                tfidf_score = tf * idf
                doc_scores[int(doc_id)] += tfidf_score
    
    return dict(doc_scores)
    
def rank_documents(scores):
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def process_query(query_text):
    return preprocess_text(query_text)

def search_tfidf(query_text, index_data):
    query_terms = process_query(query_text)
    if not query_terms:
        return []
    
    scores = calculate_tfidf_scores(query_terms, index_data)
    return rank_documents(scores)

def main():
    index_data = load_json_data('inverted_index.json')
    if not index_data:
        print("No index found. Run src/indexer.py first.")
        return
    
    while True:
        query = input("\nEnter search query (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
        
        results = search_tfidf(query, index_data)
        
        print(f"\nTop 10 results for '{query}':")
        for i, (doc_id, score) in enumerate(results[:10], 1):
            doc_info = None
            for term in process_query(query):
                if term in index_data['index'] and str(doc_id) in index_data['index'][term]:
                    doc_info = index_data['index'][term][str(doc_id)]
                    break
            
            if doc_info:
                print(f"{i}. {doc_info['title']}")
                print(f"   URL: {doc_info['url']}")
                print(f"   Score: {score:.4f}")

if __name__ == "__main__":
    main()