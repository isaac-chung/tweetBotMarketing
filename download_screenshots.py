"""
 1. Create a dataset for all the unlabeled data in the app.
 2. Create a dataset version. 
 3. Export the dataset version as protobuf.
 4. Run this script.
 """

import requests

from clarifai.datasets.export.dataset_inputs import DatasetExportReader, InputDownloader

key = ""
metadata = f'Key {key}'

def main():
    local_archive_path = "/Users/isaacchung/Downloads/clarifai-data-protobuf.zip"
    save_path = "output.zip"
    # Create a session object and set auth header
    session = requests.Session()
    session.headers.update({'Authorization': metadata})

    with DatasetExportReader(session=session, local_archive_path=local_archive_path) as reader:
        InputDownloader(session, reader).download_input_archive(save_path=save_path)


if __name__ == '__main__':
    main()