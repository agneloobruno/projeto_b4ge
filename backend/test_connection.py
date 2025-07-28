import psycopg2

try:
    conn = psycopg2.connect(
        dbname="b4gedb",
        user="b4geuser",
        password="b4gepass",
        host="localhost",  # ou 'db' se rodar via Docker
        port="5432"
    )
    print("Conexão estabelecida com sucesso!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:", e)
