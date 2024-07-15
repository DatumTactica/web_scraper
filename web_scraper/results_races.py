from web_scraper.config import START_URL,MIN_YEAR
from web_scraper.functions import years_to_process
from web_scraper.scraper import F1Results,F1RaceResultsLinks
from web_scraper.storage import save_parquet
from datetime import datetime
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set parent folder 
table_name = 'results_races'
gp_table_name = 'gp_results_races'

def main():
    # Get current year
    year = datetime.today().strftime('%Y')

    # Set range of years to process
    years = np.arange(MIN_YEAR,int(year)+1,1)
    
    # When there's processed results, get the distinct years that have been processed
    to_process = years_to_process(table_name,years,year)

    # Get race results
    results_races = []
    for i in to_process:

        results_races_url = START_URL + '/en/results.html/'+str(i)+'/races.html'
        # Append the year results to the results array
        current_results = F1Results(results_races_url,'Grand Prix')
        for j in current_results:
            j['year'] = i
        
        results_races.extend(current_results)
        
        logger.info(f"Gathered race results from {str(i)}")

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
                if 'PTS' in result_gp:
                    result_gp['PTS']=float(result_gp['PTS'])
                # print(result_gp['Pos'] )
            results_races_gp.extend(current_results_gp)
            
            # Get available links
            aval_links = F1RaceResultsLinks(gp_url)
            aval_links.pop('Race result', None)
            # print(aval_links)
            logger.info(f"Gathering results from {result['Grand Prix']} - {i}")
            for link in aval_links:
                gp_url = f"{START_URL}/{aval_links[link]}"
                sub_results_races_gp = F1Results(gp_url)
                for sub_result in sub_results_races_gp:
                    sub_result['date'] = result['Date']
                    sub_result['gp'] = result['Grand Prix']
                    sub_result['year'] = i
                    if 'Pos' in sub_result:
                        sub_result['Pos'] = str(sub_result['Pos'])
                    if 'Time' in sub_result:
                        sub_result['Time'] = str(sub_result['Time'])
                filename = f"{result['Grand Prix'].replace(' ','').lower()}{i}"
                gp_sub_table_name = f"gp_{link.replace(' ','_').lower()}"
                # print(gp_url)
                save_parquet(
                    data = sub_results_races_gp,
                    table_name=gp_sub_table_name,
                    # partitions=['year']
                    filename=filename
                )
        save_parquet(
            data = results_races_gp,
            table_name=gp_table_name,
            partitions=['year']
        )
    save_parquet(
        data = results_races,
        table_name=table_name,
        partitions=['year']
    )
    
if __name__ == "__main__":
    main()
