# In config.py
import os

# This should point to the static folder in the root of your Flask app
PDF_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")