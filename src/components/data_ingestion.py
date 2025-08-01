import os
import pandas as pd
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging
from scripts.download_dataset import download_dataset

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            logging.error(e)
    
    def download_kaggle_dataset(self):
        try:
            dataset_path = os.path.dirname(self.data_ingestion_config.feature_file_path)
            download_dataset(dataset_path)
        except Exception as e:
            logging.error(e)
    
    def split_data(self):
        try:
            feature_file_path = self.data_ingestion_config.feature_file_path
            split_ratio = self.data_ingestion_config.train_test_ratio
            
            df = pd.read_csv(feature_file_path)
            
            df.drop(columns=['searchInput/position', 'searchInput/country', 'jobType/1', 'jobType/2', 'jobType/3'], inplace=True)
            df['jobType/0'].fillna(df['jobType/0'].mode()[0], inplace=True)
            df.rename(columns={"jobType/0": "job_type"}, inplace=True)
            
            train_dataset,test_dataset = train_test_split(df, test_size=split_ratio)
            
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
            
            ingest_dir = os.path.dirname(train_file_path)
            os.makedirs(ingest_dir, exist_ok=True)
            
            train_dataset.to_csv(train_file_path, index=False)
            test_dataset.to_csv(test_file_path, index=False)
        except Exception as e:
            logging.error(e)
    
    def initiate_data_ingestion(self):
        try:
            self.download_kaggle_dataset()
            self.split_data()
            
            return DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path,
            )
        except Exception as e:
            logging.error(e)
