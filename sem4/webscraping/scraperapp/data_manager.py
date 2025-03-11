# data_manager.py
import os
import json
import hashlib
from urllib.parse import urlparse
from datetime import datetime

from .config import JSON_DIRECTORY ,MARKDOWN_DIRECTORY

def get_filename_from_url(url):
    """Generate a consistent filename from a URL."""
    # Extract domain for readability
    domain = urlparse(url).netloc.replace("www.", "")
    # Add timestamp and hash for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    
    return f"{domain}_{timestamp}_{url_hash}"

def save_as_json(scraped_data, base_filename):
    """Save scraped data as JSON."""
    json_path = os.path.join(JSON_DIRECTORY, f"{base_filename}.json")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2)
    
    return json_path

def save_as_markdown(scraped_data, base_filename):
    """Save scraped data as Markdown."""
    markdown_path = os.path.join(MARKDOWN_DIRECTORY, f"{base_filename}.md")
    
    with open(markdown_path, 'w', encoding='utf-8') as f:
        # Write title
        if 'title' in scraped_data:
            f.write(f"# {scraped_data['title']}\n\n")
        
        # Write URL and timestamp
        f.write(f"Source: [{scraped_data['url']}]({scraped_data['url']})\n")
        f.write(f"Date scraped: {scraped_data['date_scraped']}\n\n")
        
        # Write content
        f.write("## Content\n\n")
        for item in scraped_data['content']:
            if item['type'] == 'h1':
                f.write(f"# {item['text']}\n\n")
            elif item['type'] == 'h2':
                f.write(f"## {item['text']}\n\n")
            elif item['type'] == 'h3':
                f.write(f"### {item['text']}\n\n")
            elif item['type'] == 'p':
                f.write(f"{item['text']}\n\n")
            elif item['type'] == 'li':
                f.write(f"* {item['text']}\n")
        
        # Add images
        if scraped_data['images']:
            f.write("\n## Images\n\n")
            for img in scraped_data['images']:
                if img['local_path']:
                    relative_path = os.path.relpath(img['local_path'], os.path.dirname(markdown_path))
                    relative_path = relative_path.replace('\\', '/')  # Fix Windows paths
                    f.write(f"![{img.get('alt', 'Image')}]({relative_path})\n\n")
    
    return markdown_path