from web_scrapper import F1Results,createDir,createDir,F1RaceResultsLinks
import pandas as pd
from datetime import datetime
import os
import pprint 
pp = pprint.PrettyPrinter(indent=4)
import numpy as np
from dotenv import load_dotenv 
load_dotenv() 

# Get current year
year = datetime.today().strftime('%Y')

# Set parent folder 
data_folder = 'results'

##########################################################################
#                               RACE RESULTS                             #
##########################################################################
# Set path
results_path = os.getenv("DESTINTATION_PATH") + data_folder + '/race_results'
createDir(results_path)

# Set range of years to process
years = np.arange(2000,int(year)+1,1)

# Check if there are any processed results
if not os.listdir(results_path):
    # When there are not processed results, process all years
    to_process = years
else:
    # When there's processed results, get the distinct years that have been processed
    processed = pd.to_datetime(pd.read_parquet(results_path, columns=['Date'])['Date']).dt.year.unique()
    # Ensure to reprocess current year
    processed = processed[processed != int(year)]
    # Set the years to process as the difference between what has been pocessed and the expectation
    to_process = np.setdiff1d(years, processed)

# Get race results
race_results = []
for i in to_process:
    race_results_url = 'https://www.formula1.com/en/results.html/'+str(i)+'/races.html'
    # Append the year results to the results array
    current_results = F1Results(race_results_url,'Grand Prix')
    race_results.extend(current_results)
    print(f"Gathered race results from {str(i)}")
    gp_race_results = []
    for j in current_results:
        gp_url = f"https://www.formula1.com/{j['Grand Prix_link']}"
        # race
        gp_race_results = F1Results(gp_url)
        for k in gp_race_results:
            k['date'] = j['Date']
            k['gp'] = j['Grand Prix']
        # gp_race_results.extend(gp_race_current_results)
        dir = os.getenv("DESTINTATION_PATH") + data_folder + '/gp_race_results/'
        createDir(dir)
        pd.DataFrame(gp_race_results).to_parquet(dir + j['Grand Prix'].replace(' ','').lower() + j['Date'].replace(' ','').lower() + '.parquet')

        # Get available links
        aval_links = F1RaceResultsLinks(gp_url)
        aval_links.pop('Race result', None)
        # print(aval_links) 
        gp_race_results = []
        for link in aval_links:
            gp_url = f'https://www.formula1.com/{aval_links[link]}'
            gp_race_results = F1Results(gp_url)
            # print(pd.DataFrame(gp_race_results))
            for k in gp_race_results:
                k['date'] = j['Date']
                k['gp'] = j['Grand Prix']
                if 'Pos' in k:
                    k['Pos'] = str(k['Pos'])

            dir = os.getenv("DESTINTATION_PATH") + data_folder + '/gp_' + link.replace(' ','_').lower() + '_results/'
            createDir(dir)
            pd.DataFrame(gp_race_results).to_parquet(dir + j['Grand Prix'].replace(' ','').lower() + j['Date'].replace(' ','').lower() + '.parquet')
            print(f"Created {link} file for {j['Grand Prix']} on {j['Date']}")

# Save as data frame
pd.DataFrame(race_results).to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/race_results',partition_cols=['Winner','Grand Prix'])
print('Created file with race resulsts')

