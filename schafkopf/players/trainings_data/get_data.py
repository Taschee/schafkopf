#!/usr/bin/env python3

from schafkopf.players.trainings_data.data_scraper import DataScraper
import pickle


scraper = DataScraper()

game_numbers = [846389616, 846389972, 846389815, 846389389, 846389142]

with open('data_test.p', 'wb') as outfile:

    username = input("Username : ")
    password = input("Password : ")

    for num in game_numbers:

        html = scraper.get_html(num, username, password)

        if scraper.game_with_eight_cards(html):

            player_hands, game_mode, declaring_player, played_cards = scraper.scrape(html)

            if game_mode is not None:

                data = {'player_hands': player_hands,
                        'game_mode': game_mode,
                        'declaring_player': declaring_player,
                        'played_cards': played_cards}

                pickle.dump(data, outfile)

