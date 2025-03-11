from flask import Flask, render_template, request, send_from_directory
from .scraper import scrape_and_generate_pdf  # Import your scraping function

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            pdf_filename = scrape_and_generate_pdf(url)
            if isinstance(pdf_filename, str) and pdf_filename.startswith("Error"): # Check for errors
                return render_template("index.html", error=pdf_filename) # Display the error
            return send_from_directory(directory=".", path=pdf_filename, as_attachment=True)
        else:
            return render_template("index.html", error="Please enter a URL.")

    return render_template("index.html")

# ... (rest of the code)