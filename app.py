from web_scrapper import F1DriversPositions,F1Details,F1TeamsPositions
import json 
from datetime import datetime
import pandas as pd

date = datetime.today().strftime('%Y%m%d')

# Get positions positions
drivers_positions_url = 'https://www.formula1.com/en/drivers'
drivers_positions = F1DriversPositions(drivers_positions_url)
with open('data/drivers_positions'+date+'.json', 'w', encoding='latin-1') as f:
    json.dump(drivers_positions, f, indent=4, ensure_ascii=False)
print("Created drivers positions File")
# print(drivers_positions)
# Get Drivers details
data = {}
for i in drivers_positions:
    data[i] = F1Details(drivers_positions[i]['driver_link'],drivers_positions[i]['name'])
with open('data/drivers_'+date+'.json', 'w', encoding='latin-1') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
print("Created drivers File")

# Get teams positions
teams_positions_url = 'https://www.formula1.com/en/teams'
teams_positions = F1TeamsPositions(teams_positions_url)
with open('data/teams_positions'+date+'.json', 'w', encoding='latin-1') as f:
    json.dump(teams_positions, f, indent=4, ensure_ascii=False)
print("Created teams positions File")


# Get teams details
data = {}
for i in teams_positions:
    data[i] = F1Details(teams_positions[i]['team_link'],teams_positions[i]['name'])
with open('data/teams_'+date+'.json', 'w', encoding='latin-1') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
print("Created teams File")
# print(teams)
