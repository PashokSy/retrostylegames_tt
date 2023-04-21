import time

import pandas as pd
import requests, csv, pandas
from bs4 import BeautifulSoup
import lxml, html5lib

data_dict = {'Name': [], 'Rating': [], 'ReleaseDate': []}


# function for navigation through metacritic search pages
def webpage(pageNum, platform):
    url = 'https://www.metacritic.com/browse/games/genre/userscore/real-time/' \
          + str(platform) + '?view=condensed' + str(pageNum)
    userAgent = {'User-agent': 'chromedriver'}
    try:
        response = requests.get(url, headers=userAgent)
    except:
        print('Some error with response in "webpage" function')
    return response


def scrapper(num_loops, content):
    tblnum = 0
    while tblnum < num_loops:
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            if len(td) == 0:
                break
            for a in td[1].find_all('a', {"class": "title"}):
                data_dict['Name'].append(a.find('h3').text)

        for tr in table_rows:
            td = tr.find_all('td')
            if len(td) == 0:
                break
            for rating in td[1].find_all('div', {"class": "metascore_w"}):
                data_dict['Rating'].append(rating.text)

        for tr in table_rows:
            td = tr.find_all('td')
            if len(td) == 0:
                break
            for date in td[1].find_all('span', {"class": ""}):
                data_dict['ReleaseDate'].append(date.text)

        print(tblnum)

    tblnum += 1


def numberPages(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class": "page last_page"})
    pagesCleaned = pages[0].find('a', {"class": "page_num"})
    return (pagesCleaned.text)


def pages(platform):
    currentPage = 0
    while currentPage < 2:
        url = url = 'https://www.metacritic.com/browse/games/genre/userscore/real-time/' \
                    + str(platform) + '?view=condensed' + str(currentPage)
        userAgent = {'User-agent': 'chromedriver'}
        try:
            response = requests.get(url, headers=userAgent)
        except:
            print('Some error with response in "pages" function')
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find_all('table')
        num_loops = len(content)
        scrapper(num_loops, content)
        currentPage += 1
        print(f'current page - {currentPage}')
        print(data_dict.values())
        time.sleep(6)


def main():
    platform = 'pc'
    pages(platform)
    xData = (pd.DataFrame.from_dict(data_dict))
    xData.to_csv('mc.csv')


main()
