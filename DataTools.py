import csv
import pandas as pd

#TODO create function to get top 3 games

def writeDataSetInCSV(data_set):
    game = pd.DataFrame.from_dict(data_set, orient='index')
    games = game.transpose()
    games.to_csv('games_list.csv', index=False, header=True, mode='w')


def readDataSetInCSV():
    data_set = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [], 'style': [], 'developer': []}
    filename = 'games_list.csv'
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            if line[0] == 'name':
                continue
            data_set['name'] = line[0]
            data_set['date'] = line[1]
            data_set['platform'] = line[2]
            data_set['score'] = line[3]
            data_set['reviewCount'] = line[4]
            data_set['style'] = line[5]
            data_set['developer'] = line[6]
