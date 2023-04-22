import time
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# hardcode metacritic url with !NO page number
metacritic_url = 'https://www.metacritic.com/browse/games/genre/userscore/real-time/all?view=condensed&page='
user_agent = {'User-agent': 'Mozilla/5.0'}

# data set for collected data
metacritic_data = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [], 'style': [], 'developer': []}


# method to get data for BeautifulSoup
def get_page_content(url):
    page = requests.get(url, headers=user_agent)
    return BeautifulSoup(page.text, 'html.parser')


# method to add data in dataset from first to selected pages
def scrapDataFromMetacritic(endPage):
    currentPage = 0
    while currentPage < endPage:
        url = metacritic_url + str(currentPage)

        # Getting data for further parse
        soup = get_page_content(metacritic_url)

        # Parse web-page to find all game names
        for a in soup.find_all('a', {'class': 'title'}):
            for h3 in a.find_all('h3'):
                name = h3.get_text().strip()
                metacritic_data['name'].append(name)

        # Parse web-page to find all release dates and platforms (in same cycle because in same 'td')
        for td in soup.find_all('td', {'class', 'details'}):
            # Get game release date
            for date_span in td.find_all('span', {'class': ''}):
                date = date_span.get_text().strip()
                metacritic_data['date'].append(date)
            # Get game platform
            for platform_span in td.find_all('span', {'class': 'data'}):
                platform = platform_span.get_text().strip()
                metacritic_data['platform'].append(platform)

        # Parse web-page to find all user scores
        for meta_score in soup.find_all('div', {'class': 'metascore_w user large game positive'}):
            score = meta_score.get_text().strip()
            metacritic_data['score'].append(score)

        # Move to game page to extract review count
        for gamePage in soup.find_all('a', {'class': 'title'}):
            new_url = 'https://www.metacritic.com' + gamePage['href']
            new_page = requests.get(new_url, headers=user_agent)
            new_soup = BeautifulSoup(new_page.text, 'html.parser')
            for review_span in new_soup.find_all(name='a',
                                                 attrs={'href': gamePage['href'] + '/user-reviews', 'class': ''},
                                                 limit=1):
                review_count = re.findall(r'\d+', review_span.get_text().strip())
                metacritic_data['reviewCount'].append(review_count.pop())
            for developer_span in new_soup.find_all(name='a',
                                                    href=True,
                                                    attrs={'class': 'button'},
                                                    limit=1):
                metacritic_data['developer'].append(developer_span.get_text().strip())

        # wait some time to not get banned
        time.sleep(6)
        currentPage += 1  # transfer to next page


# TODO finish wiki scraper
# Search wiki list of rts for styles of the games in list
def getStyleFromWiki():
    wickiList = 'https://en.wikipedia.org/wiki/List_of_real-time_strategy_video_games#List'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    wikiPage = requests.get(wickiList, headers=user_agent)
    wikiSoup = BeautifulSoup(wikiPage.text, 'html.parser')

    for name in metacritic_data['name']:
        next_siblind = wikiSoup.find_next_sibling('a', {'title': str(name)})
        print(next_siblind)

        """for td in utopia.find_all_next('td'):
            print('-----')
            print(td.get_text().strip())
            print('------')
            metacritic_data['style'].append(td.get_text().strip())
"""

# Save result dictionary to csv file
def createDataFrame():
    game = pd.DataFrame.from_dict(metacritic_data, orient='index')
    games = game.transpose()
    games.to_csv('games_list.csv', index=False, header=True, mode='w')


# Method for call from main
def initiateMetacriticDataScrap(endPage):
    scrapDataFromMetacritic(endPage)
    createDataFrame()

    # some primitive checks
    print(f"{len(metacritic_data['name'])} names {metacritic_data['name']} \n"
          f"{len(metacritic_data['date'])} dates {metacritic_data['date']} \n"
          f"{len(metacritic_data['platform'])} platforms {metacritic_data['platform']} \n"
          f"{len(metacritic_data['score'])} scores {metacritic_data['score']} \n"
          f"{len(metacritic_data['reviewCount'])} reviewCount {metacritic_data['reviewCount']} \n"
          f"{len(metacritic_data['style'])} style {metacritic_data['style']} \n"
          f"{len(metacritic_data['developer'])} developer {metacritic_data['developer']} \n")
