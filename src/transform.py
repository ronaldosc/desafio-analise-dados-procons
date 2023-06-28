from __future__ import annotations

import pandas as pd
from config import dataset_folder_name
from config import dataset_value_dictionary
from config import dataset_years


class CSVReader:
    def __init__(self, folder_name: str, years: list[int], value_dictionary: dict[str, tuple[str, int]]):
        self.folder_name = folder_name
        self.years = years
        self.value_dictionary = value_dictionary

    def read_csv(self, year_index: int, file_number: int) -> pd.DataFrame:
        csv_file = f'{self.folder_name}/{self.years[year_index]}_{file_number}.csv'
        print(csv_file)
        encodings = ['utf-8', 'cp1252']
        separators = [';', '\t']

        for encoding in encodings:
            for separator in separators:
                try:
                    df = pd.read_csv(csv_file, on_bad_lines='skip', encoding=encoding, sep=separator)
                    break  # Break out of the inner loop if successful
                except UnicodeDecodeError as e:
                    print(f'An error occurred: {e}')
            else:
                continue  # Continue to the next encoding if the inner loop wasn't broken
            break  # Break out of the outer loop if successful

        df = df.fillna(0)
        for column, (data_type, slice_size) in self.value_dictionary.items():
            if slice_size is not None:
                df[column] = df[column].astype(str).str.slice(0, slice_size)
            df[column] = df[column].astype(data_type)
        return df


csv_reader = CSVReader(dataset_folder_name, dataset_years, dataset_value_dictionary)
df = csv_reader.read_csv(0, 1)
print(df.head())
