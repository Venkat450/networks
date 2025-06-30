from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os,sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def predict(self, X):
        """
        Predict the output using the preprocessor and model.
        
        :param X: Input data for prediction
        :return: Predicted output
        """
        try:
            x_transform = self.preprocessor.transform(X)
            return self.model.predict(x_transform)
        except Exception as e:
            raise NetworkSecurityException(e, sys)