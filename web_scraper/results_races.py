from web_scraper.config import STORAGE_ROOT
from web_scraper.config import START_URL
from web_scraper.scraper import F1Results,F1RaceResultsLinks
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
    data_folder = 'results_races'
    gp_data_folder = 'gp_results_races'
    
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
    results_races = []
    for i in to_process:

        results_races_url = START_URL + '/en/results.html/'+str(i)+'/races.html'
        # Append the year results to the results array
        current_results = F1Results(results_races_url,'Grand Prix')
        
        results_races.extend(current_results)
        
        logger.info(f"Gathered driver results from {str(i)}")

        # Define link for each GP results 
        results_races_gp = []
        for result in current_results:
            result['year'] = i
            gp_url = f"{START_URL}/{result['Grand Prix_link']}"
            current_results_gp = F1Results(gp_url)
            # print(current_results_gp)
            for result_gp in current_results_gp:
                result_gp['date'] = result['Date']
                result_gp['gp'] = result['Grand Prix']
                result_gp['year'] = i
                if 'Pos' in result_gp:
                    result_gp['Pos']=str(result_gp['Pos'])
                # print(result_gp['Pos'] )
            results_races_gp.extend(current_results_gp)
            
            # Get available links
            aval_links = F1RaceResultsLinks(gp_url)
            aval_links.pop('Race result', None)
            
            for link in aval_links:
                gp_url = f"{START_URL}/{aval_links[link]}"
                sub_results_races_gp = F1Results(gp_url)
                for sub_result in sub_results_races_gp:
                    sub_result['date'] = result['Date']
                    sub_result['gp'] = result['Grand Prix']
                    sub_result['year'] = i
                    if 'Pos' in sub_result:
                        sub_result['Pos'] = str(sub_result['Pos'])
                filename = f"{result['Grand Prix'].replace(' ','').lower()}{i}"
                gp_sub_data_folder = f"gp_{link.replace(' ','_').lower()}"
                save_parquet(
                    data = sub_results_races_gp,
                    relative_path=gp_sub_data_folder,
                    filename=filename
                )


            # break
        save_parquet(
            data = results_races_gp,
            relative_path=gp_data_folder,
            # filename='test'
            partitions=['date','gp']
        )

    save_parquet(
        data = results_races,
        relative_path=data_folder,
        partitions=['year','Grand Prix']
    )
    
if __name__ == "__main__":
    main()
