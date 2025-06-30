from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging as logger
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.components.model_trainer import ModelTrainer
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
        logger.info("Data Ingestion Pipeline Completed Successfully")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logger.info("Data Validation Artifact Created Successfully")
        
        data_transformation_config = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact,
                                                data_transformation_config)
        logger.info("Starting Data Transformation Pipeline")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logger.info("Data Transformation Artifact Created Successfully")
        print(data_transformation_artifact)
        logger.info("Data Transformation Pipeline Completed Successfully")
        
        logger.info("Model Trainer Pipeline Started")
        model_trainer_config = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                      model_trainer_config=model_trainer_config)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        logger.info("Model Trainer Artifact Created Successfully")
        print(model_trainer_artifact)
        logger.info("Model Trainer Pipeline Completed Successfully")
        
        
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e