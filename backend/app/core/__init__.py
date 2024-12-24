# app/cors/__init__.py
from flask_cors import CORS

def configure_cors(app):
     CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE"], supports_credentials=True)
