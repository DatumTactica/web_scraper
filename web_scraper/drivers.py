from web_scraper.config import STORAGE_ROOT
from web_scraper.config import START_URL
from web_scraper.scraper import F1DriversPositions,F1Details
from web_scraper.storage import save_parquet
from datetime import datetime

def main():
    # Get current date
    date = datetime.today().strftime('%Y%m%d')

    # Set parent folder 
    data_folder = 'drivers_positions'

    drivers_positions_url = START_URL + '/en/drivers'
    # Get race results
    drivers = F1DriversPositions(drivers_positions_url)
    drivers_list = list(drivers.values()) 
    
    save_parquet(
        data = drivers_list,
        relative_path=data_folder,
        filename=data_folder + '_' + date
    )

    # Set parent folder 
    data_folder = 'drivers'

    data = {}
    for i in drivers:
        data[i] = F1Details(drivers[i]['driver_link'],drivers[i]['name'])

    data_list = list(data.values())

    save_parquet(
        data = data_list,
        relative_path=data_folder,
        filename=data_folder
    )



if __name__ == "__main__":
    main()
