from web_scraper.config import STORAGE_ROOT
from web_scraper.config import START_URL
from web_scraper.config import MIN_YEAR
from web_scraper.scraper import F1Results
from web_scraper.storage import save_parquet
from datetime import datetime
import numpy as np
import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Get current year
    year = datetime.today().strftime('%Y')

    # Set parent folder 
    data_folder = 'results_drivers'
    
    full_path = STORAGE_ROOT + data_folder

    # Set range of years to process
    years = np.arange(MIN_YEAR,int(year)+1,1)

    # Check if there are any processed results
    if not os.path.exists(full_path) or not os.listdir(full_path):
        # When there are not processed results, process all years
        to_process = years
    else:
        # When there's processed results, get the distinct years that have been processed
        processed = pd.read_parquet(full_path, columns=['year'])['year'].unique()
        # Ensure to reprocess current year
        processed = processed[processed != int(year)]
        # Set the years to process as the difference between what has been pocessed and the expectation
        to_process = np.setdiff1d(years, processed)

    # Get race results
    results_driver = []
    for i in to_process:

        results_driver_url = START_URL + '/en/results.html/'+str(i)+'/drivers.html'
        # Append the year results to the results array
        current_results = F1Results(results_driver_url)
        for j in current_results:
            j['year'] = i
            if 'Pos' in j:
                j['Pos']=str(j['Pos'])
        results_driver.extend(current_results)
        logger.info(f"Gathered driver results from {str(i)}")

    save_parquet(
        data = results_driver,
        relative_path=data_folder,
        partitions=['year']
    )
    
if __name__ == "__main__":
    main()
