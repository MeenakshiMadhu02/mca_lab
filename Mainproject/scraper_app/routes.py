from flask import Flask, request, render_template, jsonify,send_from_directory
from scraper_app import app # Import the app instance
from .scraper import scrape_and_generate_pdf  # Import your scraping function
import os
from .config import PDF_DIRECTORY # Import from config.py


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            url = request.form.get("url")
            if not url:
                return jsonify({"error": "URL is required"}), 400

            pdf_filename = scrape_and_generate_pdf(url) # Assuming this function returns only the file name
            if isinstance(pdf_filename, str) and pdf_filename.startswith("Error"):
                return jsonify({"error": pdf_filename}), 500

            return jsonify({"pdf_url": f"/static/{pdf_filename}"}), 200  # Relative URL

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "An error occurred"}), 500

    return render_template("index.html")

# Serve static files (including PDFs) from the specified directory
@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory(PDF_DIRECTORY, path)