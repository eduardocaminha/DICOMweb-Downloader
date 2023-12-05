"""
DICOMweb Downloader
---------------------------
Author: Eduardo Caminha
Description: This script allows downloading multiple dicom files using a list of accession numbers in a text file.
             It works using QIDO-RS and WADO-RS.
"""             

import os
from tqdm import tqdm
from dicomweb_client.api import DICOMwebClient

# User-defined variables
DOWNLOAD_FOLDER = "download" # Folder where the DICOM files will be saved
TXT_FILE_PATH = "accession_numbers.txt" # Path to the text file containing the accession numbers
QIDO_URL = "YOUR QIDO URL" # http://192.168.0.1:800/qido-rs
WADO_URL = "YOUR WADO URL" # http://192.168.0.1:800/wado-rs
AE_TITLE = "YOUR AE TITLE" # AE Title of the DICOMweb server

# Read the accession numbers from the text file
with open(TXT_FILE_PATH, 'r') as file:
    accession_numbers = [line.strip() for line in file.readlines()]

# Set up DICOMwebClient for QIDO-RS
qido_client = DICOMwebClient(url=QIDO_URL, headers={'User-Agent': 'dicomweb-client', 'X-AE-Title': AE_TITLE})

# Set up DICOMwebClient for WADO
wado_client = DICOMwebClient(url=WADO_URL, headers={'User-Agent': 'dicomweb-client', 'X-AE-Title': AE_TITLE})

# Iterate through the accession numbers
for accession_number in tqdm(accession_numbers, desc='Processing studies'):
    # Construct the QIDO URL for retrieving Study Instance UID
    qido_filters = {'AccessionNumber': accession_number}
    study_info = qido_client.search_for_studies(search_filters=qido_filters, get_remaining=True)
    
    if study_info:
        study_instance = study_info[0]['0020000D']['Value'][0]
        print(f"Study Instance UID for Accession Number {accession_number}: {study_instance}")

        # Retrieve and save the DICOM files associated with the Study Instance UID
        dicom_files = wado_client.retrieve_study(study_instance) 
        study_folder = os.path.join(DOWNLOAD_FOLDER, accession_number)
        os.makedirs(study_folder, exist_ok=True)
        
        for i, dicom_data in enumerate(dicom_files):
            output_path = os.path.join(study_folder, f'{accession_number}_{i}.dcm')
            dicom_data.save_as(output_path)

    else:
        print(f"Study not found for Accession Number {accession_number}")

print("Processing complete.")