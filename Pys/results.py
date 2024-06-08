from web_scrapper import F1Results,F1MinMaxYears,createDir,createDir
import pandas as pd
from datetime import datetime
import os
import pathlib
from pathlib import Path
import pprint 
pp = pprint.PrettyPrinter(indent=4)
from dotenv import load_dotenv 
load_dotenv() 

year = datetime.today().strftime('%Y')
data_folder = 'results'
# Get min year
results_path = os.getenv("DESTINTATION_PATH") + data_folder
# print(results_path)
createDir(os.getenv("DESTINTATION_PATH") + data_folder)
processed = os.listdir(results_path)
if len(processed) == 0:
    minYear = 1950
else:
    processed = [int(n) for n in [s[-4:] for s in os.listdir(results_path)]]
    if min(processed) > 1950:
        minYear = 1950
    else:
        minYear = max(processed)

# Get race results
race_results = []
# for i in range(minYear,int(year)+1):
for i in range(2023,2025):
    if i > int(year):
        break
    race_results_url = 'https://www.formula1.com/en/results.html/'+str(i)+'/races.html'
    race_results.extend(F1Results(race_results_url))
    # print(race_results)
    print(f"Gathered data from {str(i)}")
pd.DataFrame(race_results).to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/race_results',partition_cols=['Winner','Grand Prix'])
print('Created file with resulsts')