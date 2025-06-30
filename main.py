from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging as logger
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig= TrainingPipelineConfig()
        dataingestionconfig= DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        dataingestion = DataIngestion(data_ingestion_config=dataingestionconfig)
        logger.info("Starting Data Ingestion Pipeline")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logger.info("Data Ingestion Artifact Created Successfully")
        print(dataingestionartifact)
        datavalidationconfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation= DataValidation(data_validation_config=datavalidationconfig,data_ingestion_artifact=dataingestionartifact)
        logger.info("Starting Data Validation Pipeline")
        data_validation.initiate_data_validation()
        logger.info("Data Ingestion Pipeline Completed Successfully")
        data_validation_artifact=DataValidation(dataingestionconfig, datavalidationconfig)
        print(data_validation_artifact)
        logger.info("Data Validation Artifact Created Successfully")
        
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e