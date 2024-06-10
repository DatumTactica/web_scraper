from web_scrapper import F1DriversPositions,F1Details,createDir
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv 
load_dotenv() 

date = datetime.today().strftime('%Y%m%d')
data_folder = 'drivers'
# Get Drivers positions
drivers_positions_url = 'https://www.formula1.com/en/drivers'
drivers_positions = F1DriversPositions(drivers_positions_url)
# print(os.getenv("DESTINTATION_PATH") + '/data/drivers')
createDir(os.getenv("DESTINTATION_PATH") + data_folder)
pd.DataFrame.from_dict(drivers_positions,orient='index').to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/drivers_position_'+date)
print("Created drivers positions File")

# Get Drivers details
data = {}
for i in drivers_positions:
    data[i] = F1Details(drivers_positions[i]['driver_link'],drivers_positions[i]['name'])
# print(pd.DataFrame.from_dict(data,orient='index'))
pd.DataFrame.from_dict(data,orient='index').to_parquet(os.getenv("DESTINTATION_PATH") + data_folder + '/drivers_'+date)
print("Created drivers File")
