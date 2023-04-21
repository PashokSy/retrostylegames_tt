import time

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# hardcode metacritic url with !NO page number
metacritic_url = 'https://www.metacritic.com/browse/games/genre/userscore/real-time/all?view=condensed&page='
user_agent = {'User-agent': 'Mozilla/5.0'}

# data set for collected data
metacritic_data = {'name': [], 'date': [], 'platform': [], 'score': []}


# method to get data for BeautifulSoup
def get_page_content(url):
    page = requests.get(url, headers=user_agent)
    return BeautifulSoup(page.text, 'html.parser')


# method to add data in dataset from first to selected pages
def add_data(url, endPage):
    currentPage = 0
    while currentPage < endPage:
        url = url + str(currentPage)

        # Getting data for further parse
        soup = get_page_content(metacritic_url)

        # Parse web-page to find all game names
        for a in soup.find_all('a', {'class': 'title'}):
            for h3 in a.find_all('h3'):
                name = h3.get_text().strip()
                metacritic_data['name'].append(name)

        # Parse web-page to find all release dates and platforms (in same cycle because in same 'td')
        for td in soup.find_all('td', {'class', 'details'}):
            for date_span in td.find_all('span', {'class': ''}):
                date = date_span.get_text().strip()
                metacritic_data['date'].append(date)
            for platform_span in td.find_all('span', {'class': 'data'}):
                platform = platform_span.get_text().strip()
                metacritic_data['platform'].append(platform)

        # Parse web-page to find all user scores
        for meta_score in soup.find_all('div', {'class': 'metascore_w user large game positive'}):
            score = meta_score.get_text().strip()
            metacritic_data['score'].append(score)

        # wait some time to not get banned
        time.sleep(6)
        currentPage += 1  # transfer to next page

    # console print some checks
    print(f"{len(metacritic_data['name'])} names {metacritic_data['name']} \n"
          f"{len(metacritic_data['date'])} dates {metacritic_data['date']} \n"
          f"{len(metacritic_data['platform'])} platforms {metacritic_data['platform']} \n"
          f"{len(metacritic_data['score'])} scores {metacritic_data['score']}")


def createDataFrame():
    game = pd.DataFrame.from_dict(metacritic_data, orient='index')
    games = game.transpose()
    games.to_csv('games_list.csv', index=False, header=True)


def main():
    add_data(metacritic_url, 1)
    createDataFrame()


main()
