import os
from dotenv import load_dotenv
load_dotenv()

import kaggle

DATASET = os.getenv('DATASET')

def download_dataset(path = 'datasets'):
    kaggle_api = kaggle.api
    kaggle_api.authenticate()
    kaggle_api.dataset_download_files(DATASET, os.path.join(os.getcwd(), path), unzip=True)

if __name__ == '__main__':
    download_dataset()
