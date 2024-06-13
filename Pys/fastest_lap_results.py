from web_scrapper import F1Results,F1MinMaxYears,createDir,createDir
import pandas as pd
from datetime import datetime
import os
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import numpy as np
from dotenv import load_dotenv 
load_dotenv() 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get current year
year = datetime.today().strftime('%Y')

# Set parent folder 
data_folder = 'results'

##########################################################################
#                     FASTEST LAP RESULTS                                #
##########################################################################
# Set path
results_path = os.getenv("DESTINTATION_PATH") + data_folder + '/fastest_lap_results'
createDir(results_path)

# Set range of years to process
years = np.arange(2000,int(year)+1,1)

# Check if there are any processed results
if not os.listdir(results_path):
    # When there are not processed results, process all years
    to_process = years
else:
    # When there's processed results, get the distinct years that have been processed
    processed = pd.read_parquet(results_path, columns=['year'])['year'].unique()
    # Ensure to reprocess current year
    processed = processed[processed != int(year)]
    # Set the years to process as the difference between what has been pocessed and the expectation
    to_process = np.setdiff1d(years, processed)
    # print(f'processed:\n{np.sort(processed)}\nto_process\n{np.sort(to_process)}\nyear\n{year}')

# Get race results
fastest_lap_results = []
for i in to_process:

    fastest_lap_results_url = 'https://www.formula1.com/en/results.html/'+str(i)+'/fastest-laps.html'
    # Append the year results to the results array
    current_results = F1Results(fastest_lap_results_url)
    for j in current_results:
        j['year'] = i
        # j['Pos'] = str(j['Pos'])
    fastest_lap_results.extend(current_results)
    logger.info(f"Gathered fastest lap results from {str(i)}")

# Save as data frame
# print(pd.DataFrame(fastest_lap_results)['Pos'])
pd.DataFrame(fastest_lap_results).to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/fastest_lap_results',partition_cols=['year','Driver'])
logger.info('Created files with fastest lap resulsts')