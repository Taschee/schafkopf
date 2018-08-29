#!/usr/bin/env python3

from schafkopf.players.trainings_data.data_scraper import DataScraper
import pickle


scraper = DataScraper()

game_numbers = range(846000000, 846010000)

with open('train_data.p', 'wb') as outfile:

    username = input("Username : ")
    password = input("Password : ")

    driver = scraper.login_to_sauspiel(username, password)
    num_collected = 0

    for num in game_numbers:

        html = scraper.get_html(num, driver)

        if scraper.game_with_eight_cards(html):

            player_hands, game_mode, declaring_player, played_cards = scraper.scrape(html)

            if game_mode is not None:

                data = {'player_hands': player_hands,
                        'game_mode': game_mode,
                        'declaring_player': declaring_player,
                        'played_cards': played_cards}

                pickle.dump(data, outfile)

                num_collected += 1

    driver.close()

print("Collected data from {} games".format(num_collected))
