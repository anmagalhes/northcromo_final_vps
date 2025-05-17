import os
import threading
import traceback
import json
import random
import string
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import sys

import requests
import pygsheets

from fastapi import FastAPI
from app.api.order import router as order_router
from app.api.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware

# Carregar credenciais para autenticação no Google Sheets
credencias = pygsheets.authorize(
    service_file=os.getcwd() + "/sistemaNortrCromo_googleConsole.json"
)

# Cria a instância do FastAPI
app = FastAPI()

# Adiciona o middleware CORS para permitir chamadas de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por ['http://seuapp.com']
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers no FastAPI (você pode ter diferentes routers para diferentes funcionalidades)
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])

# Outros endpoints e configurações adicionais podem ser adicionados abaixo
