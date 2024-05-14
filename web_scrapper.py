from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrapInitConfig(url):
    pageToScrap = requests.get(url)
    soup = BeautifulSoup(pageToScrap.text,'html.parser')
    return soup

def scrapWebF1Positions(url):
    soup = scrapInitConfig(url)
    cards = soup.findAll('a', attrs={'class': 'outline outline-offset-4 outline-brand-black group outline-0 focus-visible:outline-2'})
    res = []
    for card in cards:
        card_details = card.contents[0].contents[0]
        # print(card.contents[0])
        position = card_details.contents[0].contents[0].text
        points = card_details.contents[0].contents[1].contents[0].text
        name = card_details.contents[2].contents[0].contents[0].contents[1].text + ' ' + card_details.contents[2].contents[0].contents[0].contents[0].text
        team = card_details.contents[4].text
        driver_link = 'https://www.formula1.com' + card['href']
        data = {
            'name': name,
            'team': team,
            'points': points,
            'position': position,
            'driver_link':driver_link
            }
        res.append(data)
    return pd.DataFrame(res)
