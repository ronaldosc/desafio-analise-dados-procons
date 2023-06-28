from __future__ import annotations

import pandas as pd


class CSVReader:
    def __init__(self, folder_name: str, years: list[int], value_dictionary: dict[str, tuple[str, int]]):
        self.folder_name = folder_name
        self.years = years
        self.value_dictionary = value_dictionary

    def read_csv(self, year_index: int, file_number: int) -> pd.DataFrame:
        csv_file = f'{self.folder_name}/{self.years[year_index]}_{file_number}.csv'
        print(csv_file)
        try:
            df = pd.read_csv(csv_file, on_bad_lines='skip', encoding='utf-8', sep=';')
        except UnicodeDecodeError:
            df = pd.read_csv(csv_file, on_bad_lines='skip', encoding='cp1252', sep='\t')
        df = df.fillna(0)
        for column, (data_type, slice_size) in self.value_dictionary.items():
            if slice_size is not None:
                df[column] = df[column].astype(str).str.slice(0, slice_size)
            df[column] = df[column].astype(data_type)
        return df


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

csv_reader = CSVReader('csv_files', [2019, 2020, 2021, 2022, 2023], value_dictionary)
df = csv_reader.read_csv(0, 1)
print(df.head())
