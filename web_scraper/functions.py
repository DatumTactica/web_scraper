import duckdb, numpy as np, logging
from web_scraper.config import ENV,S3_BUCKET,STORAGE_ROOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_local(duck_con,table_name):
    full_path = STORAGE_ROOT + table_name
    processed = check_files(duck_con,full_path)
    return processed

def get_s3(duck_con,table_name):
    full_path = S3_BUCKET + table_name
    duck_con.sql(f"CALL load_aws_credentials();")
    processed = check_files(duck_con,full_path)
    return processed

def check_files(duck_con,full_path):
    try:
        duck_con.read_parquet(f'{full_path}/**')
        df = duck_con.read_parquet(f'{full_path}/**').fetchdf()
        processed_df = duck_con.execute("select distinct year from df").fetchdf()
        processed = processed_df['year'].to_list()
        return processed
    except:
        return []


def get_processed(table_name):
    """
    You want to determine IF you will check it locally or in the S3 bucket
    with that, you will define the variables to check the respective repository 
    Then, you will  get the list of years that have been processed
    """    
    # Set the variable for the environment
    env = ENV
    if not env:
        env = 'LOCAL'
        
    # Create a duckdb connection  
    duck_con = duckdb.connect()
    
    processed = []
    # if you are in local, check the files in local
    if env.lower() == 'local':
        processed = get_local(duck_con,table_name)
    # if you are in prd, check the files in s3
    elif env.lower() == 'prd':
        processed = get_s3(duck_con,table_name)
    # else, raise an error
    else:
        logger.error(f'No Environment configured for {env}')
        return
    return processed

def years_to_process(table_name,years,year):
    """
    You want to get a list of the `processed` years of the table `table_name` 
    with that, you are going to cross it with the `years` that are supposed to be porcessed to get the list of years pending `to_process`
    last but not least, you are going to make sure to add the current `year` to have te most updated data
    """
    # Get the list of processed years 
    processed = get_processed(table_name)
    # Remove from the processed years the current year

    if int(year) in processed:
        processed.remove(int(year))
    # processed = processed[processed != int(year)]

    # Set the years to process as the difference between what has been pocessed and the expectation
    to_process = np.setdiff1d(years, processed)
    return to_process
