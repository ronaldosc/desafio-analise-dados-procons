from __future__ import annotations

import pathlib
from os import getenv

import psycopg2 as pg
from dotenv import load_dotenv
from psycopg2 import Error as err

load_dotenv()

# environment variables
db_host = getenv('DB_HOST')
db_port = getenv('DB_PORT')
db_name = getenv('DB_NAME')
db_user = getenv('DB_USER')
db_password = getenv('DB_PASSWORD')


def create_connection():
    try:
        conn = pg.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            dbname=db_name
        )
        print('Database connected successfully')

    except err:
        print(f'Database not connected successfully.\n    Error message: {err}')

    return conn


def execute_schema_queries():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Ler o arquivo schema.sql
        queries = pathlib.Path('src/database/schema.sql').read_text()
        # Executar as queries
        cursor.execute(queries)
        conn.commit()
        print('Queries executadas com sucesso.')
        return True

    except (Exception, err) as error:
        conn.rollback()
        print('Erro na execução das queries:', error)

    finally:
        if conn:
            # Restaurar o autocommit para True
            conn.autocommit = True
            cursor.close()
            conn.close()
            print('Conexão fechada.')
