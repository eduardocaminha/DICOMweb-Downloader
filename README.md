# DICOMweb Downloader

## Description
DICOMweb Downloader is a Python script developed by Eduardo Caminha for efficiently downloading DICOM files using a list of accession numbers. The script, leveraging the [dicomweb-client](https://github.com/MGHComputationalPathology/dicomweb-client) library, interacts with DICOMweb servers. It's an invaluable tool for radiologists, researchers, and IT professionals in healthcare. Additionally, this project is in the process of being extended to include a Flask application with a user interface for easier interaction.

## Features
- Download multiple DICOM files using accession numbers.
- Utilizes QIDO-RS and WADO-RS protocols, facilitated by the dicomweb-client library.
- Easy configuration and execution.
- Future integration with a Flask app for a user-friendly interface.

## Installation

### Prerequisites
- Python 3.x
- Access to a DICOMweb server.

### Steps
1. Clone this repository:
git clone [(https://github.com/eduardocaminha/DICOMweb-Downloader.git)]
2. Navigate to the cloned directory:
cd DICOMweb-Downloader
3. Install required dependencies:
pip install -r requirements.txt

## Usage
1. Update the `TXT_FILE_PATH`, `QIDO_URL`, `WADO_URL`, and `AE_TITLE` variables in `DICOMweb_Downloader.py` with your specific configuration details.
2. Place your list of accession numbers in a text file and set its path to `TXT_FILE_PATH`.
3. Execute the script:
python DICOMweb_Downloader.py

## Configuration
Make sure to configure the following variables in the script:
- `DOWNLOAD_FOLDER`: The folder where the DICOM files will be saved.
- `TXT_FILE_PATH`: Path to the text file containing the accession numbers.
- `QIDO_URL`: URL for the QIDO-RS service.
- `WADO_URL`: URL for the WADO-RS service.
- `AE_TITLE`: AE Title of your DICOMweb server.

## Contributing
Contributions to improve DICOMweb Downloader are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License
This project is freely available for use and modification under the MIT License. See the `LICENSE` file for more details.

## Contact
Eduardo Caminha - caminhae@gmail.com
