from web_scrapper import F1DriversPositions,F1Details,createJSON
import json 
from datetime import datetime

date = datetime.today().strftime('%Y%m%d')

# Get Drivers positions
drivers_positions_url = 'https://www.formula1.com/en/drivers'
drivers_positions = F1DriversPositions(drivers_positions_url)
createJSON(
    'data/drivers/drivers_position_'+date,
    drivers_positions
    )
print("Created drivers positions File")

# Get Drivers details
data = {}
for i in drivers_positions:
    data[i] = F1Details(drivers_positions[i]['driver_link'],drivers_positions[i]['name'])
createJSON(
    'data/drivers/drivers_'+date,
    drivers_positions
    )
print("Created drivers File")
