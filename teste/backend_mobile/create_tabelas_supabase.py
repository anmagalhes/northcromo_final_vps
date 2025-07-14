import os
import psycopg2
import traceback

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )
    print("✅ Conectado com sucesso!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:")
    traceback.print_exc()
