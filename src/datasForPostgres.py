from __future__ import annotations

import itertools

from database.database_config import create_connection
from psycopg2 import Error
from tqdm import tqdm
from transform import transform


def insert_data_from_dataframe(df):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Iniciar a transação
        conn.autocommit = False

        total_rows = len(df)
        progress_bar = tqdm(total=total_rows)

        for index, row in df.iterrows():
            # Inserção na tabela Regiao
            cursor.execute("""
                INSERT INTO Regiao (CodigoRegiao, Regiao)
                VALUES (%s, %s)
                ON CONFLICT (CodigoRegiao) DO NOTHING
            """, (row['CodigoRegiao'], row['Regiao']))

            # Inserção na tabela TipoAtendimento
            cursor.execute("""
                INSERT INTO TipoAtendimento (CodigoTipoAtendimento, DescricaoTipoAtendimento)
                VALUES (%s, %s)
                ON CONFLICT (CodigoTipoAtendimento) DO NOTHING
            """, (row['CodigoTipoAtendimento'], row['DescricaoTipoAtendimento']))

            # Inserção na tabela Assunto
            cursor.execute("""
                INSERT INTO Assunto (CodigoAssunto, DescricaoAssunto, GrupoAssunto)
                VALUES (%s, %s, %s)
                ON CONFLICT (CodigoAssunto) DO NOTHING
            """, (row['CodigoAssunto'], row['DescricaoAssunto'], row['GrupoAssunto']))

            # Inserção na tabela Problema
            cursor.execute("""
                INSERT INTO Problema (CodigoProblema, DescricaoProblema, GrupoProblema)
                VALUES (%s, %s, %s)
                ON CONFLICT (CodigoProblema) DO NOTHING
            """, (row['CodigoProblema'], row['DescricaoProblema'], row['GrupoProblema']))

            # Inserção na tabela Atendimento
            cursor.execute("""
                INSERT INTO Atendimento (AnoAtendimento, TrimestreAtendimento, MesAtendimento, DataAtendimento,
                                        CodigoRegiao, UF, CodigoTipoAtendimento, CodigoAssunto, CodigoProblema,
                                        SexoConsumidor, FaixaEtariaConsumidor, CEPConsumidor)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['AnoAtendimento'], row['TrimestreAtendimento'], row['MesAtendimento'], row['DataAtendimento'],
                  row['CodigoRegiao'], row['UF'], row['CodigoTipoAtendimento'], row['CodigoAssunto'],
                  row['CodigoProblema'], row['SexoConsumidor'], row['FaixaEtariaConsumidor'], row['CEPConsumidor']))

            progress_bar.update(1)

        # Confirmar a transação
        conn.commit()
        print('Dados copiados com sucesso')

        return True

    except (Exception, Error) as error:
        conn.rollback()
        print('Error while executing queries:', error)

    finally:
        if conn:
            conn.autocommit = True
            cursor.close()
            conn.close()
            progress_bar.close()
            print('Conection closed.')


for year, trimester in itertools.product(range(2), range(4)):
    df = transform(year_index=year, trimester_index=trimester + 1)
    insert_data_from_dataframe(df)
