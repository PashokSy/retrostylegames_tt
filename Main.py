import MetacriticScrapper as metacriticScrapper
import GooglePlayScrapper as googlePlayScrapper
import DataTools as dataTools

game_list = {'name': [], 'date': [], 'platform': [], 'score': [], 'reviewCount': [],
                'style': [], 'developer': [], 'downloads': []}
def Main():
    # metacritic_data = metacriticScrapper.scrapDataFromMetacritic(2)
    # google_data = googlePlayScrapper.scrapDataFromGooglePlay()
    # dataTools.writeDataSetInCSV(metacritic_data, 'metacritic_data.csv')
    # dataTools.writeDataSetInCSV(google_data, 'google_data.csv')

    game_list = dataTools.readDataSetInCSV('google_data.csv')

    print(game_list.values())


Main()
