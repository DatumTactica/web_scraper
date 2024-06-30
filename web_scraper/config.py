import os
from dotenv import load_dotenv 
load_dotenv() 

START_URL = 'https://www.formula1.com'
STORAGE_ROOT = os.getenv("LOCAL_PATH")
ENV = os.getenv("ENV")
S3_BUCKET = os.getenv("S3_BUCKET")
MIN_YEAR = 2023