import logging
import os
from datetime import datetime

LOG_FILE= f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"  # Log file name with timestamp

logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)  # Directory for logs
os.makedirs(logs_path, exist_ok=True)  # Create logs directory if it doesn't exist


LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)  # Full path to the log file

logging.basicConfig(
    filename=LOG_FILE_PATH, # Log file path
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # Set the logging level to INFO
)