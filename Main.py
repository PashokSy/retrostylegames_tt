import MetacriticScrapper as metacriticScrapper
import GooglePlayScrapper as googlePlayScrapper
import DataTools as dataTools

# data set for collecting data
games_data = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [], 'style': [], 'developer': []}


def Main():
    metacritic_data = metacriticScrapper.scrapDataFromMetacritic(1)
    google_data = googlePlayScrapper.scrapDataFromGooglePlay()
    # TODO merge dictionaries
    # games_data = metacritic_data | google_data
    # TODO check write and read functions
    # TODO create csv file reserve copy of correct data
    dataTools.writeDataSetInCSV(metacritic_data)
    dataTools.writeDataSetInCSV(google_data)
    games_data = dataTools.readDataSetInCSV()

    # some primitive checks
    print(f"{len(games_data['name'])} names {games_data['name']} \n"
          f"{len(games_data['date'])} dates {games_data['date']} \n"
          f"{len(games_data['platform'])} platforms {games_data['platform']} \n"
          f"{len(games_data['score'])} scores {games_data['score']} \n"
          f"{len(games_data['reviewCount'])} reviewCount {games_data['reviewCount']} \n"
          f"{len(games_data['style'])} style {games_data['style']} \n"
          f"{len(games_data['developer'])} developer {games_data['developer']} \n")


Main()
