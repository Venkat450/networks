from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging as logger
from networksecurity.entity.artifact_entity import DataIngestionArtifact

## configuration for data ingestion component

from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from typing import List
from dotenv import load_dotenv
load_dotenv()   

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Retrieves data from MongoDB collection and exports it as a Pandas DataFrame.
        Returns:
            pd.DataFrame: DataFrame containing the data from the MongoDB collection.       
        
        """
        try:
            logger.info("Exporting collection to DataFrame")
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            df= pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], axis=1, inplace=True)
                
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
        
    def export_data_to_feature_store(self, df: pd.DataFrame) -> None:
        """
        Exports the DataFrame to a feature store file.
        Args:
            df (pd.DataFrame): DataFrame to be exported.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #create directory if it does not exist
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            df.to_csv(feature_store_file_path, index=False, header=True)
            logger.info(f"Data exported to feature store at {feature_store_file_path}")
            return df
        
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    def split_data_as_train_test(self, df: pd.DataFrame) -> List[pd.DataFrame]:
        """
        Splits the DataFrame into training and testing sets.
        Args:
            df (pd.DataFrame): DataFrame to be split.
        Returns:
            List[pd.DataFrame]: List containing training and testing DataFrames.
        """
        try:
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            logger.info("Performed train-test split on the DataFrame")
            
            logger.info("Exited split_data_as_train_test method of Data_Ingestion class")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logger.info("Exporting train and test file paths")
            train_df.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_df.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logger.info(f"Train and test data exported to {self.data_ingestion_config.training_file_path} and {self.data_ingestion_config.testing_file_path}")  
            
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    
    def initiate_data_ingestion(self) -> pd.DataFrame:
        try:
            logger.info("Starting data ingestion process")
            dataframe = self.export_collection_as_dataframe()
            logger.info("Data exported from MongoDB collection successfully")
            dataframe = self.export_data_to_feature_store(dataframe)
            logger.info("Data exported to feature store successfully")
            self.split_data_as_train_test(dataframe)
            logger.info("Data split into training and testing sets successfully")
            dataingestionartifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            
            return dataingestionartifact        
   
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e