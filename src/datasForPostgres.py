from __future__ import annotations

import itertools

from database.database_config import create_connection
from psycopg2 import Error
from transform import transform


def insert_data_from_dataframe(df):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Iniciar a transação
        conn.autocommit = False

        for index, row in df.iterrows():
            # Inserção na tabela ChamadosProcon
            # cursor.execute("""
            #     INSERT INTO "ChamadosProcon" ("dataAtendimento", "nomeRegiao", "ufRegiao", "descricaoAtendimento", "descricaoAssunto", "descricaoProblema", "sexo", "faixaEtaria", "cep")
            #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            # """, (row['DataAtendimento'], row['Regiao'], row['UF'], row['DescricaoTipoAtendimento'], row['DescricaoAssunto'], row['DescricaoProblema'], row['SexoConsumidor'], row['FaixaEtariaConsumidor'], row['CEPConsumidor'],))

            # Inserção na tabela Regiao
            cursor.execute("""
                INSERT INTO "Regiao" ("nomeRegiao", "ufRegiao")
                VALUES (%s, %s)
            """, (row['Regiao'], row['UF'],))

            # Inserção na tabela TipoAtendimento
            cursor.execute("""
                INSERT INTO "TipoAtendimento" ("descricaoAtendimento")
                VALUES (%s)
            """, (row['DescricaoTipoAtendimento'],))

            # Inserção na tabela Assunto
            cursor.execute("""
                INSERT INTO "Assunto" ("descricaoAssunto")
                VALUES (%s)
            """, (row['DescricaoAssunto'],))

            # Inserção na tabela Problema
            cursor.execute("""
                INSERT INTO "Problema" ("descricaoProblema")
                VALUES (%s)
            """, (row['DescricaoProblema'],))

            # Inserção na tabela Atendimento
            cursor.execute("""
                INSERT INTO "Atendimento" ("sexo", "faixaEtaria", "cep", "dataAtendimento")
                VALUES (%s, %s, %s, %s)
            """, (row['SexoConsumidor'], row['FaixaEtariaConsumidor'], row['CEPConsumidor'], row['DataAtendimento'],))

        # Confirmar a transação
        conn.commit()
        print('Dados copiados com sucesso')

        return True

    except (Exception, Error) as error:
        # Reverter a transação em caso de erro
        conn.rollback()
        print('Erro ao copiar os dados:', error)

    finally:
        if conn:
            # Restaurar o autocommit para True
            conn.autocommit = True
            cursor.close()
            conn.close()
            print('Conexão fechada.')


for year, trimester in itertools.product(range(2), range(4)):
    print(f'{2019+year}_{1+trimester}')
    df = transform(year_index=year, trimester_index=trimester + 1)
    insert_data_from_dataframe(df)
