import json
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

def load_json_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_data(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def normalize_url(url, base_url):
    if not url:
        return None
    
    url = url.strip()
    if url.startswith('#'):
        return None
    
    if url.startswith('mailto:') or url.startswith('tel:'):
        return None
    
    full_url = urljoin(base_url, url)
    parsed = urlparse(full_url)
    
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        normalized += f"?{parsed.query}"
    
    return normalized

def extract_text_content(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text
    
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('crawler.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def safe_request(url, timeout=10):
    import requests
    try:
        response = requests.get(url, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return None

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False