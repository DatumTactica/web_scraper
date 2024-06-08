from web_scrapper import F1Details,F1TeamsPositions,createDir
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv 
load_dotenv() 

date = datetime.today().strftime('%Y%m%d')
data_folder = 'teams'

# Get teams positions
teams_positions_url = 'https://www.formula1.com/en/teams'
teams_positions = F1TeamsPositions(teams_positions_url)
createDir(os.getenv("DESTINTATION_PATH") + data_folder)
pd.DataFrame.from_dict(teams_positions,orient='index').to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/teams_position_'+date)
print("Created teams positions File")


# Get teams details
data = {}
for i in teams_positions:
    data[i] = F1Details(teams_positions[i]['team_link'],teams_positions[i]['name'])
pd.DataFrame.from_dict(data,orient='index').to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/teams_'+date)
print("Created teams File")
# print(teams)


