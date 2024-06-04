from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

def scrapInitConfig(url):
    pageToScrap = requests.get(url)
    soup = BeautifulSoup(pageToScrap.text,'html.parser')
    return soup

def F1DriversPositions(url):
    soup = scrapInitConfig(url)
    cards = soup.findAll('a', attrs={'class': 'outline outline-offset-4 outline-brand-black group outline-0 focus-visible:outline-2'})
    res = []
    keys, values = [], []
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
            'driver_link':driver_link
            }
        keys.append(position)
        values.append(data)
    return dict(zip(keys, values))

def F1Details(url,driver):
    soup = scrapInitConfig(url)
    headers = soup.findAll('dt')
    texts = soup.findAll('dd')
    keys, values = ['Name'], [driver]
    for header,text in zip(headers,texts):
        # print(table)
        keys.append(header.text)
        values.append(text.text)
    return dict(zip(keys, values))

def F1TeamsPositions(url):
    soup = scrapInitConfig(url)
    cards = soup.findAll('a', attrs={'class': 'outline outline-offset-4 outline-brand-black group outline-0 focus-visible:outline-2'})
    res = []
    keys, values = [], []
    for card in cards:
        card_details = card.contents[0].contents[0]
        # print(card.contents[0])
        position = card_details.contents[0].contents[0].text
        points = card_details.contents[0].contents[1].contents[0].text
        name = card_details.contents[2].contents[0].contents[0].contents[0].text
        drivers = {
            'driver1': card_details.contents[4].contents[0].contents[0].contents[0].contents[0].text + ' ' + card_details.contents[4].contents[0].contents[0].contents[0].contents[1].text,
            'driver2': card_details.contents[4].contents[1].contents[0].contents[0].contents[0].text + ' ' + card_details.contents[4].contents[1].contents[0].contents[0].contents[1].text
        }
        team_link = 'https://www.formula1.com' + card['href']
        data = {
            'name': name,
            'drivers': drivers,
            'points': points,
            'team_link':team_link
            }
        keys.append(position)
        values.append(data)
    return dict(zip(keys, values))

def F1Results(url):
    soup = scrapInitConfig(url)
    table = soup.findAll('table', attrs={'class': 'resultsarchive-table'})
    res = pd.read_html(str(table))[0]
    del res[res.columns[0]]
    del res[res.columns[-1]]
    return res.to_dict('records')

def createJSON(path,dict):
    with open(path+'.json', 'w', encoding='latin-1') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)

def F1MinMaxYears(url):
    soup = scrapInitConfig(url)
    table = soup.find('div', class_='resultsarchive-filter-container').find('div').findAll('a')
    print(table)
    # for i in table[0].contents[0].contents[0]: