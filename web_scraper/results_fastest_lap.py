from web_scraper.config import START_URL,MIN_YEAR
from web_scraper.functions import years_to_process
from web_scraper.scraper import F1Results
from web_scraper.storage import save_parquet
from datetime import datetime
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set parent folder 
table_name = 'results_fastest_lap'

def main():
    # Get current year
    year = datetime.today().strftime('%Y')

    # Set range of years to process
    years = np.arange(MIN_YEAR,int(year)+1,1)
    
    # When there's processed results, get the distinct years that have been processed
    to_process = years_to_process(table_name,years,year)
    
    # Get race results
    fastest_lap_results = []
    for i in to_process:

        fastest_lap_results_url = START_URL + '/en/results.html/'+str(i)+'/fastest-laps.html'
        # Append the year results to the results array
        current_results = F1Results(fastest_lap_results_url)
        for j in current_results:
            j['year'] = i
            if 'Pos' in j:
                j['Pos']=str(j['Pos'])
        fastest_lap_results.extend(current_results)
        logger.info(f"Gathered fastest-laps results from {str(i)}")

    save_parquet(
        data = fastest_lap_results,
        table_name=table_name,
        partitions=['year']
    )
   
if __name__ == "__main__":
    main()
