#app/config.py
# app/config.py
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

class Config:
    """Configurações base"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desabilita a modificação de objetos para evitar overhead

    @staticmethod
    def get_database_uri():
        """Constrói e retorna a URI do banco de dados a partir das variáveis de ambiente"""
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_PORT = os.getenv('DATABASE_PORT')
        DATABASE_NAME = os.getenv('DATABASE_NAME')

        if not all([DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME]):
            raise ValueError("Uma ou mais variáveis de ambiente do banco de dados não foram configuradas corretamente.")
        
        return f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}'

class DevelopmentConfig(Config):
    """Configuração de Desenvolvimento"""
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()

class ProductionConfig(Config):
    """Configuração de Produção"""
    SQLALCHEMY_DATABASE_URI = Config.get_database_uri()
