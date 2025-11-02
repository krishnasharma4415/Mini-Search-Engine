# IR Search Engine

A simple web crawler and search engine for AI/ML domain websites demonstrating core Information Retrieval concepts including web crawling, indexing, and ranking algorithms (TF-IDF, PageRank, and HITS).

## Project Overview

This educational project implements a complete information retrieval system with the following components:

- **Web Crawler**: Breadth-first crawling of AI/ML focused websites
- **Indexer**: Inverted index construction with text preprocessing
- **TF-IDF Ranker**: Term frequency-inverse document frequency scoring
- **PageRank**: Link-based authority scoring algorithm
- **HITS**: Hub and authority analysis for query-specific results
- **Search Interface**: Command-line interface with multiple ranking options

## Setup Instructions

### 1. Install Dependencies

**Core Dependencies (Required):**
```bash
pip install -r requirements.txt
```

**Optional Dependencies (Development & Notebooks):**
For enhanced development experience, Jupyter notebooks, and additional tools:
```bash
pip install -r requirements-optional.txt
```

**Manual Installation:**
You can also install dependencies individually:
```bash
# Core only
pip install requests beautifulsoup4 nltk numpy

# With optional tools
pip install jupyter matplotlib seaborn pytest black
```

### 2. Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords')"
```

**Note**: The NLTK stopwords corpus is required for text preprocessing. The indexer will automatically attempt to download it if not present, but you can also download it manually using the command above.

### 3. Create Data Directory
The `data/` directory will be created automatically when you run the crawler.

## How to Run

### Step 1: Crawl Websites
```bash
python src/crawler.py
```
This will:
- Crawl 50 pages from AI/ML websites (Kaggle, Papers with Code, Hugging Face, Google AI Blog)
- Save crawled data to `data/crawled_pages.json`
- Generate link graph in `data/link_graph.json`
- Respect robots.txt and add delays between requests

### Step 2: Build Search Index
```bash
python src/indexer.py
```
This will:
- Process crawled content with text preprocessing
- Build inverted index with term frequencies
- Save index to `data/inverted_index.json`

### Step 3: Calculate PageRank Scores
```bash
python src/pagerank.py
```
This will:
- Calculate PageRank scores for all crawled pages
- Save scores to `data/pagerank_scores.json`
- Display top 10 pages by PageRank

### Step 4: Start Searching
```bash
python src/search.py
```
This provides an interactive search interface with three ranking options:
1. **TF-IDF only**: Pure content-based ranking
2. **TF-IDF + PageRank**: Combined content and authority ranking (60% TF-IDF, 40% PageRank)
3. **TF-IDF + HITS Authority**: Combined content and query-specific authority (60% TF-IDF, 40% HITS)

## Sample Usage

```
Enter search query (or 'quit' to exit): machine learning
Select ranking mode (1-3): 2

Results for 'machine learning' using TF-IDF + PageRank
Search completed in 0.045 seconds
--------------------------------------------------------------------------------
1. Introduction to Machine Learning
   URL: https://example.com/ml-intro
   Score: 0.234567
   Snippet: Machine learning is a subset of artificial intelligence...

2. Deep Learning Fundamentals
   URL: https://example.com/deep-learning
   Score: 0.198432
   Snippet: Deep learning uses neural networks with multiple layers...
```

## Sample Queries for Testing

- "deep learning"
- "natural language processing"
- "computer vision"
- "reinforcement learning"
- "neural networks"
- "artificial intelligence"
- "data science"
- "machine learning algorithms"

## Algorithm Comparison

### TF-IDF Only
- **Strengths**: Fast, content-focused, good for specific term matching
- **Weaknesses**: Ignores page authority and link structure

### TF-IDF + PageRank
- **Strengths**: Balances content relevance with overall page authority
- **Weaknesses**: PageRank is query-independent, may favor popular pages

### TF-IDF + HITS Authority
- **Strengths**: Query-specific authority calculation, identifies topic experts
- **Weaknesses**: Slower computation, requires sufficient link connectivity

## Performance Benchmarks

- **Crawling**: ~50 pages in 2-5 minutes (with 1.5s delays)
- **Indexing**: <30 seconds for 50 pages
- **PageRank**: Converges in 10-20 iterations
- **HITS**: Converges in 5-15 iterations per query
- **Search**: <2 seconds response time

## Project Structure

```
ir_search_engine/
├── src/                # Source code
│   ├── crawler.py      # Web crawling functionality
│   ├── indexer.py      # Text processing and indexing
│   ├── ranker.py       # TF-IDF ranking implementation
│   ├── pagerank.py     # PageRank algorithm
│   ├── hits.py         # HITS algorithm
│   ├── search.py       # Search interface and result combination
│   ├── utils.py        # Utility functions
│   ├── stats.py        # Statistics generation
│   └── evaluation.py   # Query evaluation and comparison
├── tests/              # Test files
│   ├── test_algorithms.py  # Unit tests
│   └── test_integration.py # Integration tests
├── notebooks/          # Jupyter notebooks for experimentation
├── data/              # Generated data files
│   ├── crawled_pages.json
│   ├── link_graph.json
│   ├── inverted_index.json
│   └── pagerank_scores.json
├── requirements.txt         # Core Python dependencies
├── requirements-optional.txt # Optional development dependencies  
└── README.md               # This file
```

## Testing

### Run Unit Tests
```bash
python tests/test_algorithms.py
```

### Run Integration Tests
```bash
python tests/test_integration.py
```

### Generate Statistics
```bash
python src/stats.py
```

## Limitations and Future Improvements

### Current Limitations
- File-based storage limits scalability
- Single-threaded crawler design
- Simple text preprocessing (no advanced NLP)
- Limited to 50-100 pages for educational purposes
- No web interface (command-line only)

### Potential Improvements
- Database storage for better scalability
- Multi-threaded crawling for faster data collection
- Advanced text processing (named entity recognition, topic modeling)
- Web-based user interface
- Real-time indexing and incremental updates
- More sophisticated ranking algorithms (BM25, learning-to-rank)
- Query expansion and spell correction
- Result clustering and faceted search

## Educational Value

This project demonstrates:
- **Web Crawling**: Breadth-first search, robots.txt compliance, URL normalization
- **Text Processing**: Tokenization, stopword removal, stemming
- **Information Retrieval**: Inverted indexing, TF-IDF scoring
- **Link Analysis**: PageRank and HITS algorithms
- **System Design**: Modular architecture, error handling, testing

Perfect for understanding the fundamentals of search engines and information retrieval systems.