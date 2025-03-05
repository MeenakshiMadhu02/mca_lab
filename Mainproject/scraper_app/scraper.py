import os
import time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
from .config import PDF_DIRECTORY

# Exclusion Patterns to filter out unwanted content
EXCLUDE_PATTERNS = [
    "Ipsum porta proin", "Sit id nullam", "Convallis risus",
    "Tellus faucibus duis", "Phasellus at nisi"
]
EXCLUDE_URL_PATTERNS = ["/respond"]

def is_same_domain(link, base_url):
    from urllib.parse import urlparse
    return urlparse(link).netloc == urlparse(base_url).netloc

def download_image(image_url, save_dir):
    """Download and process images (convert to RGB if needed)."""
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_name = os.path.basename(image_url).split("?")[0]  # Remove query parameters
            image_path = os.path.join(save_dir, image_name)

            with open(image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            with PILImage.open(image_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")  # Convert RGBA to RGB
                converted_path = image_path.rsplit(".", 1)[0] + ".jpg"
                img.save(converted_path, "JPEG")
                os.remove(image_path)  # Remove original file
                return converted_path

        print(f"❌ Failed to download image: {image_url}")
    except Exception as e:
        print(f"❌ Error downloading image {image_url}: {e}")
    return None

def should_exclude(text):
    """Check if text matches exclusion patterns."""
    return any(pattern in text for pattern in EXCLUDE_PATTERNS)

def should_exclude_url(url):
    """Check if URL matches exclusion patterns."""
    return any(pattern in url for pattern in EXCLUDE_URL_PATTERNS)

def scrape_page(page, url, base_url, image_save_dir, doc_elements, processed_images, is_home_page):
    print(f"\nScraping URL: {url}\n" + "-" * 50)

    try:
        # Wait for a specific element that indicates the page content has loaded (adjust the selector and timeout as needed)
        page.wait_for_selector("body", timeout=10000) # Wait for the body element

        # If there are specific elements loaded by JS that you need, wait for them:
        # page.wait_for_selector(".element-loaded-by-js", timeout=10000)

    except Exception as e:
        print(f"❌ Timeout waiting for element on {url}: {e}")
        return  # Or handle the timeout as needed

    soup = BeautifulSoup(page.content(), "html.parser")  # Parse the fully rendered HTML

    styles = getSampleStyleSheet()
    styles["Title"].fontSize = 16
    styles["Title"].spaceAfter = 10
    styles["Heading1"].fontSize = 14
    styles["Heading1"].spaceAfter = 8
    styles["BodyText"].fontSize = 11
    styles["BodyText"].leading = 14  # Adjust line spacing

    if is_home_page:
        title = soup.find("title").text.strip() if soup.find("title") else "No Title"
        doc_elements.append(Paragraph(f"<b>Page Title:</b> {title}", styles["Title"]))
        doc_elements.append(Spacer(1, 10))

    # Remove footer elements
    for footer in soup.find_all("footer"):
        footer.decompose()
    for element in soup.find_all(attrs={"id": ["footer", "site-footer"], "class": ["footer", "site-footer"]}):
        element.decompose()

    # Extract text and images in order of appearance
    for element in soup.find_all(["p", "h1", "h2", "h3", "ul", "li", "img"]):
        if element.name in ["h1", "h2", "h3"]:
            text = element.get_text(strip=True)
            if not should_exclude(text):
                doc_elements.append(Paragraph(text, styles["Heading1"]))
                doc_elements.append(Spacer(1, 10))

        elif element.name == "p":
            text = element.get_text(strip=True)
            if not should_exclude(text):
                doc_elements.append(Paragraph(text, styles["BodyText"]))
                doc_elements.append(Spacer(1, 5))

        elif element.name == "ul":
            for li in element.find_all("li"):
                li_text = li.get_text(strip=True)
                if not should_exclude(li_text):
                    doc_elements.append(Paragraph(f"• {li_text}", styles["BodyText"]))
            doc_elements.append(Spacer(1, 5))

        elif element.name == "img":
            img_url = urljoin(base_url, element.get("src"))
            if img_url in processed_images:
                continue
            processed_images.add(img_url)

            image_path = download_image(img_url, image_save_dir)
            if image_path:
                try:
                    img = Image(image_path, width=400, height=250)  # Adjust size
                    doc_elements.append(Spacer(1, 10))
                    doc_elements.append(img)
                    doc_elements.append(Spacer(1, 10))
                except Exception as e:
                    print(f"❌ Error adding image to PDF: {e}")

def crawl_website(page, start_url, visited, base_url, image_save_dir, doc_elements, is_home_page):
    """Recursively scrape content from the website."""
    if start_url in visited or should_exclude_url(start_url):
        return

    try:
        page.goto(start_url, timeout=60000)
        page.wait_for_load_state("load")
        visited.add(start_url)

        processed_images = set() # This is the crucial line that was missing
        scrape_page(page, start_url, base_url, image_save_dir, doc_elements, processed_images, is_home_page)

        soup = BeautifulSoup(page.content(), "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = urljoin(base_url, a_tag["href"])
            if is_same_domain(href, base_url) and href not in visited:
                links.add(href)

        for link in links:
            crawl_website(page, link, visited, base_url, image_save_dir, doc_elements, False)

    except Exception as e:
        print(f"❌ Error processing {start_url}: {e}")

def scrape_and_generate_pdf(start_url, pdf_filename="scraped_content.pdf"):
    image_save_dir = "images"
    os.makedirs(image_save_dir, exist_ok=True)

    pdf_file = os.path.join(PDF_DIRECTORY,pdf_filename)  # Use absolute path
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    doc_elements = []  # Initialize doc_elements HERE (This was missing)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            visited = set()
            crawl_website(page, start_url, visited, start_url, image_save_dir, doc_elements, True)  # Pass doc_elements

            browser.close()

        doc.build(doc_elements)
        print(f"✅ Scraping complete. Data saved to {pdf_file}")

        if os.path.exists(pdf_file):
            return pdf_file
        else:
            return "Error: PDF file not created."

    except Exception as e:
        print(f"❌ Error during scraping or PDF generation: {e}")
        return f"Error: {e}"


# The main function is no longer needed here, as the Flask route will call scrape_and_generate_pdf