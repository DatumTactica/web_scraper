import pandas as pd
import os
from web_scraper.config import STORAGE_ROOT,ENV,S3_BUCKET
import logging
import duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_table_from_dataframe(duckdb_con, table_name):
    duckdb_con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")

def save(duckdb_con, table_name, path, partition=None, filename=None):
    if partition:
        partitions= f""", PARTITION_BY ({', '.join(f"'{item}'" for item in partition)}), OVERWRITE_OR_IGNORE 1"""
        filename = ''
    else:
        partitions = ''
        # filename = f'/{filename}'
    query = f"""
        COPY (
            SELECT * 
            FROM {table_name}
        ) 
        TO '{path}{table_name}/{filename}' 
        (FORMAT PARQUET{partitions});
    """
    # print('test')
    # print(query)
    duckdb_con.sql(query)
    logger.info(f"Parquets created at: {path}{table_name}")

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
        # print (path)
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'Dir created: {path}')

def save_local(table_name,duckdb_con,partitions,filename):
    path = STORAGE_ROOT
    createDir(f'{path}{table_name}')
    save(duckdb_con,table_name,path,partitions,filename)
    
def save_s3(table_name,duckdb_con,partitions,filename):
    path = S3_BUCKET
    duckdb_con.sql(f"CALL load_aws_credentials();")
    save(duckdb_con,table_name,path,partitions,filename)    

def save_parquet(data,table_name,filename = None,partitions = None):
    # If there's not ENV variable, it should consider it local. 
    env = ENV
    if not env:
        env = 'LOCAL'

    df = pd.DataFrame(data)
    duckdb_con = duckdb.connect()
    create_table_from_dataframe(duckdb_con,table_name)

    if filename:
        filename=filename.replace("'","")
        if not filename.endswith('.parquet'):
            filename = filename + '.parquet'

    if env.lower() == 'local':
        save_local(table_name,duckdb_con,partitions,filename)
    elif env.lower() == 'prd':
        save_s3(table_name,duckdb_con,partitions,filename)
    else:
        logger.error(f'No Environment configured for {env}')
        return
    

