from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data Ingestion Artifact class to hold the data ingestion related artifacts.
    """
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """
    Data Validation Artifact class to hold the data validation related artifacts.
    """
    valid_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    
@dataclass
class DataTransformationArtifact:
    """
    Data Transformation Artifact class to hold the data transformation related artifacts.
    """
    transformed_train_file_path: str
    transformed_test_file_path: str
    transformed_object_file_path: str
