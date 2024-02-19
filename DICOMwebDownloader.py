"""
DICOMweb Downloader
---------------------------
Author: Eduardo Caminha
Description: This script allows downloading multiple dicom files using a list of accession numbers in a text file.
             It works using QIDO-RS and WADO-RS.

Update: Eduardo Farina performed and updated version to make it faster and handle PACS limitation.
"""             

import os
from tqdm import tqdm
from dicomweb_client.api import DICOMwebClient
import concurrent.futures
import time

# User-defined variables
DOWNLOAD_FOLDER = "/data/download_jpr"
TXT_FILE_PATH = "num_pedido.txt"
QIDO_URL = "http://172.22.66.186:10080/qido-rs"
WADO_URL = "http://172.22.66.186:12080/wado-rs"
AE_TITLE = "SynapseWadoSCU"

def chunk_list(lst, chunk_size):
    """Yield successive chunk_size chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def download_studies(accession_numbers_chunk, progress=None):
    """Process each chunk of accession numbers."""
    for accession_number in accession_numbers_chunk:
        download_study(accession_number)
    if progress:
        progress.update(1)

def download_study(accession_number, max_retries=5, wait_time=60):
    study_folder = os.path.join(DOWNLOAD_FOLDER, accession_number)
    if os.path.exists(study_folder) and os.path.isdir(study_folder):
        print(f"Study folder for Accession Number {accession_number} already exists. Skipping download.")
        return

    attempt = 0
    while attempt < max_retries:
        try:
            qido_filters = {'AccessionNumber': accession_number}
            study_info = qido_client.search_for_studies(search_filters=qido_filters, get_remaining=True)

            if study_info:
                study_instance = study_info[0]['0020000D']['Value'][0]
                print(f"Study Instance UID for Accession Number {accession_number}: {study_instance}")

                dicom_files = wado_client.retrieve_study(study_instance)
                os.makedirs(study_folder, exist_ok=True)

                for i, dicom_data in enumerate(dicom_files):
                    output_path = os.path.join(study_folder, f'{accession_number}_{i}.dcm')
                    dicom_data.save_as(output_path)
                return
            else:
                print(f"Study not found for Accession Number {accession_number}")
                return
        except Exception as e:
            print(f"Error downloading study for Accession Number {accession_number}: {e}")
            attempt += 1
            print(f"Attempt {attempt}/{max_retries}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2

# Read the accession numbers from the text file
with open(TXT_FILE_PATH, 'r') as file:
    accession_numbers = [line.strip() for line in file.readlines()]

# Split the accession numbers into chunks of 20
accession_numbers_chunks = list(chunk_list(accession_numbers, 20))

# Set up DICOMwebClient instances
qido_client = DICOMwebClient(url=QIDO_URL, headers={'User-Agent': 'dicomweb-client', 'X-AE-Title': AE_TITLE})
wado_client = DICOMwebClient(url=WADO_URL, headers={'User-Agent': 'dicomweb-client', 'X-AE-Title': AE_TITLE})

# Initialize the progress bar
progress = tqdm(total=len(accession_numbers_chunks), desc='Processing chunks')

# Use ThreadPoolExecutor to process chunks of accession numbers in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(download_studies, chunk, progress) for chunk in accession_numbers_chunks]
    concurrent.futures.wait(futures)

# Close the progress bar
progress.close()

print("Processing complete.")