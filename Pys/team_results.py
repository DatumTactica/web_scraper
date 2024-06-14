from web_scrapper import F1Results,F1MinMaxYears,createDir,createDir
import pandas as pd
from datetime import datetime
import os
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
#                            TEAM RESULTS                                #
##########################################################################
# Set path
results_path = os.getenv("DESTINTATION_PATH") + data_folder + '/team_results'
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
team_results = []
for i in to_process:

    team_results_url = 'https://www.formula1.com/en/results.html/'+str(i)+'/team.html'
    # Append the year results to the results array
    current_results = F1Results(team_results_url)
    for j in current_results:
        j['year'] = i
        j['Pos'] = str(j['Pos'])
    team_results.extend(current_results)
    logger.info(f"Gathered team results from {str(i)}")

# Save as data frame
# print(pd.DataFrame(team_results)['Pos'])
pd.DataFrame(team_results).to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/team_results',partition_cols=['year','Team'])
logger.info('Created file with team resulsts')