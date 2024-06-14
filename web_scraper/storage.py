import pandas as pd
import os
from web_scraper.config import STORAGE_ROOT
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_parquet(data,relative_path,filename = None,partitions = None):

    dir = full_path = STORAGE_ROOT + relative_path
    if not filename:
        full_path = STORAGE_ROOT + relative_path
    else:
        if not relative_path.endswith('/'):
            relative_path = relative_path + '/'
        if not filename.endswith('.parquet'):
            filename = filename + '.parquet'
        full_path = STORAGE_ROOT + relative_path + filename
        
    # Create folder if not exists 
    createDir(dir)

    pd.DataFrame(data).\
        to_parquet(
            full_path,
            partition_cols=partitions
        )
    logger.info(f'Parquet created at {full_path}')

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
        # print (path)
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'Dir created: {path}')
