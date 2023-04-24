import csv
import json
import pprint
import time

import numpy as np
import pandas as pd

import MetacriticScrapper as metacriticScrapper
import GooglePlayScrapper as googlePlayScrapper
import DataTools as dataTools


def Main():
    # scrap and write metacritic data
    # metacritic_data = metacriticScrapper.scrapDataFromMetacritic(2)
    # dataTools.writeDataSetInCSV(metacritic_data, 'metacritic_data.csv')
    # scrap and write google data
    # google_data = googlePlayScrapper.scrapDataFromGooglePlay()
    # dataTools.writeDataSetInCSV(google_data, 'google_data.csv')

    # concat two dictionaries and write result into csv file
    # metacritic_list = dataTools.readDataSetFromCSV('metacritic_data.csv')
    # google_list = dataTools.readDataSetFromCSV('google_data.csv')
    # result_list = dataTools.concatTwoDict(metacritic_list, google_list)
    # dataTools.writeDataSetInCSV(result_list, 'games_list.csv')

    # generate top for metacritic
    dataTools.writeTopInCSV('metacritic_data.csv')
    # generate top for google
    dataTools.writeTopInCSV('google_data.csv')


Main()
