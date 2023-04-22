import time
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# google appstore url
appstore_url = 'https://play.google.com/store/search?q=real-time%20strategy%20realism&c=apps&hl=en&gl=US'
user_agent = {'User-agent': 'Mozilla/5.0'}

# data set for collecting data
google_play_data = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [], 'style': [],
                    'developer': []}


# method to scrape data from Google play
def scrapDataFromGooglePlay():
    request = requests.get(appstore_url, user_agent)
    soup = BeautifulSoup(request.text, 'html.parser')

    # Getting game page
    for gamePage in soup.find_all('a', {'class': 'Si6A0c Gy4nib'}):
        # wait some time to not get ip ban
        time.sleep(6)

        # get game page url
        game_url = 'https://play.google.com' + gamePage['href']
        game_request = requests.get(game_url, headers=user_agent)
        game_soup = BeautifulSoup(game_request.text, 'html.parser')

        # scrap data from game page url for name
        for gameName in game_soup.find_all('h1', {'itemprop': 'name'}):
            google_play_data['name'].append(gameName.get_text().strip())
        # scrap data from game page url for score
        for gameScore in game_soup.find_all('div', {'class': 'TT9eCd'}):
            score = float(gameScore.get_text().strip()[:3]) * 2
            google_play_data['score'].append(str(score))
        # scrap data from game page url for score
        for gameReviewCount in game_soup.find_all('div', {'class': 'g1rdde'}, limit=1):
            countNumberList = gameReviewCount.get_text().split(' ', 1)
            countNumber = countNumberList[0]
            if countNumber.find('K') > 0 > countNumber.find('.'):
                countNumber = countNumber.replace('K', '') + '000'
            elif countNumber.find('K') > 0 and countNumber.find('.') > 0:
                countNumber = countNumber.replace('K', '')
                countNumber = countNumber.replace('.', '') + '00'
            elif countNumber.find('M') > 0 > countNumber.find('.'):
                countNumber = countNumber.replace('K', '') + '000000'
            elif countNumber.find('M') > 0 and countNumber.find('.') > 0:
                countNumber = countNumber.replace('K', '')
                countNumber = countNumber.replace('.', '') + '00000'
            google_play_data['reviewCount'].append(countNumber)
        # scrap data from game page url for developer
        for gameDeveloper in game_soup.find_all('div', {'class', 'Vbfug auoIOc'}):
            google_play_data['developer'].append(gameDeveloper.get_text().strip())
        # get update date
        for gameDate in game_soup.find_all('div', {'class': 'xg1aie'}):
            google_play_data['date'].append(gameDate.get_text().strip())
        # all games in list are mobile and realistic
        google_play_data['platform'].append('Mobile')
        google_play_data['style'].append('Realism')

    return google_play_data



def createDataFrame():
    game = pd.DataFrame.from_dict(google_play_data, orient='index')
    games = game.transpose()
    games.to_csv('games_list.csv', index=False, header=True, mode='w')
