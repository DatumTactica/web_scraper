from web_scrapper import scrapWebF1Positions,scrapWebF1Drivers
import json 
from datetime import datetime

date = datetime.today().strftime('%Y%m%d')

url = 'https://www.formula1.com/en/drivers'
# url = 'https://www.laliga.com/en-GB/leaderboard/all-leaders?stat_competition=laliga-easports&stat=total_goals_ranking'

positions = scrapWebF1Positions(url)
# with open('data/positions'+date+'.json', 'w', encoding='latin-1') as f:
#     json.dump(positions.to_json(orient='values'), f, indent=4, ensure_ascii=False)
# print("Created positions File")
