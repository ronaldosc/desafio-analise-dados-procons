from __future__ import annotations

import os
import urllib.parse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

url = 'https://dados.mj.gov.br/dataset/atendimentos-de-consumidores-nos-procons-sindec'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all elements with class="resource-url-analytics"
elements = soup.find_all(class_='resource-url-analytics')

# Create a directory to store the downloaded files
folder_name = 'csv_files'
os.makedirs(folder_name, exist_ok=True)

# List of years to filter the files
years = [2019, 2020, 2021, 2022, 2023]

# Files to ignore (exclude)
ignore = ['fornecedor']

# Total number of files to download
total_files = 0

# Count the total number of files to download
for element in elements:
    file_url = urllib.parse.urljoin(url, element['href'])
    file_name = os.path.join(folder_name, element['href'].split('/')[-1])

    if (
        file_url.endswith('.csv')
        and any(str(year) in file_name for year in years)
        and all(term.lower() not in file_name.lower() for term in ignore)
    ):
        total_files += 1

# Iterate through the elements and download the .csv files from 2019 to 2023
progress_bar = tqdm(total=total_files, unit='file')

for element in elements:
    file_url = urllib.parse.urljoin(url, element['href'])
    file_name = os.path.join(folder_name, element['href'].split('/')[-1])

    if (
        file_url.endswith('.csv')
        and any(str(year) in file_name for year in years)
        and all(term.lower() not in file_name.lower() for term in ignore)
    ):
        if os.path.exists(file_name):
            print(f'Skipping {file_name} (already downloaded)')
        else:
            progress_bar.set_description(f'Downloading {file_name}')
            response = requests.get(file_url, stream=True)

            # Get the file size in bytes
            file_size = int(response.headers.get('Content-Length', 0))

            # Create the file and download the content
            with open(file_name, 'wb') as file:
                with tqdm(
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    desc='Progress',
                    leave=False,
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))

        progress_bar.update(1)

progress_bar.close()

print('All .csv files downloaded.')
