import numpy as np
from utils import load_json_data
from indexer import preprocess_text

def extract_query_subgraph(query_terms, link_graph, index_data):
    relevant_pages = set()
    index = index_data['index']
    
    for term in query_terms:
        if term in index:
            for doc_id in index[term]:
                doc_info = index[term][doc_id]
                relevant_pages.add(doc_info['url'])
    
    if not relevant_pages:
        return {'nodes': [], 'edges': {}}
    
    neighbors = set()
    edges = link_graph['edges']
    
    for page in relevant_pages:
        if page in edges:
            neighbors.update(edges[page])
        
        for source, targets in edges.items():
            if page in targets:
                neighbors.add(source)
    
    subgraph_nodes = list(relevant_pages.union(neighbors))
    subgraph_edges = {}
    
    for node in subgraph_nodes:
        if node in edges:
            subgraph_edges[node] = [target for target in edges[node] if target in subgraph_nodes]
        else:
            subgraph_edges[node] = []
    
    return {
        'nodes': subgraph_nodes,
        'edges': subgraph_edges,
        'relevant_pages': list(relevant_pages)
    }
    
def normalize_scores(scores):
    scores_array = np.array(list(scores.values()))
    norm = np.linalg.norm(scores_array)
    if norm == 0:
        return scores
    
    normalized = {}
    for url, score in scores.items():
        normalized[url] = score / norm
    return normalized

def update_hub_authority_scores(subgraph, hub_scores, auth_scores):
    new_hub_scores = {}
    new_auth_scores = {}
    
    for page in subgraph['nodes']:
        new_hub_scores[page] = 0
        new_auth_scores[page] = 0
    
    for page in subgraph['nodes']:
        auth_sum = 0
        for target in subgraph['edges'].get(page, []):
            auth_sum += hub_scores.get(target, 0)
        new_auth_scores[page] = auth_sum
    
    for page in subgraph['nodes']:
        hub_sum = 0
        for source, targets in subgraph['edges'].items():
            if page in targets:
                hub_sum += auth_scores.get(source, 0)
        new_hub_scores[page] = hub_sum
    
    return new_hub_scores, new_auth_scores

def calculate_hits(query_terms, link_graph, index_data, max_iterations=20):
    subgraph = extract_query_subgraph(query_terms, link_graph, index_data)
    
    if not subgraph['nodes']:
        return {}, {}
    
    hub_scores = {page: 1.0 for page in subgraph['nodes']}
    auth_scores = {page: 1.0 for page in subgraph['nodes']}
    
    for iteration in range(max_iterations):
        new_hub_scores, new_auth_scores = update_hub_authority_scores(subgraph, hub_scores, auth_scores)
        
        new_hub_scores = normalize_scores(new_hub_scores)
        new_auth_scores = normalize_scores(new_auth_scores)
        
        hub_diff = sum(abs(new_hub_scores.get(p, 0) - hub_scores.get(p, 0)) for p in subgraph['nodes'])
        auth_diff = sum(abs(new_auth_scores.get(p, 0) - auth_scores.get(p, 0)) for p in subgraph['nodes'])
        
        if hub_diff < 0.0001 and auth_diff < 0.0001:
            print(f"HITS converged after {iteration + 1} iterations")
            break
        
        hub_scores = new_hub_scores
        auth_scores = new_auth_scores
    
    return hub_scores, auth_scores

def main():
    link_graph = load_json_data('data/link_graph.json')
    index_data = load_json_data('data/inverted_index.json')
    
    if not link_graph or not index_data:
        print("Missing data files. Run crawler.py and indexer.py first.")
        return
    
    while True:
        query = input("\nEnter query for HITS analysis (or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
        
        query_terms = preprocess_text(query)
        hub_scores, auth_scores = calculate_hits(query_terms, link_graph, index_data)
        
        if not hub_scores:
            print("No relevant pages found for this query.")
            continue
        
        print(f"\nTop 5 Authorities for '{query}':")
        top_authorities = sorted(auth_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (url, score) in enumerate(top_authorities, 1):
            print(f"{i}. {url}: {score:.6f}")
        
        print(f"\nTop 5 Hubs for '{query}':")
        top_hubs = sorted(hub_scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (url, score) in enumerate(top_hubs, 1):
            print(f"{i}. {url}: {score:.6f}")

if __name__ == "__main__":
    main()