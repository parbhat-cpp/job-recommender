import os
from datetime import datetime

import src.constants as const

class TrainingPipelineConfig:
    def __init__(self, timestamp = datetime.now() ) -> None:
        timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.artifact_dir = const.ARTIFACT_DIR
        self.artifact_path = os.path.join(self.artifact_dir, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        self.artifact_dir = os.path.join(
            training_pipeline_config.artifact_path,
            const.DATA_INGESTION_DIR_NAME,
        )
        self.feature_file_path = os.path.join(
            self.artifact_dir,
            const.DATA_INGESTION_FEATURE_STORE,
            const.FILE_NAME,
        )
        self.training_file_path = os.path.join(
            self.artifact_dir,
            const.DATA_INGESTION_INGESTED,
            const.TRAIN_FILE_NAME,
        )
        self.testing_file_path = os.path.join(
            self.artifact_dir,
            const.DATA_INGESTION_INGESTED,
            const.TEST_FILE_NAME,
        )
        self.train_test_ratio = const.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_path,
            const.DATA_TRANSFORMATION_DIR_NAME,
        )
        self.transformed_train_file_path = os.path.join(
            self.data_transformation_dir,
            const.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            const.DATA_TRANSFORMATION_TRAIN_FILE_NAME,
        )
        self.transformed_test_file_path = os.path.join(
            self.data_transformation_dir,
            const.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
            const.DATA_TRANSFORMATION_TEST_FILE_NAME,
        )
        self.data_transformer_path = os.path.join(
            self.data_transformation_dir,
            const.DATA_TRANSFORMATION_TRANSFORMER_MODEL_DIR,
            const.DATA_TRANSFORMATION_MODEL_NAME,
        )
