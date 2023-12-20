"""
 1. Create a dataset for all the unlabeled data in the app.
 2. Create a dataset version.
 3. Export the dataset version as protobuf.
 4. Run this script.
 """

import requests

# from clarifai.client.dataset import Dataset
from helper import DatasetExportReader, InputAnnotationDownloader

def main():
    # d = Dataset(url='https://clarifai.com/Isaac/q4-tweet-screenshots/datasets/20231219')
    local_archive_path = "/Users/isaacchung/Downloads/clarifai-data-protobuf.zip"
    save_path = "output.zip"

    session = requests.Session()
    session.headers.update({'Authorization': 'Key PAT'})
    with DatasetExportReader(
        session=session, local_archive_path=local_archive_path) as reader:
      InputAnnotationDownloader(session, reader, 4).download_archive(
          save_path=save_path, split='all')

    # d.export(save_path=save_path, local_archive_path=local_archive_path)


if __name__ == '__main__':
    main()
