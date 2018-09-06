#!/usr/bin/env python3

from schafkopf.players.data.data_scraper import DataScraper
import pickle


scraper = DataScraper()


# scraped data from #846000000 - 846320000
# test data from #700000000 - 700010000
# validation data from #700010000 - 700020000

game_numbers = range(846300000, 846320000)

with open('train_data.p', 'ab') as outfile:

    username = input("Username : ")
    password = input("Password : ")

    driver = scraper.login_to_sauspiel(username, password)
    num_collected = 0

    for num in game_numbers:
        try:
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

        except:
            continue

    driver.close()

print("Collected data from {} games".format(num_collected))
