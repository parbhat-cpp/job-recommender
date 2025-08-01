import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

from src.logger import logging
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.entity.artifact_entity import DataTransformationArtifact

from src.utils import preprocess_text,save_numpy_array,save_object

class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_transformation_config: DataTransformationConfig) -> None:
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_config = data_transformation_config
    
    def generate_tags(self) -> tuple[pd.DataFrame, pd.DataFrame] | None:
        try:
            train_df_path = self.data_ingestion_artifact.training_file_path
            test_df_path = self.data_ingestion_artifact.testing_file_path
            
            train_df = pd.read_csv(train_df_path)
            test_df = pd.read_csv(test_df_path)
            
            train_df['tags'] = train_df['positionName'] + train_df['location'] + train_df['description'] + train_df['job_type']
            test_df['tags'] = test_df['positionName'] + test_df['location'] + test_df['description'] + test_df['job_type']
            
            train_df['tags'] = train_df['tags'].apply(lambda x:x.lower())
            test_df['tags'] = test_df['tags'].apply(lambda x:x.lower())
            
            train_df['tags'] = train_df['tags'].apply(preprocess_text)
            test_df['tags'] = test_df['tags'].apply(preprocess_text)
            
            return train_df, test_df
        except Exception as e:
            logging.error(e)
    
    def apply_vectorization(self, train_df: pd.DataFrame, test_df: pd.DataFrame):
        try:
            X_train = train_df['tags'].apply(lambda x: " ".join(x))
            X_test = test_df['tags'].apply(lambda x: " ".join(x))
            
            y_train = np.array(X_train.index.tolist()).reshape(1,-1)
            y_test = np.array(X_test.index.tolist()).reshape(1,-1)
            
            vectorizer = CountVectorizer()
            X_train_vector = vectorizer.fit_transform(X_train)
            X_test_vector = vectorizer.transform(X_test)
            
            save_numpy_array(
                self.data_transformation_config.transformed_train_file_path,
                X_train_vector,
            )
            save_numpy_array(
                self.data_transformation_config.transformed_test_file_path,
                X_test_vector,
            )
            save_object(
                self.data_transformation_config.data_transformer_path,
                vectorizer
            )
        except Exception as e:
            logging.error(e)
    
    def initiate_data_transformation(self):
        try:
            train_df, test_df = self.generate_tags()
            self.apply_vectorization(train_df, test_df)
            
            return DataTransformationArtifact(
                data_transformer_path=self.data_transformation_config.data_transformer_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
        except Exception as e:
            logging.error(e)
