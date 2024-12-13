# app/cors/__init__.py
from flask_cors import CORS
#from typing import List

#from pydantic import BaseSettings, AnyHttpUrl
#from sqlalchemy.ext.declarative import declarative_base


#class Settings(BaseSettings):

    #API_V1_STR: str = '/ap'

def configure_cors(app):
    CORS(app)
