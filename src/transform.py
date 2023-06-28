from __future__ import annotations

import pandas as pd


folder_name = 'csv_files'
years = [2019, 2020, 2021, 2022, 2023]
csv_file = f'{folder_name}/{years[0]}_1.csv'
print(csv_file)

# Define the data types and slice sizes for each column
value_dictionary = {
    'AnoAtendimento': ('int64', None),
    'TrimestreAtendimento': ('int64', None),
    'MesAtendimento': ('int64', None),
    'DataAtendimento': ('datetime64[ns]', None),
    'CodigoRegiao': ('object', 2),
    'Regiao': ('object', 15),
    'UF': ('object', 2),
    'CodigoTipoAtendimento': ('int64', None),
    'DescricaoTipoAtendimento': ('object', 50),
    'CodigoAssunto': ('int64', None),
    'DescricaoAssunto': ('object', 160),
    'GrupoAssunto': ('object', 160),
    'CodigoProblema': ('int64', None),
    'DescricaoProblema': ('object', 160),
    'GrupoProblema': ('object', 160),
    'SexoConsumidor': ('object', 1),
    'FaixaEtariaConsumidor': ('object', 20),
    'CEPConsumidor': ('object', 8)
}


# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file, on_bad_lines='skip', encoding='utf-8', sep=';')

# Replace non-finite values in all columns with a default value
df = df.fillna(0)  # Replace with a default value of 0

for column, (data_type, slice_size) in value_dictionary.items():
    if slice_size is not None:
        df[column] = df[column].astype(str).str.slice(0, slice_size)

    df[column] = df[column].astype(data_type)


# Display the DataFrame
print(df.head())
