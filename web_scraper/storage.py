import pandas as pd
import os
from web_scraper.config import STORAGE_ROOT,ENV
import logging
import duckdb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_table_from_dataframe(duckdb_con, table_name):
    duckdb_con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")

def save_local(duckdb_con, table_name, path, partition=None, filename=None):
    createDir(f'{path}{table_name}')
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
    print(query)
    duckdb_con.sql(query)
    logger.info(f"Parquets created at: {path}{table_name}")

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
        # print (path)
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f'Dir created: {path}')

def save_parquet(data,table_name,filename = None,partitions = None):
    # If there's not ENV variable, it should consider it local. 
    env = ENV
    if not env:
        env = 'LOCAL'

    path = STORAGE_ROOT

    df = pd.DataFrame(data)
    duckdb_con = duckdb.connect()
    create_table_from_dataframe(duckdb_con,table_name)

    if filename:
        filename=filename.replace("'","")
        if not filename.endswith('.parquet'):
            filename = filename + '.parquet'

    if env.lower() == 'local':
        save_local(duckdb_con,table_name,path,partitions,filename)
    elif env.lower == 'prd':
        save_s3()
    else:
        logger.error(f'No Environment configured for {env}')

    # dir = full_path = STORAGE_ROOT + relative_path
    # if not filename:
    #     full_path = STORAGE_ROOT + relative_path
    # else:
    #     if not relative_path.endswith('/'):
    #         relative_path = relative_path + '/'
    #     if not filename.endswith('.parquet'):
    #         filename = filename + '.parquet'
    #     full_path = STORAGE_ROOT + relative_path + filename
        

    # pd.DataFrame(data).\
    #     to_parquet(
    #         full_path,
    #         partition_cols=partitions
    #     )
    # logger.info(f'Parquet created at {full_path}')
