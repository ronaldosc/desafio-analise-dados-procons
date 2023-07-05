from os import getenv
from dotenv import load_dotenv
import psycopg2 as pg
from psycopg2 import Error as err

load_dotenv()

# environment variables
db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")
db_name = getenv("DB_NAME")
db_user = getenv("DB_USER")
db_password = getenv("DB_PASSWORD")

def create_connection():
    try:
        conn = pg.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            dbname=db_name
        )
        print("Database connected successfully")

    except err:
        print(f"Database not connected successfully.\n    Error message: {err}")

    return conn

def create_tables():
    conn = create_connection()
    cur = conn.cursor()

    try:
        # Lendo o arquivo .sql com as queries de criação de tabelas
        with open('schema.sql', 'r', encoding='utf-8') as sql_file:
            # Lendo o conteúdo do arquivo
            queries = sql_file.read()

            # Executando as queries usando o cursor
            cur.execute(queries)

        # Commit das alterações
        conn.commit()

        print("Tabelas criadas com sucesso")

        # Exemplo: Realizando uma consulta na tabela recém-criada
        cur.execute("SELECT * FROM Assunto")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except err:
        print(f"Erro ao criar tabelas.\n    Mensagem de erro: {err}")

    cur.close()
    conn.close()
