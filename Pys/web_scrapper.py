from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import os
import io
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

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

def F1Results(url,column_link=None):
    soup = scrapInitConfig(url)
    table = soup.find('table', attrs={'class': 'resultsarchive-table'})
    res = pd.read_html(io.StringIO(str(table)))[0]
    res = res.iloc[:, 1:-1]
    # If link_column_name is provided, extract links from the specified column
    if column_link is not None:
        links = []
        link_column_index = res.columns.get_loc(column_link)+1
        for row in table.find_all('tr')[1:]:
            link = row.find_all('td')[link_column_index].find('a')
            if link:
                links.append(link['href'])
            else:
                links.append(None)        
        # Add links as a new column to the DataFrame
        res[column_link + '_link'] = links
    return res.to_dict('records')

def F1RaceResultsLinks(url):
    soup = scrapInitConfig(url)
    li_tags = soup.find_all("li", class_="side-nav-item")
    links_dict = {}
    for li in li_tags:
        a_tags = li.find_all("a")
        for a_tag in a_tags:
            link = a_tag.get("href") 
            text = a_tag.get_text()  
            links_dict[text] = link  
    return links_dict

def createDir(path):
    if not path.endswith('/'):
        path = path + '/'
    # print (path)
    if not os.path.exists(path):
        os.makedirs(path)

def createJSON(path,filename,dict):
    path=os.getenv("DESTINTATION_PATH") + '/'+ path
    createDir(path)
    if not path.endswith('/'):
        path = path + '/'
    with open(path+filename+'.json', 'w+', encoding='latin-1') as f:
        json.dump(dict, f, indent=4, ensure_ascii=False)

def F1MinMaxYears(url):
    soup = scrapInitConfig(url)
    table = soup.find('div', class_='resultsarchive-filter-container').find('div').findAll('a')
    print(table)
    # for i in table[0].contents[0].contents[0]: