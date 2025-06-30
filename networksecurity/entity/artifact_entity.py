from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data Ingestion Artifact class to hold the data ingestion related artifacts.
    """
    train_file_path: str
    test_file_path: str
