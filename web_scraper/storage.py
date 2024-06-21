import pandas as pd
import os
from web_scraper.config import STORAGE_ROOT
from web_scraper.config import S3_BUCKET
import logging
from io import BytesIO
import boto3

print(STORAGE_ROOT)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_to_s3(file_content, bucket_name, s3_path):
    s3 = boto3.client('s3')
    s3.upload_fileobj(file_content, bucket_name, s3_path)
    logger.info(f'File uploaded to s3://{bucket_name}/{s3_path}')

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
        # print (path)
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'Dir created: {path}')

def save_parquet(data,relative_path,filename = None,partitions = None):

    if not relative_path.endswith('/'):
        relative_path = relative_path + '/'
        
    df = pd.DataFrame(data)

    if S3_BUCKET:
        # If there's a S3 bucket, save there
        buffer = BytesIO()
        df.to_parquet(buffer, partition_cols=partitions)
        buffer.seek(0)
        if not filename:
            s3_path = relative_path
        else:
            s3_path = relative_path + filename
        upload_to_s3(buffer, S3_BUCKET, s3_path)
    else:
        # If there's not an S3 bucket, try to save locally 
        if STORAGE_ROOT:
            # If the local path doesn't have a / at the end, add it
            if not STORAGE_ROOT.endswith('/'):
                STORAGE_ROOT = STORAGE_ROOT + '/'

            # If there is no filename, then we use the aprtitions, whith means the full path is the source plus the 
            if not filename:
                full_path = STORAGE_ROOT + relative_path
            else:
                if not filename.endswith('.parquet'):
                    filename = filename + '.parquet'
                full_path = STORAGE_ROOT + relative_path + filename
                
            # Create folder if not exists 
            createDir(full_path)
            
            df.to_parquet(full_path,partition_cols=partitions)
            logger.info(f'Parquet created locally at {full_path}')
        else:
            logger.info(f'There is no local pathnor S3 bucket to store')  
            

    
