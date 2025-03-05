from flask import Flask
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (for development)

from . import routes  # Import routes *after* CORS is enabled