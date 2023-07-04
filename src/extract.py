from __future__ import annotations

import urllib.parse
from collections import defaultdict
import os
from typing import List
from bs4 import BeautifulSoup as soup
from requests import exceptions, get
from tqdm import tqdm
from config import dataset_folder_name, dataset_ignore_list, dataset_source_url, dataset_years


class Extract:
    def __init__(self, url: str, folder_name: str, years: List[int], ignore: List[str] | None = None):
        if ignore is None:
            ignore = []
        self.url = url
        self.folder_name = folder_name
        self.years = years
        self.ignore = ignore
        self.total_files = 0

    def count_files_to_download(self) -> int:
        elements = self._get_resource_elements()
        return sum(self._is_valid_file(element) for element in elements)

    def download_files(self) -> None:
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

            year = self._get_year_from_filename(file_name)
            year_count[year] += 1
            count = year_count[year]
            new_file_name = f'{year}_{count}.csv'
            new_file_path = os.path.join(self.folder_name, new_file_name)

            self._download_file(file_url, new_file_path)
            progress_bar.update(1)

        progress_bar.close()

        print('All .csv files downloaded.')

    def _download_file(self, file_url: str, file_path: str) -> None:
        if os.path.exists(file_path):
            print(f'Skipping {file_path} (already downloaded)')
            return
        
        try:
            response = get(file_url, stream=True, timeout=15)
            response.raise_for_status()
            file_size = int(response.headers.get('Content-Length', 0))

            with open(file_path, 'wb') as file:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc='Progress', leave=False) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
        
        except exceptions.RequestException as e:
            print(f'Error downloading file: {file_url}\n   Complete error: {e}')

    def _get_resource_elements(self) -> List[soup]:
        response = get(self.url, timeout=15)
        soup_resp = soup(response.content, 'html.parser')
        return soup_resp.find_all(class_='resource-url-analytics')

    def _is_valid_file(self, element: soup) -> bool:
        file_url = self._get_file_url(element)
        file_name = self._get_file_name(element)

        return (
            file_url.endswith('.csv')
            and any(str(year) in file_name for year in self.years)
            and all(term.lower() not in file_name.lower() for term in self.ignore)
        )

    def _get_file_url(self, element: soup) -> str:
        return urllib.parse.urljoin(self.url, element['href'])

    def _get_file_name(self, element: soup) -> str:
        return os.path.join(self.folder_name, element['href'].split('/')[-1])

    def _get_year_from_filename(self, filename: str) -> int:
        for year in self.years:
            if str(year) in filename:
                return year
        raise ValueError(f'No valid year found in filename: {filename}')


def extract() -> None:
    extractor = Extract(dataset_source_url, dataset_folder_name, dataset_years, dataset_ignore_list)
    extractor.download_files()


extract()
