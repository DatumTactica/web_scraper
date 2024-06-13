from web_scraper.config import STORAGE_ROOT
from web_scraper.config import START_URL
from web_scraper.scraper import F1Results
from web_scraper.storage import save_parquet
from datetime import datetime
import numpy as np
import os
import pandas as pd


def main():
    # Get current year
    year = datetime.today().strftime('%Y')

    # Set parent folder 
    data_folder = 'results_drivers'
    
    full_path = STORAGE_ROOT + data_folder

    # Set range of years to process
    years = np.arange(2022,int(year)+1,1)

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
    driver_results = []
    for i in to_process:

        driver_results_url = START_URL + '/en/results.html/'+str(i)+'/drivers.html'
        # Append the year results to the results array
        current_results = F1Results(driver_results_url)
        for j in current_results:
            j['year'] = i
        driver_results.extend(current_results)
        print(f"Gathered driver results from {str(i)}")

    save_parquet(
        data = driver_results,
        relative_path=data_folder,
        partitions=['year','Driver']
    )
    
if __name__ == "__main__":
    main()
