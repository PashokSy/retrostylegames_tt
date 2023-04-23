import csv
import itertools

import pandas as pd


def writeDataSetInCSV(data_set, file_name):
    game = pd.DataFrame.from_dict(data_set, orient='index')
    games = game.transpose()
    games.to_csv(str(file_name), index=False, header=True, mode='w+')


def readDataSetFromCSV(file_name):
    data_set = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [],
                'style': [], 'developer': [], 'downloads': []}
    with open(str(file_name), 'r+') as data:
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
            data_set['downloads'].append(line[7])
    return data_set


def concatTwoDict(dict1, dict2):
    for key in dict2:
        for value in dict2[key]:
            dict1[key].append(value)
    return dict1


def key_value_combinations(keys, values):
    items = list(zip(keys, values))
    value_combinations = itertools.product(*[item[1] for item in items])
    combinations = [{items[i][0]: combination[i] for i in range(len(items))} for combination in value_combinations]
    return combinations
