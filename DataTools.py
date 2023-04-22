import csv
import pandas as pd


# TODO create function to get top 3 games

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
            data_set['name'].append(line[0])
            data_set['date'].append(line[1])
            data_set['platform'].append(line[2])
            data_set['score'].append(line[3])
            data_set['reviewCount'].append(line[4])
            data_set['style'].append(line[5])
            data_set['developer'].append(line[6])
    return data_set
