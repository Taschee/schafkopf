from schafkopf.players.trainings_data.data_scraper import DataScraper
import pickle


scraper = DataScraper()


game_numbers = [846389616, 846389972, 846389815, 846389389, 846389142]

with open('data_test.p', 'wb') as outfile:

    for num in game_numbers:
        player_hands, game_mode, declaring_player, played_cards = scraper.scrape(game_num=num)

        data = {'player_hands': player_hands,
                'game_mode': game_mode,
                'declaring_player': declaring_player,
                'played_cards': played_cards}

        pickle.dump(data, outfile)

