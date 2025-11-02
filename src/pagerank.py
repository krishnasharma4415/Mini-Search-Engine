import numpy as np
from utils import load_json_data, save_json_data

def build_adjacency_matrix(link_graph):
    nodes = link_graph['nodes']
    edges = link_graph['edges']
    n = len(nodes)
    
    url_to_index = {url: i for i, url in enumerate(nodes)}
    matrix = np.zeros((n, n))
    
    for source_url, target_urls in edges.items():
        if source_url in url_to_index:
            source_idx = url_to_index[source_url]
            for target_url in target_urls:
                if target_url in url_to_index:
                    target_idx = url_to_index[target_url]
                    matrix[target_idx][source_idx] = 1
    
    return matrix, url_to_index

def handle_dangling_nodes(matrix):
    n = matrix.shape[0]
    
    for col in range(n):
        col_sum = np.sum(matrix[:, col])
        if col_sum == 0:
            matrix[:, col] = 1.0 / n
        else:
            matrix[:, col] = matrix[:, col] / col_sum
    
    return matrix
    
def calculate_pagerank(link_graph, damping_factor=0.85, max_iterations=30, threshold=0.0001):
    matrix, url_to_index = build_adjacency_matrix(link_graph)
    matrix = handle_dangling_nodes(matrix)
    
    n = len(link_graph['nodes'])
    pagerank_scores = np.ones(n) / n
    
    for iteration in range(max_iterations):
        new_scores = (1 - damping_factor) / n + damping_factor * np.dot(matrix, pagerank_scores)
        
        if np.sum(np.abs(new_scores - pagerank_scores)) < threshold:
            print(f"PageRank converged after {iteration + 1} iterations")
            break
        
        pagerank_scores = new_scores
    
    index_to_url = {i: url for url, i in url_to_index.items()}
    scores_dict = {index_to_url[i]: float(score) for i, score in enumerate(pagerank_scores)}
    
    return scores_dict

def main():
    link_graph = load_json_data('link_graph.json')
    if not link_graph:
        print("No link graph found. Run src/crawler.py first.")
        return
    
    print(f"Calculating PageRank for {len(link_graph['nodes'])} pages...")
    
    pagerank_scores = calculate_pagerank(link_graph)
    save_json_data(pagerank_scores, 'pagerank_scores.json')
    
    print("PageRank calculation completed")
    print(f"Saved scores to data/pagerank_scores.json")
    
    top_pages = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 pages by PageRank:")
    for i, (url, score) in enumerate(top_pages, 1):
        print(f"{i}. {url}: {score:.6f}")

if __name__ == "__main__":
    main()