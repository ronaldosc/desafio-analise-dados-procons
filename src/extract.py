from __future__ import annotations

import os
import urllib.parse
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Extract:
    def __init__(self, url, folder_name, years, ignore=None):
        if ignore is None:
            ignore = []
        self.url = url
        self.folder_name = folder_name
        self.years = years
        self.ignore = ignore
        self.total_files = 0

    def count_files_to_download(self):
        elements = self._get_resource_elements()
        return sum(bool(self._is_valid_file(element)) for element in elements)

    def download_files(self):
        # Count the total number of files to download
        self.total_files = self.count_files_to_download()

        # Create a directory to store the downloaded files
        os.makedirs(self.folder_name, exist_ok=True)

        elements = self._get_resource_elements()
        # Iterate through the elements and download the .csv files from 2019 to 2023
        progress_bar = tqdm(total=self.total_files, unit='file')

        year_count = defaultdict(int)

        for element in elements:
            if not self._is_valid_file(element):
                continue

            file_url = self._get_file_url(element)
            file_name = self._get_file_name(element)

            year = next(year for year in self.years if str(year) in file_name)
            year_count[year] += 1
            count = year_count[year]
            new_file_name = f'{year}_{count}.csv'
            new_file_path = os.path.join(self.folder_name, new_file_name)

            self._download_file(file_url, new_file_path)
            progress_bar.update(1)

        progress_bar.close()

        print('All .csv files downloaded.')

    def _download_file(self, file_url, file_path):
        if os.path.exists(file_path):
            print(f'Skipping {file_path} (already downloaded)')
            return

        response = requests.get(file_url, stream=True)

        # Get the file size in bytes
        file_size = int(response.headers.get('Content-Length', 0))

        # Create the file and download the content
        with open(file_path, 'wb') as file:
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='Progress', leave=False) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

    def _get_resource_elements(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find_all(class_='resource-url-analytics')

    def _is_valid_file(self, element):
        file_url = self._get_file_url(element)
        file_name = self._get_file_name(element)

        return (file_url.endswith('.csv')
                and any(str(year) in file_name for year in self.years)
                and all(term.lower() not in file_name.lower() for term in self.ignore))

    def _get_file_url(self, element):
        return urllib.parse.urljoin(self.url, element['href'])

    def _get_file_name(self, element):
        return os.path.join(self.folder_name, element['href'].split('/')[-1])


def extract():
    url = 'https://dados.mj.gov.br/dataset/atendimentos-de-consumidores-nos-procons-sindec'
    folder_name = 'csv_files'
    years = [2019, 2020, 2021, 2022, 2023]
    ignore_list = ['fornecedor']

    extractor = Extract(url, folder_name, years, ignore_list)
    extractor.download_files()


extract()
