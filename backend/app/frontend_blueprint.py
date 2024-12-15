from flask import Blueprint, send_from_directory
import os

frontend_bp = Blueprint('frontend', __name__, static_folder='frontend/dist', static_url_path='')

# Rota principal para servir o index.html
@frontend_bp.route('/')
def serve_frontend():
    return send_from_directory(os.path.join(os.getcwd(), 'frontend/dist'), 'index.html')

# Rota para servir os arquivos estáticos da pasta dist
@frontend_bp.route('/<path:path>')
def serve_static(path):
    return send_from_directory(os.path.join(os.getcwd(), 'frontend/dist'), path)
