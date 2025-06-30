from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging as logger
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml, write_yaml
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os, sys

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Reads data from a CSV file and returns it as a Pandas DataFrame.
        Args:
            file_path (str): Path to the CSV file.
        Returns:
            pd.DataFrame: DataFrame containing the data from the CSV file.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e    
    
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config)
            logger.info(f"Expected number of columns: {number_of_columns}, Actual number of columns: {len(df.columns)}")
            if len(df.columns) == number_of_columns:
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    # def is_numeric_column(self, column_name: list) -> bool:
    #     try:
    #         if column_name not in self.schema_config:
    #             return False
    #         return True
                
    #     except Exception as e:
    #         raise NetworkSecurityException(e, sys) from e
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)                
    
    
    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Initiates the data validation process.
        Returns:
            DataValidationArtifact: Artifact containing the results of data validation.
        """
        try:
            logger.info("Starting data validation")
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            ## Load the training and testing data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)
            logger.info("Data loaded successfully for validation")

           ## validate number of columns

            status=self.validate_number_of_columns(df=train_df)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_number_of_columns(df=test_df)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"   
            
            # ## Validate the numeric columns
            # num_col = train_df.select_dtypes(include=[np.number]).columns.tolist()
            
            # num_status = self.is_numeric_column(num_col)
            # if not num_status:
            #     raise NetworkSecurityException(f"Numeric columns in training data {num_col} do not match expected {self.schema_config.numeric_columns}")
            
            # num_col = test_df.select_dtypes(include=[np.number]).columns.tolist()
            # num_status = self.is_numeric_column(num_col)
            # if not num_status:
            #     raise NetworkSecurityException(f"Numeric columns in testing data {num_col} do not match expected {self.schema_config.numeric_columns}")
            
            ## Validate the data drift using KS test
            status= self.detect_dataset_drift(base_df=train_df, current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_dataframe = train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe = test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
        
            data_validation_artifact = DataValidationArtifact(
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
                valid_status=status
            )
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e