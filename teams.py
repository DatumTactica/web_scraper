from web_scrapper import F1Details,F1TeamsPositions,createJSON
import json 
from datetime import datetime

date = datetime.today().strftime('%Y%m%d')

# Get teams positions
teams_positions_url = 'https://www.formula1.com/en/teams'
teams_positions = F1TeamsPositions(teams_positions_url)
createJSON(
    'data/teams/teams_positions_'+date,
    teams_positions
    )
print("Created teams positions File")


# Get teams details
data = {}
for i in teams_positions:
    data[i] = F1Details(teams_positions[i]['team_link'],teams_positions[i]['name'])
createJSON(
    'data/teams/teams_'+date,
    teams_positions
    )
print("Created teams File")
# print(teams)
