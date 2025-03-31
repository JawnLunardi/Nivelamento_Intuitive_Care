from fastapi import FastAPI
import pymysql
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "ans_data"
}

@app.get("/buscar_operadora/")
def buscar_operadora(nome: str):

    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    sql = f"""
        SELECT * FROM operadoras 
        WHERE razao_social LIKE %s OR nome_fantasia LIKE %s
        LIMIT 10
    """
    
    cursor.execute(sql, (f"%{nome}%", f"%{nome}%"))
    result = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {"operadoras": result}

