# IR Search Engine

A compact search engine for AI/ML websites demonstrating core Information Retrieval pipelines: **crawling → indexing → ranking → query interface**. Implements **TF-IDF, PageRank, and HITS**.

## Core Features

| Component          | Key Techniques                                                        |
| ------------------ | --------------------------------------------------------------------- |
| Web Crawler        | BFS crawling, robots.txt respect, link graph construction             |
| Text Preprocessing | Tokenization, stopword removal (NLTK), stemming                       |
| Inverted Index     | Term frequencies, document frequency stats                            |
| Ranking Algorithms | TF-IDF, PageRank (global authority), HITS (query-dependent authority) |
| Search Engine      | Combined rank modes (TF-IDF only / +PageRank / +HITS)                 |

## Algorithms

### TF-IDF

* Computes term weight: **TF * log(N / DF)**
* Produces **content-relevance** ranking

### PageRank

* Power-iteration on link graph
* Evaluates **global authority** (query-independent)

### HITS

* Computes **hub and authority scores** on subgraph of query-relevant pages
* **Query-aware** authority

### Ranking Modes

| Mode              | Purpose                              |
| ----------------- | ------------------------------------ |
| TF-IDF            | Pure textual relevance               |
| TF-IDF + PageRank | Relevance + global authority         |
| TF-IDF + HITS     | Relevance + topic-specific authority |

## Run Pipeline

```bash
python src/crawler.py      # Crawl & save pages + link graph
python src/indexer.py      # Build inverted index
python src/pagerank.py     # Compute PageRank
python src/search.py       # Interactive search
```

## Example Query Flow

1. Preprocess query (tokenize, stopwords, stem)
2. Retrieve candidate docs from inverted index
3. Score with TF-IDF
4. Optionally combine with PageRank or HITS
5. Return ranked results + snippet

## Performance (50 pages)

| Task     | Time                    |
| -------- | ----------------------- |
| Crawling | 2–5 min (polite delays) |
| Indexing | < 30s                   |
| PageRank | ~10–20 iterations       |
| HITS     | ~5–15 iterations/query  |
| Search   | <2s                     |

## Project Structure

```
src/
  crawler.py      # BFS crawler, link graph
  indexer.py      # Text preprocessing, inverted index
  ranker.py       # TF-IDF scoring
  pagerank.py     # PageRank iteration
  hits.py         # HITS authority calc
  search.py       # CLI search engine
```

## Purpose

Built for learning IR systems: **crawling, indexing, ranking, authority scoring** and **search relevance evaluation**.