import os
from dotenv import load_dotenv 
load_dotenv() 

START_URL = 'https://www.formula1.com'
STORAGE_ROOT = os.getenv("DESTINTATION_PATH")