import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

# google appstore url
appstore_url = 'https://play.google.com/store/search?q=real-time%20strategy%20realism&c=apps'
user_agent = {'User-agent': 'Mozilla/5.0'}

# data set for collecting data
google_play_data = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [], 'style': [],
                    'developer': [], 'downloads': []}


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
            count_number_list = gameReviewCount.get_text().split(' ', 1)
            count_number = count_number_list[0]
            striped_count_number = stripText(count_number)
            google_play_data['reviewCount'].append(striped_count_number)
        # scrap data from game page url for developer
        for gameDeveloper in game_soup.find_all('div', {'class', 'Vbfug auoIOc'}):
            google_play_data['developer'].append(gameDeveloper.get_text().strip())
        # get update date
        for gameDate in game_soup.find_all('div', {'class': 'xg1aie'}):
            google_play_data['date'].append(gameDate.get_text().strip())
        # get downloads count
        download_number_list = []
        for download in game_soup.find_all('div', {'class': 'ClM7O'}):
            download_number_list.append(download.get_text().strip())
        striped_downloads = stripText(download_number_list[1])
        google_play_data['downloads'].append(striped_downloads)
        # all games in list are mobile and realistic
        google_play_data['platform'].append('Mobile')
        google_play_data['style'].append('Realism')

    return google_play_data


def stripText(text):
    result_text = ''
    if text.find('+'):
        text = text.replace('+', '')
    if text.find('K') > 0 > text.find('.'):
        result_text = text.replace('K', '') + '000'
    elif text.find('K') > 0 and text.find('.') > 0:
        result_text = text.replace('K', '').replace('.', '') + '00'
    elif text.find('M') > 0 > text.find('.'):
        result_text = text.replace('M', '') + '000000'
    elif text.find('M') > 0 and text.find('.') > 0:
        result_text = text.replace('M', '').replace('.', '') + '00000'
    return result_text


def createDataFrame():
    game = pd.DataFrame.from_dict(google_play_data, orient='index')
    games = game.transpose()
    games.to_csv('games_list.csv', index=False, header=True, mode='w')
