from web_scraper.scraper import fetch_page
from web_scraper.parser import parse_page
from web_scraper.storage import save_parquet
from web_scraper.config import START_URL

def main():
    print('main')
    # page_content = fetch_page(START_URL + '/en/results.html/2024/races/1230/saudi-arabia/pit-stop-summary.html')
    # data = parse_page(page_content)
    # print(data)
    # save_data(data)

def test():
    print('test')

if __name__ == "__main__":
    main()
elif __name__ == "__test__":
    test()
