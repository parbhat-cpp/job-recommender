from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    training_file_path: str
    testing_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    data_transformer_path: str
