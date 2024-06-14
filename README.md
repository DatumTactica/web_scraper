# Web Scraper for Formula 1 Data

## Project Description

This Python project is designed to scrape and store various types of data from the Formula 1 website. It collects information about drivers, their positions, race results, team results, and other related data. The scraped data is then saved in Parquet format for easy storage and retrieval.

## Project Structure

The project is organized as follows:

```
web_scraper
    web_scraper
        __init__.py
        config.py
        drivers.py
        results_drivers.py
        results_fastest_lap.py
        results_races.py
        results_teams.py
        scraper.py
        storage.py
    .env
    requirements.txt
```

### File Descriptions

- **web_scraper/config.py**: Loads environment variables and sets configuration constants.
- **web_scraper/drivers.py**: Scrapes and saves the drivers' positions and details.
- **web_scraper/results_drivers.py**: Scrapes and saves the race results of drivers for the specified years.
- **web_scraper/results_fastest_lap.py**: Scrapes and saves the fastest lap results for drivers.
- **web_scraper/results_races.py**: Scrapes and saves the race results and individual Grand Prix results.
- **web_scraper/results_teams.py**: Scrapes and saves the team results for the specified years.
- **web_scraper/scraper.py**: Contains functions to fetch and parse the web pages.
- **web_scraper/storage.py**: Contains functions to save the scraped data as Parquet files.
- **.env**: Environment file to store the destination path for saving Parquet files.
- **requirements.txt**: Lists the Python dependencies for the project.

## Installation Instructions

### Prerequisites

Ensure you have Python 3.8+ installed on your system. You will also need `pip` for managing Python packages.

### Steps

1. **Clone the repository**:
   ```sh
   git clone <repository_url>
   cd web_scraper
   ```

2. **Set up a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory of the project with the following content:
   ```
   DESTINTATION_PATH='/path/to/save/data'
   ```

   Replace `/path/to/save/data` with the actual path where you want to save the Parquet files.

## Execution Instructions

### Drivers' Positions and Details

To scrape and save the drivers' positions and details, run:
```sh
python -m web_scraper.drivers
```

### Drivers' Race Results

To scrape and save the race results of drivers, run:
```sh
python -m web_scraper.results_drivers
```

### Fastest Lap Results

To scrape and save the fastest lap results, run:
```sh
python -m web_scraper.results_fastest_lap
```

### Race Results and Grand Prix Details

To scrape and save the race results and individual Grand Prix results, run:
```sh
python -m web_scraper.results_races
```

### Team Results

To scrape and save the team results, run:
```sh
python -m web_scraper.results_teams
```

## Structure of the Output

The output data is stored in Parquet format in the specified destination path. The data is organized into different folders based on the type of information:

- **drivers_positions**: Contains the drivers' positions data. Scraped from [Formula 1 Drivers](https://www.formula1.com/en/drivers.html).
- **drivers**: Contains the detailed information of each driver. Scraped from the individual driver pages linked from the drivers' positions page.
- **results_drivers**: Contains the race results of drivers, partitioned by year and driver. Scraped from [Formula 1 Driver Results](https://www.formula1.com/en/results.html).
- **results_fastest_lap**: Contains the fastest lap results, partitioned by year and driver. Scraped from [Formula 1 Fastest Lap Results](https://www.formula1.com/en/results.html).
- **results_races**: Contains the race results, partitioned by year and Grand Prix. Scraped from [Formula 1 Race Results](https://www.formula1.com/en/results.html).
- **gp_results_races**: Contains detailed Grand Prix results, partitioned by date and Grand Prix. Scraped from the individual Grand Prix results pages linked from the race results page.
- **results_teams**: Contains the team results, partitioned by year. Scraped from [Formula 1 Team Results](https://www.formula1.com/en/results.html).

There are several `gp_` folders. These folders depend on the available links for each Grand Prix, such as qualifying results, practice results, etc.

Each Parquet file is named based on the data it contains, and the folders are structured to make it easy to query and analyze the data.

## Logging

The project uses Python's built-in `logging` module to provide informative log messages during execution. This can help in troubleshooting and understanding the flow of data collection.

## Conclusion

This project provides a comprehensive solution for scraping and storing Formula 1 data. By following the installation and execution instructions, you can easily gather detailed information about drivers, races, teams, and more. The use of Parquet format ensures efficient storage and fast retrieval for further analysis.