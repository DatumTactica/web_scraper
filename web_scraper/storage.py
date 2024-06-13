import pandas as pd
import os
from web_scraper.config import STORAGE_ROOT

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
    print(f'Parquet created at {relative_path}')

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
        # print (path)
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'Dir created: {path}')
