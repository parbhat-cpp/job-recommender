import os
import yaml

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataTransformationConfig
from src.entity.config_entity import DataIngestionConfig,DataTransformationConfig
from src.logger import logging

def training_pipeline():
    try:
        training_pipeline_config = TrainingPipelineConfig()
        
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_ingestion_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        
        path_config = {
            'vectorizer': {
                'path': data_transformation_artifact.data_transformer_path
            },
            'vector': {
                'path': data_transformation_artifact.transformed_train_file_path
            },
            'dataset': {
                'path': data_ingestion_artifact.training_file_path
            }
        }
        
        config_file_path = os.path.join(os.getcwd(), "config.yaml")
        with open(config_file_path, "w") as file:
            yaml.dump(path_config, file)
    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    training_pipeline()
