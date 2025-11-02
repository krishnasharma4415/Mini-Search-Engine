import nltk
import re
from collections import defaultdict, Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from utils import load_json_data, save_json_data

def download_nltk_data():
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

def preprocess_text(text):
    download_nltk_data()
    
    text = text.lower()
    
    tokens = re.findall(r'\b[a-zA-Z]+\b', text)
    
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]
    
    return tokens

def calculate_term_frequencies(tokens):
    return dict(Counter(tokens))

def build_inverted_index(crawled_data):
    inverted_index = defaultdict(dict)
    document_frequencies = defaultdict(int)
    
    for doc_id, page in enumerate(crawled_data):
        full_text = f"{page['title']} {page['content']}"
        tokens = preprocess_text(full_text)
        term_frequencies = calculate_term_frequencies(tokens)
        
        unique_terms = set(tokens)
        for term in unique_terms:
            document_frequencies[term] += 1
        
        for term, tf in term_frequencies.items():
            inverted_index[term][doc_id] = {
                'tf': tf,
                'url': page['url'],
                'title': page['title']
            }
    
    index_with_df = {
        'index': dict(inverted_index),
        'document_frequencies': dict(document_frequencies),
        'total_documents': len(crawled_data)
    }
    
    return index_with_df

def calculate_document_frequencies(index):
    return {term: len(postings) for term, postings in index.items()}

def main():
    crawled_data = load_json_data('crawled_pages.json')
    if not crawled_data:
        print("No crawled data found. Run src/crawler.py first.")
        return
    
    print(f"Building index from {len(crawled_data)} documents...")
    
    index_data = build_inverted_index(crawled_data)
    save_json_data(index_data, 'inverted_index.json')
    
    print(f"Index built with {len(index_data['index'])} unique terms")
    print(f"Saved to data/inverted_index.json")

if __name__ == "__main__":
    main()