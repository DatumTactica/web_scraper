from web_scrapper import F1Results,createJSON,F1MinMaxYears
from datetime import datetime
import os

year = datetime.today().strftime('%Y')
# Get min year
processed = os.listdir('data/results')
if len(processed) == 0:
    minYear = 1950
else:
    processed = [int(n) for n in [s[-9:-5] for s in os.listdir('data/results')]]
    if min(processed) > 1950:
        minYear = 1950
    else:
        minYear = max(processed)

# Get race results
for i in range(minYear,int(year)+1):
# i = '2023'
    if i > int(year):
        break
    race_results_url = 'https://www.formula1.com/en/results.html/'+str(i)+'/races.html'
    print(race_results_url)
    race_results = F1Results(race_results_url)
    createJSON(
        'data/results/race_results_'+str(i),
        race_results
        )
    print(f"Created race results File {year}")

