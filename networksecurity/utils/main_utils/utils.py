import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging as logger
import os, sys
import pandas as pd
import numpy as np
import dill
import pickle

def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            content = yaml.safe_load(yaml_file)
        return content
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml(file_path: str, content: object, replace:bool =False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
