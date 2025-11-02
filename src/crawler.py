import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time
import logging
from utils import normalize_url, extract_text_content, safe_request, setup_logging

def fetch_page(url):
    logger = logging.getLogger(__name__)
    
    if not respect_robots_txt(url):
        logger.info(f"Robots.txt disallows crawling: {url}")
        return None
    
    response = safe_request(url)
    if not response:
        return None
    
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""
        
        content = extract_text_content(soup)
        links = extract_links(soup, url)
        
        return {
            'url': url,
            'title': title,
            'content': content,
            'links': links,
            'crawl_timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    except Exception as e:
        logger.error(f"Error parsing page {url}: {e}")
        return None

def extract_links(soup, base_url):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        normalized = normalize_url(href, base_url)
        if normalized and is_valid_domain(normalized):
            links.append(normalized)
    return list(set(links))

def respect_robots_txt(url):
    try:
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        
        return rp.can_fetch('*', url)
    except:
        return True

def is_valid_domain(url):
    parsed = urlparse(url)
    valid_domains = [
        'kaggle.com',
        'paperswithcode.com', 
        'huggingface.co',
        'ai.googleblog.com',
        'blog.google',
        'research.google',
        'arxiv.org',
        'towards',
        'medium.com'
    ]
    
    return any(domain in parsed.netloc.lower() for domain in valid_domains)
    
from collections import deque

def crawl_pages(seed_urls, max_pages=50, max_depth=3):
    logger = setup_logging()
    
    url_queue = deque()
    visited_urls = set()
    crawled_pages = []
    
    for url in seed_urls:
        url_queue.append((url, 0))
    
    logger.info(f"Starting crawl with {len(seed_urls)} seed URLs")
    
    while url_queue and len(crawled_pages) < max_pages:
        current_url, depth = url_queue.popleft()
        
        if current_url in visited_urls or depth > max_depth:
            continue
        
        visited_urls.add(current_url)
        logger.info(f"Crawling ({len(crawled_pages)+1}/{max_pages}): {current_url}")
        
        page_data = fetch_page(current_url)
        if page_data:
            crawled_pages.append(page_data)
            
            if depth < max_depth:
                for link in page_data['links']:
                    if link not in visited_urls:
                        url_queue.append((link, depth + 1))
        
        time.sleep(1.5)
    
    logger.info(f"Crawling completed. Total pages: {len(crawled_pages)}")
    return crawled_pages
    
from utils import save_json_data

def build_link_graph(crawled_pages):
    all_urls = {page['url'] for page in crawled_pages}
    
    nodes = list(all_urls)
    edges = {}
    
    for page in crawled_pages:
        page_url = page['url']
        outgoing_links = [link for link in page['links'] if link in all_urls]
        edges[page_url] = outgoing_links
    
    return {
        'nodes': nodes,
        'edges': edges
    }

def main():
    seed_urls = [
        'https://www.kaggle.com/discussions',
        'https://paperswithcode.com',
        'https://huggingface.co/blog',
        'https://ai.googleblog.com'
    ]
    
    crawled_data = crawl_pages(seed_urls, max_pages=50, max_depth=2)
    
    save_json_data(crawled_data, 'crawled_pages.json')
    print(f"Saved {len(crawled_data)} pages to data/crawled_pages.json")
    
    link_graph = build_link_graph(crawled_data)
    save_json_data(link_graph, 'link_graph.json')
    print(f"Saved link graph with {len(link_graph['nodes'])} nodes to data/link_graph.json")

if __name__ == "__main__":
    main()