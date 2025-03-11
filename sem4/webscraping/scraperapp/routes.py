from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
import os
from flask import send_from_directory
# Import your scraper functionality
from scraper_app.scraper import scrape_and_generate_pdf

app = Flask(__name__, static_folder='static')
CORS(app)

# Define the absolute path to your static directory
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
print(f"Static directory path: {static_dir}")

# Create the static directory if it doesn't exist
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"Created static directory at: {static_dir}")

@app.route('/static/<path:filename>')
def serve_static_files(filename):
    print(f"Serving static file: {filename}")
    print(f"Looking in directory: {static_dir}")
    return send_from_directory(static_dir, filename)

@app.route("/api/scrape", methods=["POST"])
def scrape():
    data = request.json
    url = data.get("url")
    print(f"Scraping URL: {url}")  # Debugging

    pdf_filename = "scrapedcontent.pdf"
    pdf_path = os.path.join(static_dir, pdf_filename)
    print(f"Expected PDF Path: {pdf_path}")  # Debugging

    # Check if PDF already exists
    if os.path.exists(pdf_path):
        print("⚠️ Existing PDF detected. Deleting...")
        os.remove(pdf_path)

    try:
        # Use your actual scraper function 
        result = scrape_and_generate_pdf(url, pdf_path)
        
        # Check if PDF was really created
        if os.path.exists(pdf_path):
            print(f"✅ PDF Successfully Created at: {os.path.abspath(pdf_path)}")
            file_size = os.path.getsize(pdf_path)
            print(f"PDF file size: {file_size} bytes")
            
            # Return the absolute URL path to the PDF
            return jsonify({
                "pdf_url": f"/static/{pdf_filename}",
                "file_size": file_size
            })
        else:
            print("❌ PDF was NOT created")
            return jsonify({"error": "PDF file was not generated."}), 500

    except Exception as e:
        print(f"❌ Error Creating PDF: {e}")
        return jsonify({"error": f"PDF file was not generated: {str(e)}"}), 500

# Add this for better debugging
@app.route("/test")
def test():
    return jsonify({"status": "API is running"})