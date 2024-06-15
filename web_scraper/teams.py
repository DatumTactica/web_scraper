from web_scraper.config import STORAGE_ROOT
from web_scraper.config import START_URL
from web_scraper.scraper import F1TeamsPositions,F1Details
from web_scraper.storage import save_parquet
from datetime import datetime

def main():
    # Get current date
    date = datetime.today().strftime('%Y%m%d')

    # Set parent folder 
    data_folder = 'teams_positions'

    teams_positions_url = START_URL + '/en/teams'
    # Get race results
    teams = F1TeamsPositions(teams_positions_url)
    teams_list = list(teams.values()) 
    
    save_parquet(
        data = teams_list,
        relative_path=data_folder,
        filename=data_folder + '_' + date
    )

    # Set parent folder 
    data_folder = 'teams'

    data = {}
    for i in teams:
        data[i] = F1Details(teams[i]['team_link'],teams[i]['name'])

    data_list = list(data.values())

    save_parquet(
        data = data_list,
        relative_path=data_folder,
        filename=data_folder
    )



if __name__ == "__main__":
    main()
